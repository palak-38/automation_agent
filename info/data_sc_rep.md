# Data Science Report: Action Item Extraction via Fine-Tuning

## 1. Fine-Tuning Setup

### Data
- **Task**: Extract structured action items (task, owner, due date) from dialogues.
- **Format**: Dialogue text as input, JSON-formatted action items as target.
- **Size**: 167 test examples (training set was larger).
- **Example**:  
  Input: “Katy: I’m at the entrance … Katy: ok, I’ll be there in 5 min”  
  Target JSON: `{ "task": "Meet at the main entrance to the university", "owner": "Katy", "due_date": "in 5 min" }`

### Method
- **Model**: FLAN-T5 
- **Training**: Fine-tuning on dialogue–JSON pairs.
- **Objective**:Extract Action Items out of Group Chats along with Asignee and Deadline
- **Evaluation Scripts**: Metrics computed include exact match, ROUGE-L, and Bag-of-Words F1.

---

## 2. Evaluation Methodology

### Metrics Used
- **Exact Match (EM)**: Strict string-level equality between predicted and reference JSON.  
  *Result: 0.0000 → model never produced an exact reference match.*
- **ROUGE-L F1 (0.4012)**: Measures longest common subsequence overlap, rewarding structural and lexical similarity.
- **BoW F1 (0.4112)**: Token-level overlap ignoring order.
  
  <img width="1539" height="588" alt="Screenshot 2025-09-17 121947" src="https://github.com/user-attachments/assets/0e81c179-c085-451b-bcff-05de42c3a13e" />


### Procedure
- Model was run on the **held-out test set (167 dialogues)**.
- Each prediction compared against ground truth with above metrics.
- Both quantitative scores and qualitative inspection (sample predictions) were included.

---






