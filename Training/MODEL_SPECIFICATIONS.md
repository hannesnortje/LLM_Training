# Model Specifications for Web4 Balanced Training

**Date**: 2025-10-27

## Base Model Details

### Current Deployment Model (Ollama)
```
Model: qwen2.5-coder:7b-instruct-q4_K_M
Format: GGUF (Q4_K_M quantization)
Size: ~4.5 GB
Context: 16K tokens
Backend: Ollama
Platform: Mac M1 32GB RAM
```

### Training Source Model (HuggingFace)
```
Model: Qwen/Qwen2.5-Coder-7B-Instruct
Format: PyTorch (FP16/BF16)
Size: ~14 GB (full precision)
Purpose: LoRA adapter training
Backend: MPS (Metal Performance Shaders)
```

## Training Flow

```
1. Download from HuggingFace:
   Qwen/Qwen2.5-Coder-7B-Instruct (full precision)
   ↓
2. Train LoRA Adapter:
   - Dataset: 46,000 samples (~25M tokens)
   - LoRA rank: 16
   - Training time: 10-14 hours on M1
   - Output: adapter_model.bin + adapter_config.json
   ↓
3. Merge LoRA with Base:
   - Combine adapter weights with base model
   - Output: Merged FP16 model
   ↓
4. Convert to GGUF:
   - Use llama.cpp converter
   - Output: model.gguf (unquantized, ~14 GB)
   ↓
5. Quantize to Q4_K_M:
   - Use llama.cpp quantize tool
   - Output: model.Q4_K_M.gguf (~4.5 GB)
   - Matches Ollama format: qwen2.5-coder:7b-instruct-q4_K_M
   ↓
6. Deploy to Ollama:
   - Create Modelfile
   - ollama create web4-agent:latest -f Modelfile
   - Replace existing qwen2.5-coder deployment
```

## Key Commands

### Download Base Model (for training)
```bash
# Using HuggingFace Hub
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    torch_dtype="auto",
    device_map="mps"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
```

### Train LoRA Adapter
```bash
python scripts/train_lora_mps.py \
    --base_model Qwen/Qwen2.5-Coder-7B-Instruct \
    --dataset data/ \
    --lora_r 16 \
    --lora_alpha 32 \
    --output outputs/web4_balanced_lora
```

### Merge and Quantize
```bash
# Merge LoRA adapter
python scripts/merge_lora.py \
    --adapter outputs/web4_balanced_lora \
    --base_model Qwen/Qwen2.5-Coder-7B-Instruct \
    --output outputs/merged_model

# Convert to GGUF
python llama.cpp/convert-hf-to-gguf.py \
    outputs/merged_model \
    --outfile outputs/model.gguf

# Quantize to Q4_K_M
./llama.cpp/quantize \
    outputs/model.gguf \
    outputs/model.Q4_K_M.gguf \
    Q4_K_M
```

### Deploy to Ollama
```bash
# Create Modelfile
cat > Modelfile << 'EOF'
FROM ./outputs/model.Q4_K_M.gguf

PARAMETER temperature 0.0
PARAMETER top_p 0.95
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 16384

SYSTEM """You are a Web4 development expert..."""
EOF

# Create model in Ollama
ollama create web4-agent:latest -f Modelfile

# Test
ollama run web4-agent:latest "Create a PDCA for component creation"
```

## Model Comparison

| Aspect | Training Model | Deployment Model |
|--------|---------------|------------------|
| **Source** | HuggingFace | Ollama |
| **Precision** | FP16/BF16 | Q4_K_M |
| **Size** | ~14 GB | ~4.5 GB |
| **Purpose** | LoRA training | Inference |
| **Speed** | Slow (training) | Fast (inference) |
| **Memory** | ~28 GB (with gradients) | ~6 GB (inference) |
| **Quality** | Full precision | ~99% of full precision |

## Why This Approach Works

1. **Training on Full Precision**: Better gradient flow, more stable training
2. **Quantization After Training**: Preserves training quality, reduces deployment size
3. **Q4_K_M Format**: Optimal balance of size/quality for M1 Mac
4. **Ollama Integration**: Easy deployment, testing, and iteration

## Incremental Training Workflow

### Nightly Update (Evening Training Loop)
```bash
# 1. Train incremental LoRA (2-3 hours)
python scripts/train_lora_mps.py \
    --base_model Qwen/Qwen2.5-Coder-7B-Instruct \
    --resume_from outputs/latest/ \
    --dataset data/incremental_$(date +%Y-%m-%d).jsonl \
    --epochs 1 \
    --learning_rate 1e-4 \
    --output outputs/nightly_$(date +%Y%m%d)

# 2. Merge + Quantize
python scripts/merge_and_quantize.py \
    --adapter outputs/nightly_$(date +%Y%m%d) \
    --base_model Qwen/Qwen2.5-Coder-7B-Instruct \
    --output_format Q4_K_M \
    --output outputs/nightly_$(date +%Y%m%d).gguf

# 3. Update Ollama
ollama create web4-agent:latest -f Modelfile

# 4. Verify
ollama run web4-agent:latest "Test prompt"
```

## Performance Expectations

### Training (M1 Mac 32GB):
- **Dry Run (100 samples)**: 2-3 hours
- **Mini Fine-tune (3,000 samples)**: 3-4 hours
- **Full Training (46,000 samples)**: 10-14 hours
- **Incremental (daily, ~50 samples)**: 2-3 hours

### Inference (M1 Mac):
- **Tokens/second**: ~8-12 tokens/sec
- **Memory usage**: ~6 GB
- **Context length**: 16K tokens
- **Latency (first token)**: ~200ms

## Quality Preservation

| Quantization | Perplexity Loss | Size | Speed Gain |
|--------------|----------------|------|------------|
| FP16 (base) | 0% (baseline) | 14 GB | 1x |
| Q8_0 | ~0.5% | 7.5 GB | 1.5x |
| Q5_K_M | ~1% | 5.5 GB | 2x |
| **Q4_K_M** | **~2%** | **4.5 GB** | **2.5x** |
| Q3_K_M | ~5% | 3.5 GB | 3x |

**Chosen**: Q4_K_M for optimal balance

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-27  
**Model**: qwen2.5-coder:7b-instruct-q4_K_M  
**Status**: Production deployment on Ollama

