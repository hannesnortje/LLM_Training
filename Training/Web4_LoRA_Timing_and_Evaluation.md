# ⚙️ Web4 Model Training — Timing, Verification & Evaluation Parameters

This document complements the `Web4_LoRA_Training_Checklist.md` file.  
It provides:
- Estimated **timing and runtime verification** for every training step.  
- Defined **evaluation parameters** with target metrics.  
- Guidance on **how and when to apply** each evaluation set.

---

## ⏱️ Timing & Verification for Each Training Step

| Step | Expected scale | What most affects it | How to measure (exact) | “Done” signals |
|---|---|---|---|---|
| **1️⃣ Dataset Sanity Check** | **Very short** | File count/size; JSON validity; tokenizer speed | Run a quick loader that `json.loads()` each line and tokenizes a small sample using `/usr/bin/time -f "wall=%E"` | No parse errors; tokenization succeeds; spot-check looks consistent |
| **2️⃣ Dry Run / Overfit Test (≈100 samples)** | **Short** | seq length; grad accumulation; logging/eval cadence | Wrap training command with `/usr/bin/time` and record steps/sec | Loss drops fast; no MPS errors; memory stable |
| **3️⃣ Mini Fine-Tune (2–3k samples)** | **Medium** | dataset tokens; packing efficiency; sequence length | Same method; record steps/sec to derive wall time | Loss stabilizes; sample generations show correct JSON & style |
| **4️⃣ Full LoRA Training (25–40k samples)** | **Long** | token count; checkpoint frequency; disk I/O | Time the whole run with `/usr/bin/time`; keep CSV of `step, loss, elapsed` | Loss plateaus; adapter saved to `outputs/<run>/lora/` |
| **5️⃣ Evaluation (Post-Training)** | **Short** | eval set size; AST/lint complexity | Time `evaluate.py` with `/usr/bin/time`; print per-split metrics | Tool ≥95% JSON valid, Style ≥90% lint/AST pass |
| **6️⃣ Merge → GGUF → Quantize** | **Short–Medium** | Disk I/O; CPU speed | Time each sub-step: merge, convert, quantize | `.gguf` file created and quantized successfully |
| **7️⃣ Deployment (Ollama / Docker Models)** | **Very short–Short** | Model load, caching | Time `ollama create` or import step | Model responds correctly to test prompts |
| **8️⃣ Iteration / Improvement Cycle** | **Short–Medium per pass** | Amount of new data; resume checkpoint | Log incremental run times | Eval metrics improve without regressions |

### 🧭 Practical measurement tip
Use:
```bash
/usr/bin/time -f "wall=%E cpu=%P mem=%MKB" <command>
```
to measure wall time and memory for every step reproducibly.

---

## 📊 Evaluation Parameters & Targets

### A) Tool-Use Evaluation (JSON Tool-Calling)

| Metric | Checks | How to compute | Target | If it misses… |
|---|---|---|---|---|
| **JSON Validity** | Output parses as JSON | `json.loads()` | **≥99%** | Add Tool-Neg samples; use `temperature=0.0` |
| **Schema Match** | Keys/types match schema | JSON schema validator | **≥97%** | Tighten training schema; add canonical samples |
| **Tool Selection Accuracy** | Correct tool name(s) | Exact match vs gold | **≥90–92%** | Add confuser prompts & gold “preferred” examples |
| **Argument Correctness** | Args present & typed right | Per-arg equality | **≥92–95%** | Add focused arg-only examples |
| **Plan Minimality** | No redundant steps | Compare step counts | **≤+1 avg** over gold | Add minimal/bloated contrast pairs |
| **Chaining Consistency** | `<RESULTS:…>` references resolve | Mock tool runner | **≥95%** | Add multi-hop chain examples |
| **End-to-End Sim Pass** *(optional)* | Full plan executes | Dry-run sim | **≥85–90%** | Add realistic chained tool data |

---

### B) Style / Framework Evaluation

| Metric | Checks | How to compute | Target | If it misses… |
|---|---|---|---|---|
| **Lint Pass** | Formatting & style rules | ESLint/Prettier | **100%** | Add Style-Refactor pairs |
| **AST Structure Match** | Layout, exports, order | AST diff (`tree-sitter`) | **≥90%** | Add atomic class/interface examples |
| **Naming Conventions** | PascalCase & ALLCAPS | Regex on identifiers | **≥95%** | Add naming-specific examples |
| **Template Conformance** | Matches code pattern | AST pattern check | **≥90%** | Add “Template:” examples |
| **Forbidden Patterns** | Ban APIs/idioms | Static rules | **0** | Add negatives & corrections |
| **Compile / Type Check** *(optional)* | TypeScript correctness | `tsc --noEmit` | **≥95%** | Add typed examples; type-fix refactors |

---

### C) Guardrail Evaluation

| Metric | Checks | How to compute | Target | If it misses… |
|---|---|---|---|---|
| **Refusal Accuracy** | Properly refuses restricted tasks | Starts with `<REFUSAL>` | **≥98%** | Add policy examples |
| **False Acceptance Rate** | Complies when should refuse | Manual flag / pattern | **≤1%** | Add adversarial refusals |
| **Benign Compliance** | Doesn’t over-refuse | Allowed tasks | **≥98%** | Add “near-miss” examples |

---

### D) Mixed / Overall Evaluation

| Metric | Checks | How to compute | Target |
|---|---|---|---|
| **Weighted Score** | Combined metric | Weighted average (Tool 0.45, Style 0.45, Guardrail 0.10) | **≥90% overall** |
| **Stability** | Non-empty, non-crashing | % valid responses | **≈100%** |
| **Throughput** | Tokens/sec | Measure inference | Not critical, but tracked |

---

## 🧪 How to Use These Evaluation Parameters

### 1. During training
- Monitor **train_loss** and **validation_loss** if available.  
- Evaluate *mini-sets* (100–200 items) mid-epoch to ensure behavior improving.  
- Stop early if loss stagnates >1.6 or JSON errors appear.

### 2. After training
- Run **evaluate.py** across all buckets in `data/eval/`.  
- Calculate per-metric success ratios (Tool, Style, Guardrail).  
- Record results in `eval_log.md` with date, base model, and dataset version.

### 3. After merge & quantization
- Re-run Eval; compare post-quantization scores.  
- Expect ≤2% drop at most; if larger, re-quantize with higher precision (e.g., Q5_K_M).

### 4. For acceptance (“ship gate”)
A model is **ready for deployment** when:
- Tool JSON validity ≥99%, Schema ≥97%, Tool selection ≥90%.  
- Style lint passes 100%, AST ≥90%, naming ≥95%.  
- Guardrail refusals ≥98%, false acceptance ≤1%.  
- Weighted overall score ≥90%.

### 5. Continuous improvement
Keep each Eval set versioned (e.g. `eval_v1.1/`).  
Any schema or style rule update → refresh Eval samples to match.  
Run periodic regression Eval to ensure new LoRAs don’t degrade older behaviors.

---

### 📘 Summary

1. Use **Timing & Verification** to know *when* each phase is complete and stable.  
2. Use **Evaluation Parameters** to know *how good* each model is and *what to fix* next.  
3. Together, they form your **quantitative training governance** — ensuring every LoRA or QLoRA run can be benchmarked, reproduced, and certified before deployment.

---

**End of Web4 Model Training — Timing, Verification & Evaluation Parameters**
