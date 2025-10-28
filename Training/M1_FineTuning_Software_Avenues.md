# 🍏 Web4 Training — Software Avenues for Mac M1 (32 GB)

| **Phase** | **Purpose** | **Primary Software / Tools (M1-compatible)** | **Optional / Alternatives** | **Notes** |
|------------|-------------|----------------------------------------------|-----------------------------|------------|
| **1️⃣ Data Preparation & QA** | Authoring, validation, token inspection | • `datasets` (Hugging Face)<br>• `pandas`, `pyarrow`<br>• `jsonschema` (tool-JSON checks)<br>• `jq`, `yq` CLI tools | • `Label Studio` / `Argilla` (manual QA) | Validate JSONL, count tokens, enforce schema consistency. |
| **2️⃣ LoRA Training (fine-tuning)** | Core fine-tuning of base model | • **PyTorch with Metal (MPS)** backend<br>• **transformers** (≥ 4.44)<br>• **peft** (LoRA adapter support)<br>• **trl** (SFTTrainer)<br>• **accelerate** (device mgmt) | • **Unsloth** (experimental faster LoRA on Apple Silicon) | ✅ LoRA only — QLoRA (4-bit) not supported natively on M1. |
| **3️⃣ Checkpoint Management** | Organize, resume, version runs | • `accelerate` checkpoints<br>• `safetensors` format | • Manual folder versioning / `DVC` | Keep adapters under `outputs/<run_name>/lora`. |
| **4️⃣ Merge → GGUF → Quantize** | Create deployable artifacts | • **llama.cpp** tools:<br>  – `convert-hf-to-gguf.py`<br>  – `quantize` | • **llama.cpp finetune** (very small LoRA) | CPU-based; works well on M1. Use Q4_K_M or Q5_K_M. |
| **5️⃣ Serving / Runtime** | Run and test the model | • **Ollama** (macOS native)<br>• **Docker Desktop Models** (Model Runner tab)<br>• `llama.cpp server` (optional HTTP) | • `text-generation-webui` (Python, heavier) | Ollama supports both merged GGUF and `ADAPTER` stacking. |
| **6️⃣ Evaluation & Scoring** | Measure Tool / Style / Guardrail metrics | • `evaluate.py` (custom)<br>• `jsonschema`<br>• **ESLint**, **Prettier**, **TypeScript (tsc)**<br>• **tree-sitter** / **esprima** for AST | • `promptfoo` (visual dashboards) | All work natively; AST & linting are CPU-only. |
| **7️⃣ Visualization & Docs** | Diagrams, notes, dashboards | • **draw.io**, **Mermaid**, **Obsidian/Markdown** | • **MkDocs** / **Docusaurus** | Keep pipeline, eval charts, and reports. |
| **8️⃣ Environment & Orchestration** | Reproducible envs | • **Python 3.10+ venv**<br>• **pip tools** or **poetry** | • **Docker** (for training sandbox) | Stick to Metal-backed PyTorch wheels. |
| **9️⃣ Security / Compliance** | Sanitize data, version control | • `git-secrets`, `trufflehog` | • `syft` (SBOMs if containerizing) | Optional but recommended before publishing. |

---

## ✅ Summary: Recommended Baseline Stack (M1)

| Category | Software |
|-----------|-----------|
| **Language Runtime** | Python 3.10+ |
| **Core Libraries** | PyTorch (MPS), Transformers, PEFT, TRL, Accelerate |
| **Data** | Datasets, pandas, jsonschema |
| **Conversion / Packaging** | llama.cpp |
| **Serving** | Ollama or Docker Desktop Models |
| **Evaluation** | ESLint, Prettier, TypeScript, tree-sitter, jsonschema |
| **Docs & Tracking** | Markdown + draw.io + git |
| **Optional Enhancements** | Unsloth (faster LoRA), promptfoo (eval UI), DVC (data versioning) |

---

### ⚙️ Key Constraints & Notes
- **QLoRA** (4-bit) not yet practical on M1 — LoRA (16-bit fp16/bf16) is the stable path.  
- Use **Metal backend** (`device="mps"`) for acceleration.  
- Quantization is post-training (CPU-friendly); M1 handles **Q4_K_M / Q5_K_M** easily.  
- For larger models or continued LoRA stacking, migrate later to a Linux/CUDA node.  

---

**End of Web4 — M1 Software Stack Overview**
