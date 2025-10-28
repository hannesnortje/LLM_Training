# 🚀 Web4 LoRA Core 10% Phase — Train, Package, Deploy

> This document details the 10% “hands-on” phase of the Web4 LoRA project:  
> **Training → Packaging → Deployment.**  
> It assumes all data, schema, and evaluation groundwork (the 90%) are already complete.  

---

## ⚙️ Overview — The 10% Segment

| **Stage** | **What Happens** | **Primary Tools** | **Output Artifact** |
|------------|------------------|-------------------|----------------------|
| **5️⃣ Training Orchestration** | Fine-tune the base model with your curated dataset via LoRA adapters. | PyTorch (MPS), Transformers, PEFT, TRL, Accelerate | LoRA adapter weights (`adapter_model.bin`, `adapter_config.json`) |
| **6️⃣ Artifact Packaging (Merge → GGUF → Quantize)** | Merge the LoRA adapter with the base model, convert to GGUF, and quantize for fast inference. | llama.cpp tools (`convert-hf-to-gguf.py`, `quantize`) | Quantized `.gguf` model (~4–8 GB) |
| **7️⃣ Deployment & Runtime** | Load the quantized model into Ollama or Docker Desktop Models for local inference and testing. | Ollama, Docker Desktop, llama.cpp | Ready-to-run model responding to prompts |

---

## 🧠 5️⃣ Training Orchestration — “Teaching the Model”

### 🎯 Goal
Infuse the base model (e.g. DeepSeek-Coder 6.7B, Qwen2.5-Coder 7B) with your Web4 framework logic, OOP philosophy, and tool-use intelligence using LoRA adapters.

### 🔩 How It Works
1. Load the base model in **float16 (fp16)** on Metal (MPS).  
2. Attach **LoRA adapters** that train only selected attention heads — lightweight updates.  
3. Run **Supervised Fine-Tuning (SFT)** with your dataset (Tool-Core, Style-Core, Guardrails).  
4. Track training loss to ensure healthy convergence.  
5. Save only adapter deltas at the end.

### 🧰 Tools / Libraries
- **PyTorch (MPS)** for hardware acceleration  
- **Transformers** (≥ 4.44) for model loading  
- **PEFT** for LoRA layers  
- **TRL** for SFT orchestration  
- **Accelerate** for single-device management  

### 🧾 Typical Outputs
```
outputs/
 └── run_2025-10-23/
     ├── adapter_config.json
     ├── adapter_model.bin
     ├── trainer_state.json
     ├── tokenizer.json
     └── logs/loss.csv
```

### ✅ Success Criteria
- Loss stabilizes between **0.6–1.0**  
- Generations return valid JSON tool calls and stylistically correct TypeScript code  
- No MPS OOM (Out-of-Memory) errors during training  

---

## 🧱 6️⃣ Artifact Packaging — “Turning Training Into a Deployable Model”

### 🎯 Goal
Transform the trained LoRA adapter into a single, portable, efficient `.gguf` model file.

### ⚙️ Process
1. **Merge adapters (optional)**  
   Merge LoRA deltas into the base model:  
   ```bash
   peft merge_and_unload
   ```
   Creates a complete `merged_model/` directory.
2. **Convert to GGUF**  
   ```bash
   python3 convert-hf-to-gguf.py merged_model/
   ```  
   Produces `model.gguf` (16–20 GB unquantized).
3. **Quantize for efficiency**  
   ```bash
   ./quantize model.gguf model.Q4_K_M.gguf Q4_K_M
   ```  
   Produces 4–8 GB model with negligible accuracy loss (~1–2%).
4. **Verify integrity**  
   - Run a checksum (`shasum -a 256`)  
   - Compare eval metrics pre- vs post-quantization

### 🧰 Tools
- `llama.cpp` utilities (pure CPU, M1-compatible)  
- Python 3.10+ environment  
- Optionally `safetensors` for archive consistency  

### ✅ Success Criteria
- Quantized `.gguf` loads without error  
- Eval scores drop ≤2% from pre-quantization  
- Disk footprint reduced by ~75%  

---

## 🚀 7️⃣ Deployment & Runtime — “Making It Usable”

### 🎯 Goal
Serve your trained and quantized model locally for interactive use, testing, or further evaluation.

### ⚙️ Deployment Paths

#### 🟩 **Option A: Ollama (Recommended on M1)**
1. Create a `Modelfile`:
   ```text
   FROM ./model.Q4_K_M.gguf
   PARAMETER temperature 0
   TEMPLATE """{{ .System }}\n{{ .Prompt }}"""
   ```
2. Register and run:
   ```bash
   ollama create web4-lora -f Modelfile
   ollama run web4-lora
   ```
3. Test tool-use, code style, and guardrails.

#### 🟦 **Option B: Docker Desktop Models**
1. Open Docker Desktop → **Models** → “Add Model”  
2. Import your `.gguf` file  
3. Assign metadata (name, version, description)  
4. Launch local API endpoint for apps to connect  

### 🧪 Post-Deployment Tests

| **Test Type** | **Expected Result** |
|----------------|--------------------|
| Tool-JSON prompt | Returns valid `{ "tool": "...", "args": { ... } }` |
| Style prompt | Generates TypeScript in correct house format |
| Guardrail prompt | Proper `<REFUSAL>` response when required |
| Latency | ~1 token/sec for 7B Q4 model on M1 |
| Memory footprint | ~22–26 GB shared memory used |

---

## 📦 Deliverables After the 10% Phase

| **Artifact** | **Description** |
|---------------|----------------|
| `adapter_model.bin` | LoRA weights (training result) |
| `merged_model.gguf` | Merged unquantized model |
| `model.Q4_K_M.gguf` | Quantized deployable model |
| `Modelfile` | Ollama runtime configuration |
| `eval_log.md` | Post-training metrics summary |
| `drawio_diagram.png` | Final pipeline visualization |

---

## 💡 Why This 10% Matters

- Converts **weeks of data work** into a *real, usable AI model*  
- Establishes a **repeatable training loop**: data → LoRA → GGUF → deploy  
- Keeps everything **local, secure, and verifiable** — essential for Web4 governance principles  
- Enables **incremental re-training** (fine-tune only new adapters, not the full base model)

---

## 🧭 Recap

| **Step** | **Goal** | **Tools** | **Outcome** |
|-----------|-----------|------------|--------------|
| **Train** | Teach Web4 philosophy via LoRA | PEFT + TRL on MPS | Adapter weights |
| **Package** | Merge + Quantize for performance | llama.cpp scripts | `.gguf` model |
| **Deploy** | Serve locally in Ollama or Docker | Ollama / Docker | Interactive local AI model |

---

**End of Web4 LoRA Core 10% Phase — Train, Package, Deploy**
