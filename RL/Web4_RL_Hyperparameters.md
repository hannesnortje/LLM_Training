# ⚙️ Web4 RL Hyperparameter Guide

> Training configuration recommendations for each RL stage

**Version:** 1.0  
**Last Updated:** 2025-10-27  
**Target:** DeepSeek-Coder-6.7B / Qwen2.5-Coder-7B with LoRA

---

## 📋 Table of Contents

1. [Baseline Configuration](#1️⃣-baseline-configuration)
2. [Stage 1: ORPO/DPO](#2️⃣-stage-1-orpo--dpo)
3. [Stage 2: AWR/RS-SFT](#3️⃣-stage-2-awr--rs-sft)
4. [Stage 3: PPO/GRPO](#4️⃣-stage-3-ppo--grpo)
5. [Hardware-Specific Settings](#5️⃣-hardware-specific-settings)
6. [Tuning Strategies](#6️⃣-tuning-strategies)
7. [Monitoring & Adjustment](#7️⃣-monitoring--adjustment)

---

## 1️⃣ Baseline Configuration

### LoRA Settings (All Stages)

```python
lora_config = {
    "r": 16,                    # Rank (try 8, 16, 32)
    "lora_alpha": 32,           # Alpha scaling (typically 2× r)
    "target_modules": [         # Modules to apply LoRA
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj"
    ],
    "lora_dropout": 0.05,       # Dropout (0.05-0.1)
    "bias": "none",             # Bias training (none/all/lora_only)
    "task_type": "CAUSAL_LM"    # Task type
}
```

**Tuning Notes:**
- **Increase r (to 32)** if: model underfitting, have more compute
- **Decrease r (to 8)** if: overfitting, limited compute
- **Alpha = 2×r** is standard, don't change unless experimenting
- **Target modules:** Include all attention + FFN for maximum expressiveness

### Base Training Settings

```python
base_config = {
    "max_seq_length": 4096,           # Context window (2048-8192)
    "gradient_checkpointing": True,   # Enable for memory savings
    "bf16": True,                     # Use BF16 if available
    "fp16": False,                    # Fallback if no BF16
    "tf32": True,                     # Use TF32 on Ampere GPUs
    "dataloader_num_workers": 4,      # Data loading (adjust per system)
    "seed": 42,                       # Random seed for reproducibility
}
```

---

## 2️⃣ Stage 1: ORPO / DPO

### ORPO Configuration (Recommended)

```python
orpo_config = {
    # Training
    "num_train_epochs": 3,
    "per_device_train_batch_size": 1,      # M1 Max: 1, A100: 4-8
    "gradient_accumulation_steps": 16,      # M1: 16-32, GPU: 4-8
    "learning_rate": 5e-6,                  # Conservative for RL
    "lr_scheduler_type": "cosine",
    "warmup_ratio": 0.1,                    # 10% warmup
    "weight_decay": 0.01,
    
    # ORPO-specific
    "beta": 0.1,                            # Odds ratio weight (0.05-0.2)
    "max_length": 4096,
    "max_prompt_length": 2048,
    
    # Optimization
    "optim": "adamw_torch",                 # Or "paged_adamw_8bit" for memory
    "max_grad_norm": 1.0,                   # Gradient clipping
    
    # Logging
    "logging_steps": 10,
    "eval_steps": 50,
    "save_steps": 100,
    "save_total_limit": 3,
}
```

### DPO Configuration (Alternative)

```python
dpo_config = {
    # Training
    "num_train_epochs": 3,
    "per_device_train_batch_size": 1,
    "gradient_accumulation_steps": 16,
    "learning_rate": 5e-6,
    "lr_scheduler_type": "cosine",
    "warmup_ratio": 0.1,
    "weight_decay": 0.01,
    
    # DPO-specific
    "beta": 0.1,                            # KL penalty coefficient (0.01-0.5)
    "max_length": 4096,
    "max_prompt_length": 2048,
    "label_smoothing": 0.0,                 # Usually 0, try 0.1 if overfitting
    
    # Optimization
    "optim": "adamw_torch",
    "max_grad_norm": 1.0,
    
    # Logging
    "logging_steps": 10,
    "eval_steps": 50,
    "save_steps": 100,
}
```

### Tuning Guide: Beta Parameter

| Beta Value | Effect | Use When |
|------------|--------|----------|
| 0.01-0.05 | Weak preference signal | Model already very good, gentle refinement |
| 0.05-0.1 | Moderate (recommended) | Balanced improvement |
| 0.1-0.2 | Strong preference | Model needs significant correction |
| 0.2-0.5 | Very strong | Model far from target behavior |
| >0.5 | Too strong | Risk of instability, not recommended |

**Start with β=0.1, adjust based on validation loss**

### Learning Rate Schedule

```python
# Cosine with warmup (recommended)
total_steps = (num_samples // effective_batch_size) * num_epochs
warmup_steps = int(total_steps * 0.1)

# Example for 1,000 samples, batch=1, grad_accum=16, epochs=3
# total_steps = (1000 // 16) * 3 = 187 steps
# warmup_steps = 18 steps
```

**LR over time:**
- Steps 0-18: Linear warmup from 0 to 5e-6
- Steps 18-187: Cosine decay from 5e-6 to ~0

### Expected Training Time

| Hardware | Batch Config | 500 Pairs | 1,500 Pairs |
|----------|--------------|-----------|-------------|
| M1 Max 64GB | batch=1, accum=16 | 3-4 hours | 8-10 hours |
| RTX 4090 | batch=2, accum=8 | 1.5-2 hours | 4-5 hours |
| A100 40GB | batch=4, accum=4 | 1 hour | 2.5-3 hours |
| A100 80GB | batch=8, accum=2 | 45 mins | 1.5-2 hours |

---

## 3️⃣ Stage 2: AWR / RS-SFT

### Rejection Sampling SFT (RS-SFT)

```python
rssft_config = {
    # Training
    "num_train_epochs": 2,                  # Fewer epochs than Stage 1
    "per_device_train_batch_size": 2,       # Can be larger (only best samples)
    "gradient_accumulation_steps": 8,
    "learning_rate": 3e-6,                  # Lower than Stage 1
    "lr_scheduler_type": "cosine",
    "warmup_ratio": 0.05,                   # Shorter warmup
    "weight_decay": 0.01,
    
    # Sampling
    "num_samples_per_prompt": 4,            # Generate N outputs, keep best
    "temperature": 0.8,                     # Sampling temperature
    "top_p": 0.9,                           # Nucleus sampling
    
    # Filtering
    "reward_threshold": 0.6,                # Only keep samples with reward > 0.6
    "max_samples": 20000,                   # Cap dataset size
    
    # Optimization
    "optim": "adamw_torch",
    "max_grad_norm": 1.0,
    
    # Logging
    "logging_steps": 10,
    "eval_steps": 100,
    "save_steps": 200,
}
```

### Advantage-Weighted Regression (AWR)

```python
awr_config = {
    # Training
    "num_train_epochs": 2,
    "per_device_train_batch_size": 2,
    "gradient_accumulation_steps": 8,
    "learning_rate": 3e-6,
    "lr_scheduler_type": "cosine",
    "warmup_ratio": 0.05,
    "weight_decay": 0.01,
    
    # AWR-specific
    "advantage_beta": 5.0,                  # Advantage scaling (1.0-10.0)
    "normalize_advantage": True,            # Normalize before weighting
    "clip_advantage": 10.0,                 # Max advantage weight
    
    # Sampling
    "num_samples_per_prompt": 8,
    "temperature": 0.8,
    
    # Optimization
    "optim": "adamw_torch",
    "max_grad_norm": 1.0,
    
    # Logging
    "logging_steps": 10,
    "eval_steps": 100,
    "save_steps": 200,
}
```

### Reward Function Weights

```python
reward_weights = {
    "json_valid": 1.0,          # Critical
    "schema_pass": 1.0,          # Critical
    "tool_success": 1.0,         # Critical
    "lint_pass": 1.0,            # Critical
    "ast_correct": 0.5,          # Important but softer
    "guardrail_pass": 2.0,       # Extra important (or -2.0 penalty)
    "verbosity_penalty": -0.1,   # Per extra step
    "off_policy_penalty": -0.5,  # Deviates from expected
}

# Normalize to [0, 1]
max_possible = 6.5  # Sum of positive components
min_possible = -2.5  # If all penalties apply
```

### Tuning Guide: Advantage Beta

| Beta Value | Effect | Use When |
|------------|--------|----------|
| 1.0-3.0 | Weak weighting | Rewards already well-calibrated |
| 3.0-5.0 | Moderate (recommended) | Balanced emphasis on high-reward |
| 5.0-10.0 | Strong weighting | Emphasize best samples heavily |
| >10.0 | Very strong | Risk of overfitting to outliers |

**Start with β=5.0, reduce if overfitting to high-reward samples**

### Expected Training Time

| Hardware | Batch Config | 5K Samples | 20K Samples |
|----------|--------------|------------|-------------|
| M1 Max 64GB | batch=2, accum=8 | 4-6 hours | 12-16 hours |
| RTX 4090 | batch=4, accum=4 | 2-3 hours | 6-8 hours |
| A100 40GB | batch=8, accum=2 | 1-1.5 hours | 3-4 hours |

*Note: Add ~2-4 hours for sample generation and scoring*

---

## 4️⃣ Stage 3: PPO / GRPO

**⚠️ Warning:** PPO is computationally intensive. **Cloud GPU highly recommended.**

### PPO Configuration

```python
ppo_config = {
    # Model
    "learning_rate": 1e-6,                  # Very conservative for PPO
    "batch_size": 16,                       # Episodes per PPO update
    "mini_batch_size": 4,                   # Gradient update batch (M1: 1-2)
    "gradient_accumulation_steps": 4,       # M1: 8-16
    
    # PPO Algorithm
    "ppo_epochs": 4,                        # PPO epochs per batch (4-8)
    "clip_range": 0.2,                      # PPO clip epsilon (0.1-0.3)
    "vf_coef": 0.5,                         # Value function coefficient
    "ent_coef": 0.01,                       # Entropy bonus (0.001-0.1)
    "max_grad_norm": 1.0,                   # Gradient clipping
    
    # KL Penalty
    "kl_penalty": "kl",                     # 'kl' or 'abs'
    "init_kl_coef": 0.05,                   # Initial KL coefficient (0.01-0.1)
    "target_kl": 0.1,                       # Target KL divergence
    "adaptive_kl": True,                    # Adapt KL coef during training
    
    # Episode
    "max_episode_length": 20,               # Max tool calls per episode
    "gamma": 0.99,                          # Discount factor
    "lam": 0.95,                            # GAE lambda
    
    # Training
    "num_episodes": 50000,                  # Total episodes (10K-50K)
    "log_interval": 100,                    # Log every N episodes
    "eval_interval": 1000,                  # Eval every N episodes
    "save_interval": 2000,                  # Save every N episodes
    
    # Optimization
    "optim": "adamw_torch",
    "weight_decay": 0.01,
}
```

### GRPO Configuration (Recommended over PPO)

```python
grpo_config = {
    # Model
    "learning_rate": 1e-6,
    "batch_size": 16,
    "mini_batch_size": 4,
    "gradient_accumulation_steps": 4,
    
    # GRPO Algorithm
    "ppo_epochs": 4,
    "clip_range": 0.2,
    "vf_coef": 0.5,
    "ent_coef": 0.01,
    "max_grad_norm": 1.0,
    
    # GRPO-specific (group relative policy optimization)
    "group_size": 4,                        # Compare within groups of N (2-8)
    "baseline_mode": "group_mean",          # 'group_mean' or 'global_mean'
    
    # KL Penalty
    "init_kl_coef": 0.05,
    "target_kl": 0.1,
    "adaptive_kl": True,
    
    # Episode
    "max_episode_length": 20,
    "gamma": 0.99,
    "lam": 0.95,
    
    # Training
    "num_episodes": 50000,
    "log_interval": 100,
    "eval_interval": 1000,
    "save_interval": 2000,
    
    # Optimization
    "optim": "adamw_torch",
    "weight_decay": 0.01,
}
```

### Reward Function (Simulator)

```python
reward_config = {
    # Task completion
    "task_complete": 10.0,              # Episode succeeds
    "task_failed": -5.0,                # Episode fails
    
    # Per-step rewards
    "correct_tool": 5.0,                # Right tool called
    "wrong_tool": -3.0,                 # Wrong tool called
    "schema_pass": 2.0,                 # Valid parameters
    "schema_fail": -5.0,                # Invalid parameters
    "style_pass": 1.0,                  # Code style correct
    "guardrail_violation": -10.0,       # Safety violation (episode ends)
    
    # Efficiency
    "step_penalty": -0.5,               # Per step (encourages efficiency)
    "redundant_action": -2.0,           # Repeats previous action
    
    # KL penalty
    "kl_weight": 0.05,                  # Applied as: -kl_weight × KL(policy || ref)
}
```

### Tuning Guide: PPO Hyperparameters

| Parameter | Low Value | Recommended | High Value | Effect of Increasing |
|-----------|-----------|-------------|------------|----------------------|
| `learning_rate` | 5e-7 | 1e-6 | 5e-6 | Faster learning but less stable |
| `clip_range` | 0.1 | 0.2 | 0.3 | Larger policy updates per step |
| `ent_coef` | 0.001 | 0.01 | 0.1 | More exploration, less focused |
| `init_kl_coef` | 0.01 | 0.05 | 0.1 | Stronger constraint on drift |
| `ppo_epochs` | 2 | 4 | 8 | More gradient updates per batch |

**Start with recommended values, adjust based on monitoring (Section 7)**

### Expected Training Time

| Hardware | Config | 10K Episodes | 50K Episodes |
|----------|--------|--------------|--------------|
| M1 Max 64GB | batch=16, mini=1, accum=16 | 1.5-2 days | 5-7 days |
| RTX 4090 | batch=16, mini=2, accum=8 | 12-18 hours | 2.5-3.5 days |
| A100 40GB | batch=16, mini=4, accum=4 | 6-10 hours | 1.5-2 days |
| A100 80GB | batch=32, mini=8, accum=2 | 4-6 hours | 1-1.5 days |

**Recommendation:** Use cloud GPU (A100) for Stage 3, or skip this stage if compute-constrained

---

## 5️⃣ Hardware-Specific Settings

### M1 Max 64GB

```python
m1_config = {
    "device": "mps",                        # Metal Performance Shaders
    "bf16": False,                          # Not supported on M1
    "fp16": True,                           # Use FP16
    "per_device_batch_size": 1,             # Conservative
    "gradient_accumulation_steps": 16,      # Compensate for small batch
    "gradient_checkpointing": True,         # Essential for memory
    "optim": "adamw_torch",                 # Standard optimizer
    "dataloader_num_workers": 2,            # M1 benefits from fewer workers
    "max_seq_length": 4096,                 # Can handle 4K context
}
```

**Memory Tips:**
- Use `torch.mps.empty_cache()` between epochs
- Monitor memory with Activity Monitor
- If OOM: reduce `max_seq_length` to 2048 or batch_size to 1

### RTX 4090 / 4080

```python
rtx4090_config = {
    "device": "cuda",
    "bf16": True,                           # Ada Lovelace supports BF16
    "tf32": True,                           # Enable TF32 acceleration
    "per_device_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "gradient_checkpointing": True,
    "optim": "adamw_torch_fused",           # Fused optimizer for Ampere+
    "dataloader_num_workers": 4,
    "max_seq_length": 4096,
}
```

### A100 40GB/80GB

```python
a100_config = {
    "device": "cuda",
    "bf16": True,                           # A100 excellent BF16 support
    "tf32": True,
    "per_device_batch_size": 8,             # 40GB: 4-8, 80GB: 8-16
    "gradient_accumulation_steps": 2,
    "gradient_checkpointing": False,        # May not need with large VRAM
    "optim": "adamw_torch_fused",
    "dataloader_num_workers": 8,
    "max_seq_length": 8192,                 # Can handle longer context
}
```

### Multi-GPU (DDP / FSDP)

```python
multi_gpu_config = {
    "distributed_strategy": "ddp",          # Or "fsdp" for very large models
    "num_processes": 4,                     # Number of GPUs
    "per_device_batch_size": 4,             # Per GPU
    "gradient_accumulation_steps": 1,       # Often not needed with multi-GPU
    "ddp_find_unused_parameters": False,    # Enable if LoRA + frozen layers
    "ddp_bucket_cap_mb": 25,                # Communication optimization
}

# Effective batch size = 4 GPUs × 4 batch × 1 accum = 16
```

---

## 6️⃣ Tuning Strategies

### When Model Underfits (Validation Loss High)

**Symptoms:**
- Training loss decreases slowly
- Validation loss not improving
- Eval metrics below target

**Actions:**
1. **Increase learning rate** (double it: 5e-6 → 1e-5)
2. **Increase LoRA rank** (16 → 32)
3. **Train more epochs** (3 → 5)
4. **Increase model capacity:** more target modules
5. **Check data quality:** Are examples clear and correct?

### When Model Overfits (Validation Loss Increases)

**Symptoms:**
- Training loss decreases but validation loss increases
- Training metrics great but eval metrics poor
- Model memorizing training set

**Actions:**
1. **Reduce learning rate** (5e-6 → 3e-6)
2. **Increase weight decay** (0.01 → 0.05)
3. **Increase dropout** (0.05 → 0.1)
4. **Reduce epochs** (3 → 2)
5. **Get more training data**

### When Training Is Unstable (Loss Spikes)

**Symptoms:**
- Loss increases suddenly
- NaN or Inf losses
- Gradient norms exploding

**Actions:**
1. **Reduce learning rate** (cut in half)
2. **Increase gradient clipping** (1.0 → 0.5)
3. **Reduce batch size** (or increase grad accumulation)
4. **Check for bad data:** corrupted examples
5. **Switch to BF16** if using FP16

### When RL Training Drifts (High KL Divergence)

**Symptoms:**
- KL divergence > 0.2
- Model outputs becoming nonsensical
- Perplexity increasing significantly

**Actions:**
1. **Increase KL penalty** (β: 0.05 → 0.1)
2. **Reduce learning rate** (1e-6 → 5e-7)
3. **Reduce PPO clip range** (0.2 → 0.1)
4. **Rollback to earlier checkpoint**
5. **Add SFT regularization:** Mix in gold examples

### When Reward Hacking Occurs

**Symptoms:**
- Reward increasing but eval metrics failing
- Model exploiting reward function quirks
- Unusual output patterns (very short, very long, repetitive)

**Actions:**
1. **Revise reward function:** add constraints
2. **Add diversity bonus** to reward
3. **Manual inspection** of high-reward samples
4. **Cap reward components:** prevent extreme values
5. **Increase human eval frequency**

---

## 7️⃣ Monitoring & Adjustment

### Key Metrics to Track

**Every Training Step:**
- Loss (should decrease)
- Learning rate (follows schedule)
- Gradient norm (should be <2.0)

**Every 100 Steps:**
- Perplexity (should remain stable 3-15)
- KL divergence (RL only, keep <0.1)
- Reward (RL only, should increase)
- Policy entropy (PPO only, keep >2.0)

**Every Checkpoint (500-1000 Steps):**
- All eval gates (JSON, schema, lint, etc.)
- Validation loss
- Sample outputs (human inspection)

### Healthy Training Patterns

**SFT/ORPO/DPO:**
- Loss decreases smoothly
- Validation tracks training with small gap
- Perplexity stable or slightly decreasing
- Eval metrics gradually improving

**PPO/GRPO:**
- Reward increases (with some noise)
- KL divergence starts low, slowly increases, stabilizes
- Entropy starts high, gradually decreases, stabilizes >2.0
- Episode length decreases (model getting more efficient)

### Warning Signs (See Section 6 for Actions)

| Metric | Warning Sign | Severity |
|--------|--------------|----------|
| Loss | NaN or Inf | 🔴 Critical |
| Loss | Increasing consistently | 🟡 Warning |
| Gradient norm | >5.0 consistently | 🟡 Warning |
| Gradient norm | >10.0 or NaN | 🔴 Critical |
| KL divergence | >0.2 | 🟡 Warning |
| KL divergence | >0.3 | 🔴 Critical |
| Perplexity | >20 or <2 | 🟡 Warning |
| Entropy (PPO) | <1.0 | 🔴 Critical |
| Eval gates | Any regression >5% | 🟡 Warning |

---

## 🔧 Quick Reference: Starting Configs

### For Rapid Experimentation (M1 Max)

```python
quick_config = {
    "per_device_batch_size": 1,
    "gradient_accumulation_steps": 8,       # Smaller for speed
    "num_train_epochs": 1,                  # Single pass
    "learning_rate": 1e-5,                  # Slightly higher
    "eval_steps": 50,
    "save_steps": 100,
    "max_samples": 1000,                    # Small subset
}
```
**Use for:** Testing pipeline, validating data, debugging

### For Production Training (Cloud GPU)

```python
prod_config = {
    "per_device_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "num_train_epochs": 3,
    "learning_rate": 5e-6,
    "eval_steps": 100,
    "save_steps": 200,
    "save_total_limit": 5,                  # Keep top-5 checkpoints
    "load_best_model_at_end": True,
    "metric_for_best_model": "eval_loss",
}
```
**Use for:** Final training runs for deployment

---

## 📚 References & Further Reading

**Papers:**
- **ORPO:** "Odds Ratio Preference Optimization" (2024)
- **DPO:** "Direct Preference Optimization" (Rafailov et al., 2023)
- **PPO:** "Proximal Policy Optimization" (Schulman et al., 2017)
- **GRPO:** "Group Relative Policy Optimization" (2024)
- **LoRA:** "Low-Rank Adaptation of Large Language Models" (Hu et al., 2021)

**Libraries:**
- **TRL (Transformer Reinforcement Learning):** HuggingFace's RL library
- **PEFT:** Parameter-Efficient Fine-Tuning (LoRA, etc.)
- **Accelerate:** Distributed training utilities

**Tools:**
- **Weights & Biases (WandB):** Experiment tracking
- **TensorBoard:** Training visualization
- **DeepSpeed:** Memory-efficient training

---

## 🔄 Version History

- **v1.0 (2025-10-27):** Initial hyperparameter guide

---

**End of Hyperparameter Guide**  
**Version:** 1.0  
**Date:** 2025-10-27

