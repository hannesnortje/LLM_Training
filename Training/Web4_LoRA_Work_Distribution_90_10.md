# 🧭 Web4 LoRA Project — Work Distribution (90% / 10% Framework)

> 💡 *90% of the work is planning, data, validation, and evaluation.*  
> *10% is the actual training and serving — the part that looks like “AI”.*  

This gives you a clear management and progress-tracking overview.

---

| **Phase** | **Focus Area** | **Main Tasks** | **Approx. Share** | **Difficulty** | **Expected Outcome** |
|------------|----------------|----------------|-------------------|----------------|----------------------|
| **1️⃣ Data Foundation** | Dataset Design & Quality | - Define JSONL schemas (Tool-Core, Style, Guardrail)<br>- Validate every line (`jsonschema`, `jq`)<br>- Balance positive & negative examples<br>- Token count analysis (max seq length) | **25%** | Easy → Moderate | Clean, schema-valid dataset; ready for LoRA training |
| **2️⃣ Template Governance** | Prompt & Format Consistency | - Define canonical chat template<br>- Align train / eval / serve formats<br>- Freeze system + user roles<br>- Document exact examples | **10%** | Moderate | Stable and deterministic prompt alignment |
| **3️⃣ Evaluation Infrastructure** | Metrics & Benchmarks | - Build `evaluate.py` harness<br>- JSON validation, schema checks<br>- AST/lint scoring for code style<br>- Guardrail refusal tests | **20%** | Moderate → Hard | Repeatable quantitative evaluation of model quality |
| **4️⃣ Data QA Loop** | Continuous Curation | - Iterate dataset improvements<br>- Add counterexamples (Tool-Neg)<br>- Refine guardrails<br>- Track token growth vs results | **15%** | Moderate | Ongoing dataset refinement; reduced overfit and bias |
| **5️⃣ Training Orchestration** | LoRA Configuration & Run | - Configure TRL+PEFT on MPS<br>- Tune LR, batch size, epochs<br>- Run dry test (100 samples)<br>- Run full fine-tune (25–35k samples) | **5%** | Moderate | Stable adapter model trained on M1 |
| **6️⃣ Artifact Packaging** | Merge & Quantize | - Merge LoRA with base HF model<br>- Convert to GGUF<br>- Quantize (Q4_K_M / Q5_K_M)<br>- Validate checksum | **2%** | Easy | Compact `.gguf` artifact ready for serving |
| **7️⃣ Deployment & Runtime** | Serving & Testing | - Create Ollama Modelfile<br>- Load model locally<br>- Run smoke tests with Eval set<br>- Optionally package in Docker Desktop Models | **3%** | Easy | Locally deployable, quantized model responding correctly |
| **8️⃣ Documentation & Reporting** | Knowledge Capture | - Maintain Markdown logs<br>- Diagram full pipeline (draw.io)<br>- Record eval metrics over time<br>- Write model card summary | **10%** | Easy | Transparent, reproducible documentation |
| **9️⃣ Continuous Improvement** | Governance & Scaling | - Add CI linting<br>- Automate eval & timing<br>- Plan migration to Linux/CUDA (optional)<br>- Improve eval metrics over versions | **10%** | Moderate | Sustainable, repeatable training process |

---

## 🧮 Effort Split Overview

| **Category** | **What it covers** | **Effort Share** | **Purpose** |
|---------------|--------------------|------------------|--------------|
| **90% — Planning, Data, Evaluation, Documentation** | Phases 1–4, 8–9 | **≈90% of total effort** | Build quality foundation and trust in results. |
| **10% — Training, Conversion, Serving** | Phases 5–7 | **≈10% of total effort** | Run the model fine-tuning and deploy the artifact. |

---

## 🧩 Summary

- **Data and evaluation dominate the workload** — you’re teaching the model your worldview, not writing ML code.  
- **Training and serving are quick once inputs and metrics are correct.**  
- The most *intellectual* part is designing *what correctness means* — the evaluation harness.  
- The most *mechanical* part is running `trl.train()`, `llama.cpp quantize`, and `ollama create`.  

This distribution ensures your LoRA fine-tuning pipeline is **accurate, reproducible, and efficient** on a single Mac M1.

---

**End of Web4 LoRA Project — Work Distribution (90% / 10% Framework)**
