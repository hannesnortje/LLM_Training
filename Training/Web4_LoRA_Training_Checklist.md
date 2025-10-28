# 🧠 Web4 LoRA / QLoRA Training Pipeline Checklist (Mac M1)

This checklist walks you through **safe, stepwise fine-tuning** of Web4 models (e.g. Qwen 2.5 Coder 7B or DeepSeek-Coder 6.7B) using your curated dataset.

---

## 🧭 Overview

You’ll validate training in **four progressive passes**:

| Stage | Name | Goal | Duration | Risk |
|--------|------|------|-----------|------|
| 1️⃣ | Dataset Sanity Check | Ensure JSONL format and tokenization OK | Minutes | Low |
| 2️⃣ | Dry Run / Overfit Test | Verify training loop and memory footprint | < 1h | Low |
| 3️⃣ | Mini Fine-Tune | Check that model learns your structure | 3–4h | Medium |
| 4️⃣ | Full LoRA Training | Train all data for production adapter | 12–20h | Medium–High |

---

## 1️⃣ Dataset Sanity Check

**Goal:** Confirm data integrity before any training.

✅ Checklist:
- [ ] All files are valid JSONL (1 object per line).  
- [ ] Fields: `task_type`, `instruction`, `input`, `output` exist.  
- [ ] Average tokens per record reasonable (< 2048).  
- [ ] Data loads with no parsing errors.  
- [ ] Tokenizer (Qwen/DeepSeek) encodes and decodes samples without errors.  
- [ ] Random sample inspection confirms format consistency.  

📊 Expectation: ~25k–40k samples, 15–30M tokens total.

---

## 2️⃣ Dry Run / Overfit Test (100 samples)

**Goal:** Validate training loop + MPS memory behavior.

✅ Checklist:
- [ ] Create subset of ~100 mixed samples across buckets.  
- [ ] Run 1 epoch with batch size 1, seq len 512.  
- [ ] Verify loss decreases from ~3–5 → <1 within few hundred steps.  
- [ ] Confirm no NaNs, no CUDA/MPS errors.  
- [ ] GPU memory stable (< 12 GB on M1 32GB).  

📊 Outcome: Model can overfit tiny set — confirms pipeline works.

---

## 3️⃣ Mini Fine-Tune (2k–3k samples)

**Goal:** Verify learning of tool-calling + coding style.

✅ Checklist:
- [ ] Use ~2k samples (balanced across Tool, Style, Guardrail).  
- [ ] Train 1 epoch, batch size 1, grad accumulation 8–12.  
- [ ] Observe loss curve stable (~1.0–1.5 range).  
- [ ] Generate 10 tool prompts → outputs valid JSON.  
- [ ] Generate 10 style prompts → matches Web4 code style.  
- [ ] Run `evaluate.py` → Tool ≥ 80%, Style ≥ 85%, Guardrail ≥ 95%.  

📊 Expectation: Confirm model internalizes structure and schema.

---

## 4️⃣ Full LoRA Training (25k–40k samples)

**Goal:** Train on full dataset for production-quality adapter.

✅ Checklist:
- [ ] All buckets included.  
- [ ] LoRA params: r=8, alpha=16, dropout=0.05.  
- [ ] Batch size 1, grad accumulation 12–16, seq len 2048.  
- [ ] Run for 1–2 epochs.  
- [ ] Monitor loss → plateaus between 0.6–1.0.  
- [ ] Save adapter (`outputs/<run_name>/lora`).  

📊 Expectation: Stable, clean adapter; no divergence.

---

## 5️⃣ Evaluation (Post-Training)

**Goal:** Quantify performance on hold-out Eval set.

✅ Checklist:
- [ ] Run `evaluate.py` on all `data/eval/*.jsonl`.  
- [ ] Tool Eval: JSON validity ≥ 95%, Correct Tool ≥ 85%.  
- [ ] Style Eval: Lint pass 100%, AST match ≥ 90%.  
- [ ] Guardrail Eval: Refusal accuracy ≥ 98%.  
- [ ] Mixed Eval ≥ 90% overall.  
- [ ] Log scores to `eval_log.md` or CSV.  

📊 Expectation: High accuracy and no format regressions.

---

## 6️⃣ Merge + Quantize

**Goal:** Create deployable artifact (GGUF or adapter).

✅ Checklist:
- [ ] Merge LoRA → HF model (`merge_and_unload`).  
- [ ] Convert to GGUF via llama.cpp script.  
- [ ] Quantize (Q4_K_M or Q5_K_M).  
- [ ] Verify same Eval results post-quantization.  

📊 Expectation: Identical or ±1% metric difference.

---

## 7️⃣ Deployment

**Goal:** Use trained model in Ollama or Docker Desktop Models.

✅ Checklist:
- [ ] Create `Modelfile` referencing your GGUF.  
- [ ] `ollama create web4-coder -f Modelfile` succeeds.  
- [ ] `ollama run web4-coder` emits proper structured responses.  
- [ ] Optionally import GGUF in Docker Desktop’s “Models” tab.  

📊 Expectation: Inference identical to evaluation runs.

---

## 8️⃣ Iteration & Improvement

| If this happens | Action |
|------------------|---------|
| Loss stagnates | Increase epochs or lower LR |
| Emits prose for tool JSON | Add Tool-Neg examples |
| Naming drift | Add more Style-Core examples |
| Refusal inconsistency | Add Guardrail samples |
| Eval score plateaus | Run extra mini fine-tune with smaller LR |

---

## ✅ Summary Table

| Stage | Purpose | Success Indicator |
|--------|----------|------------------|
| Sanity Check | Data valid, tokenizable | No JSON errors |
| Dry Run | Loop functional | Loss drops quickly |
| Mini Fine-Tune | Learning structure | JSON/code quality visible |
| Full Training | Production adapter | Low loss, stable metrics |
| Eval | Verify accuracy | ≥90–95% scores |
| Merge & Quantize | Artifact build | GGUF validated |
| Deploy | Real usage | Ollama responds correctly |

---

**End of Web4 Training Pipeline Checklist**
