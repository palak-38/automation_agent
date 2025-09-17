# Data Science Report: Action Item Extraction via Fine-Tuning

## 1. Fine-Tuning Setup

### Data
- **Task**: Extract structured action items (task, owner, due date) from dialogues.
- **Format**: Dialogue text as input, JSON-formatted action items as target.
- **Size**: 167 test examples (training set was larger, not shown in screenshot but inferred from standard splits).
- **Example**:  
  Input: “Katy: I’m at the entrance … Katy: ok, I’ll be there in 5 min”  
  Target JSON: `{ "task": "Meet at the main entrance to the university", "owner": "Katy", "due_date": "in 5 min" }`

### Method
- **Model**: A sequence-to-sequence transformer (likely T5 or FLAN-T5, judging by JSON generation style).
- **Training**: Fine-tuning on dialogue–JSON pairs.
- **Objective**: Minimize text-to-text generation loss (cross-entropy).
- **Evaluation Scripts**: Metrics computed include exact match, ROUGE-L, and Bag-of-Words F1.

---

## 2. Evaluation Methodology

### Metrics Used
- **Exact Match (EM)**: Strict string-level equality between predicted and reference JSON.  
  *Result: 0.0000 → model never produced an exact reference match.*
- **ROUGE-L F1 (0.4012)**: Measures longest common subsequence overlap, rewarding structural and lexical similarity.
- **BoW F1 (0.4112)**: Token-level overlap ignoring order.
- **Average Prediction Length (18.89)** vs **Reference Length (28.06)**: Predictions were ~30% shorter, indicating missing details.

### Procedure
- Model was run on the **held-out test set (167 dialogues)**.
- Each prediction compared against ground truth with above metrics.
- Both quantitative scores and qualitative inspection (sample predictions) were included.

---

## 3. Results and Outcomes

### Quantitative Findings
- **Exact Match = 0%**: Indicates difficulty in strict JSON matching. Small deviations (e.g., “Be at the entrance of the library” vs. “Meet at the main entrance to the university”) cause failure despite semantic similarity.
- **ROUGE-L ≈ 0.40, BoW F1 ≈ 0.41**: Moderate lexical overlap — model captures partial task information but misses fine-grained phrasing or details.
- **Length Mismatch**: Model under-generates, omitting contextual details (owner, task qualifiers).

### Qualitative Findings
- Example:  
  **Reference**: “Meet at the main entrance to the university”  
  **Prediction**: “Be at the entrance of the library”  
  → Same intent (meet at entrance), but wrong location detail. Semantically close, but fails exact matching.

### Interpretation
- The model **understands dialogue intent partially** but struggles with:
  - Precision in task phrasing.
  - Maintaining all fields in JSON.
  - Disambiguating similar entities (library vs. university entrance).

---

## 4. Recommendations

1. **Structured Decoding**: Constrain output with JSON schema (e.g., using constrained beam search).
2. **Data Augmentation**: Add more varied phrasings for locations, owners, and time expressions.
3. **Evaluation**: Introduce semantic similarity metrics (e.g., BERTScore) to complement strict exact match.
4. **Post-Processing**: Apply repair heuristics (normalize due_date formats, enforce field presence).
5. **Error Analysis**: Categorize errors (missing fields, wrong entity, truncation) to target improvements.

---
