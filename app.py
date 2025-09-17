# app.py
import os
import re
import json
import torch
import pandas as pd
import gradio as gr
from transformers import T5ForConditionalGeneration, T5Tokenizer
from peft import PeftModel

# --------------------
# Configuration
# --------------------
LOCAL_MODEL_PATH = r"C:\Users\hp\Desktop\summer'26\imby\final_stage\flan-t5-action-extractor-final"   # LoRA dir with adapter_config.json + adapter weights
BASE_MODEL_NAME = "google/flan-t5-base"                          # requires sentencepiece installed

# --------------------
# Prompting: schema + examples to force JSON
# --------------------
SCHEMA_INSTRUCTIONS = """You are an information extraction model.
Given a multi-speaker chat transcript, extract action items as a JSON array.
Each item MUST be an object with exactly these keys: "task", "owner", "due_date".

Strict rules:
- Output MUST be valid JSON. No comments, no extra text, no markdown fences.
- If no clear action items, output [].
- "owner": a person name if present, else "".
- "due_date": a natural-language date if present (e.g., "Friday", "EOD tomorrow", "2025-09-15"), else "".
- "task": a short imperative phrase.
- Do NOT repeat keys at top-level. The output must look like:
  [
    {"task":"...", "owner":"...", "due_date":"..."},
    {"task":"...", "owner":"...", "due_date":"..."}
  ]
"""

FEW_SHOT = [
    (
        """Alex: Hey team, quick sync for the project.
Ben: Go ahead.
Alex: I've finished the draft of the report. Ben, can you review it by EOD tomorrow?
Chloe: What about slides?
Alex: Chloe, you're on slides. First draft by Friday. I'll handle data viz.
Ben: Got it, I'll review the report.
Chloe: Okay, slides by Friday.""",
        [
            {"task": "Review the report", "owner": "Ben", "due_date": "EOD tomorrow"},
            {"task": "Create first draft of presentation slides", "owner": "Chloe", "due_date": "Friday"},
            {"task": "Handle data visualization", "owner": "Alex", "due_date": ""}
        ]
    ),
    (
        """PM: Standup. Updates?
Dev1: I'll push the login bug fix today.
Dev2: Need to schedule meeting with design to finalize dashboard mockups.
PM: Great. Dev1, ping when live. Dev2, set up that meeting this week.""",
        [
            {"task": "Push fix for the login bug", "owner": "Dev1", "due_date": "today"},
            {"task": "Schedule meeting with design to finalize dashboard mockups", "owner": "Dev2", "due_date": "this week"}
        ]
    )
]

def build_prompt(dialogue: str) -> str:
    parts = [SCHEMA_INSTRUCTIONS, "Examples:"]
    for chat, items in FEW_SHOT:
        parts.append("Chat:")
        parts.append(chat.strip())
        parts.append("JSON:")
        parts.append(json.dumps(items, ensure_ascii=False))
    parts.append("Chat:")
    parts.append(dialogue.strip())
    parts.append("JSON:")  # important: bias model to emit JSON next
    return "\n".join(parts)

# --------------------
# JSON repair helpers (now includes triplet salvager)
# --------------------
def strip_markdown_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        # remove starting ```
        s = s[3:]
        # remove optional language tag until first newline
        if "\n" in s:
            s = s.split("\n", 1)[1]
        # remove trailing ```
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()

def extract_json_segment(s: str) -> str:
    s = s.strip()
    # Prefer array
    lb = s.find("["); rb = s.rfind("]")
    if lb != -1 and rb != -1 and rb > lb:
        return s[lb:rb+1].strip()
    # Fallback to object
    lb = s.find("{"); rb = s.rfind("}")
    if lb != -1 and rb != -1 and rb > lb:
        return s[lb:rb+1].strip()
    return s

def normalize_quotes(s: str) -> str:
    return (s.replace("“", '"').replace("”", '"')
             .replace("’", "'").replace("‘", "'"))

def try_parse_json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None

def remove_trailing_commas(s: str) -> str:
    # remove commas before ] or }
    return re.sub(r",\s*(\]|\})", r"\1", s)

def salvage_triplets(s: str):
    """
    Salvage outputs like:
      ["task": "X", "owner": "Y", "due_date": "Z", "task": "X2", "owner": "Y2", "due_date": "Z2"]
    by grouping triples into objects.
    """
    # Find all key/value pairs in order
    kv = re.findall(r'"(task|owner|due_date)"\s*:\s*"([^"]*)"', s)
    if not kv:
        return None
    items = []
    current = {}
    for k, v in kv:
        current[k] = v
        if set(current.keys()) == {"task", "owner", "due_date"}:
            items.append({
                "task": current.get("task", "").strip(),
                "owner": current.get("owner", "").strip(),
                "due_date": current.get("due_date", "").strip(),
            })
            current = {}
    # if leftover keys exist but incomplete, we ignore them
    return items if items else None

def minimal_repair_and_parse(s: str):
    s1 = strip_markdown_fences(s)
    s2 = extract_json_segment(s1)
    s3 = normalize_quotes(s2)
    parsed = try_parse_json(s3)
    if parsed is not None:
        return parsed
    # Try after trailing comma removal
    s4 = remove_trailing_commas(s3)
    parsed = try_parse_json(s4)
    if parsed is not None:
        return parsed
    # Last resort: salvage key-value triplets
    salvaged = salvage_triplets(s4)
    return salvaged  # may be None or a list of dicts

def coerce_to_list(x):
    if x is None:
        return None
    if isinstance(x, list):
        return x
    if isinstance(x, dict):
        return [x]
    return None

def enforce_schema(items):
    out = []
    for it in items:
        if not isinstance(it, dict):
            continue
        task = str(it.get("task", "")).strip()
        owner = str(it.get("owner", "")).strip()
        due = str(it.get("due_date", "")).strip()
        if not task:
            continue
        out.append({"task": task, "owner": owner, "due_date": due})
    return out

# --------------------
# Loader
# --------------------
def load_extractor_model_safe(base_model_name: str, peft_model_path: str):
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    print(f"Using device: {device}")

    if not os.path.isdir(peft_model_path):
        raise FileNotFoundError(f"LoRA path not found or not a directory: {peft_model_path}")

    print("Loading tokenizer...")
    tokenizer = T5Tokenizer.from_pretrained(base_model_name, legacy=True)
    print("Tokenizer loaded successfully")

    print("Loading base model...")
    dtype = torch.float16 if use_cuda else torch.float32
    base_model = T5ForConditionalGeneration.from_pretrained(
        base_model_name,
        dtype=dtype,
    )
    print("Base model loaded successfully")

    print("Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, peft_model_path)
    print("LoRA adapter loaded successfully")

    print("Merging adapter weights...")
    model = model.merge_and_unload()
    model = model.to(device)
    model.eval()
    print("Model ready for inference")

    return model, tokenizer, device

# --------------------
# Global load (once)
# --------------------
try:
    extractor_model, extractor_tokenizer, extractor_device = load_extractor_model_safe(
        BASE_MODEL_NAME, LOCAL_MODEL_PATH
    )
except Exception as e:
    print(f"\nError loading model: {e}")
    import traceback
    traceback.print_exc()
    raise SystemExit("Model failed to load. Fix the error above and rerun.")

# --------------------
# Inference function
# --------------------
def process_chat(chat_dialogue: str) -> pd.DataFrame:
    if extractor_model is None or extractor_tokenizer is None:
        raise gr.Error("Model is not loaded. Please check the console for errors.")

    print("\n--- New Request ---")
    print("Received dialogue for processing.")

    prompt = build_prompt(chat_dialogue)
    device = extractor_device or next(extractor_model.parameters()).device

    inputs = extractor_tokenizer(
        prompt,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Deterministic, mildly constrained decoding to reduce babble/repetition
    with torch.no_grad():
        outputs = extractor_model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,     # deterministic
            num_beams=4,
            repetition_penalty=1.2,  # push away from repeated phrases
            early_stopping=True,
            length_penalty=0.0,
            eos_token_id=extractor_tokenizer.eos_token_id,
            pad_token_id=extractor_tokenizer.pad_token_id,
        )

    raw = extractor_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    print(f"Raw model output: {raw}")

    # Robust parsing & salvage
    parsed = minimal_repair_and_parse(raw)
    items = coerce_to_list(parsed)
    if items is None:
        print("Validation failed: Model output is not valid JSON.")
        return pd.DataFrame(columns=["task", "owner", "due_date"])

    items = enforce_schema(items)
    if not items:
        print("No valid action items found after schema enforcement.")
        return pd.DataFrame(columns=["task", "owner", "due_date"])

    df = pd.DataFrame(items, columns=["task", "owner", "due_date"])
    return df

# --------------------
# Gradio UI
# --------------------
def build_interface():
    with gr.Blocks(theme="soft") as iface:
        gr.Markdown(
            """
            # 🤖 AI Agent: Action Item Extractor
            Paste a chat dialogue below. The agent extracts action items as a JSON table
            (task, owner, due_date).
            """
        )
        with gr.Row():
            chat_input = gr.Textbox(
                lines=15,
                label="Chat Dialogue",
                placeholder="Paste your chat here..."
            )
            action_item_output = gr.DataFrame(
                label="Extracted Action Items",
                headers=["task", "owner", "due_date"]
            )

        submit_button = gr.Button("Extract Action Items", variant="primary")
        submit_button.click(fn=process_chat, inputs=chat_input, outputs=action_item_output)

        gr.Markdown("## Examples")
        gr.Examples(
            examples=[
                [
                    """
                    Alex: Hey team, quick sync for the project.
                    Ben: Go ahead.
                    Alex: I've finished the initial draft of the report. Ben, can you review it by EOD tomorrow?
                    Chloe: What about the presentation slides?
                    Alex: Good point. Chloe, you're on slides. Let's aim to have a first draft by Friday. I'll handle the data visualization part.
                    Ben: Got it, I'll review the report.
                    Chloe: Okay, slides by Friday it is.
                    """
                ],
                [
                    """
                    PM: Okay, standup time. Engineering updates?
                    Dev1: I'll push the fix for the login bug today.
                    Dev2: I need to schedule a meeting with the design team to finalize the new dashboard mockups.
                    PM: Great. Dev1, let us know when the fix is live. Dev2, please set up that meeting for this week.
                    """
                ]
            ],
            inputs=chat_input
        )
    return iface

if __name__ == "__main__":
    print("\nLaunching Gradio app...")
    iface = build_interface()
    iface.launch(debug=True)  # set share=True if you need a public link

