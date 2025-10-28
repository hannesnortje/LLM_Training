# ✅ Web4 RL Implementation Checklist

> Pre-flight validation and setup checklist for RL training stages

**Version:** 1.0  
**Last Updated:** 2025-10-27  
**Purpose:** Ensure all prerequisites are met before starting each RL stage

---

## 📋 Table of Contents

1. [General Prerequisites](#1️⃣-general-prerequisites-all-stages)
2. [Stage 1: ORPO/DPO Checklist](#2️⃣-stage-1-orpo--dpo-checklist)
3. [Stage 2: AWR/RS-SFT Checklist](#3️⃣-stage-2-awr--rs-sft-checklist)
4. [Stage 3: PPO/GRPO Checklist](#4️⃣-stage-3-ppo--grpo-checklist)
5. [Stage 4: Deployment Checklist](#5️⃣-stage-4-deployment-checklist)

---

## 1️⃣ General Prerequisites (All Stages)

### Hardware & Environment

- [ ] **Hardware confirmed:**
  - [ ] M1 Max with ≥64GB RAM (Stages 1-2) **OR**
  - [ ] Cloud GPU (RTX 4090/A100) for Stage 3
  - [ ] Storage: ≥100GB free for checkpoints and logs

- [ ] **Software installed:**
  - [ ] Python 3.9+ with venv or conda
  - [ ] PyTorch 2.0+ with appropriate backend (MPS for M1, CUDA for GPU)
  - [ ] Transformers library (≥4.35)
  - [ ] PEFT library for LoRA
  - [ ] TRL library for RL algorithms
  - [ ] Accelerate for distributed training

- [ ] **Dependencies installed:**
  ```bash
  pip install torch transformers peft trl accelerate datasets
  pip install wandb tensorboard  # For logging
  pip install jsonschema eslint  # For eval gates
  ```

- [ ] **Environment variables set:**
  ```bash
  export WANDB_API_KEY="..."     # If using Weights & Biases
  export CUDA_VISIBLE_DEVICES="0"  # If using specific GPU
  export PYTORCH_MPS_HIGH_WATERMARK_RATIO="0.0"  # M1 memory optimization
  ```

### Data & Models

- [ ] **Base model downloaded:**
  - [ ] DeepSeek-Coder-6.7B **OR**
  - [ ] Qwen2.5-Coder-7B
  - [ ] Model format verified (safetensors, GGUF, etc.)
  - [ ] Quantization tested (4-bit loading works)

- [ ] **SFT baseline available:**
  - [ ] `SFT.lora` adapter from Stage 0 (Core10Phase training)
  - [ ] SFT eval metrics recorded as baseline
  - [ ] Checkpoint can be loaded successfully

- [ ] **Evaluation harness ready:**
  - [ ] JSON validator script
  - [ ] Schema validator (jsonschema)
  - [ ] ESLint for code validation
  - [ ] AST parser (TypeScript)
  - [ ] Guardrail checker
  - [ ] Eval script runs on 100 test samples in <5 minutes

### Infrastructure

- [ ] **Monitoring setup:**
  - [ ] Weights & Biases project created **OR**
  - [ ] TensorBoard configured
  - [ ] Logging directories created (`./logs`, `./checkpoints`)

- [ ] **Version control:**
  - [ ] Git repository initialized
  - [ ] `.gitignore` excludes checkpoints, logs, data
  - [ ] Branch created for RL experiments (e.g., `rl-stage1`)

- [ ] **Backup strategy:**
  - [ ] Checkpoint auto-save configured (every 100-500 steps)
  - [ ] Backup location determined (external drive, cloud storage)
  - [ ] Rollback procedure documented and tested

### Documentation

- [ ] **Read all supplementary docs:**
  - [ ] [Web4_LoRA_RL_AddOn_Plan.md](./Web4_LoRA_RL_AddOn_Plan.md)
  - [ ] [Web4_RL_Annotation_Guidelines.md](./Web4_RL_Annotation_Guidelines.md)
  - [ ] [Web4_RL_Hyperparameters.md](./Web4_RL_Hyperparameters.md)
  - [ ] [Web4_RL_Simulator_Design.md](./Web4_RL_Simulator_Design.md) (if doing Stage 3)

- [ ] **Training logs prepared:**
  - [ ] Template for recording decisions
  - [ ] Template for eval results
  - [ ] Template for debugging notes

---

## 2️⃣ Stage 1: ORPO / DPO Checklist

### Before Starting

- [ ] **Dataset preparation:**
  - [ ] 500-1,500 diverse prompts selected from eval set
  - [ ] Coverage verified: 40% tool-use, 30% style, 20% multi-step, 10% guardrails
  - [ ] Prompts span all tool categories

- [ ] **Output generation:**
  - [ ] SFT model loaded successfully
  - [ ] Generated 3-5 outputs per prompt with varying temperatures (0.7, 0.9, 1.1)
  - [ ] Outputs stored in structured format (JSONL)
  - [ ] Output quality spot-checked (no degenerate samples)

- [ ] **Annotation infrastructure:**
  - [ ] Annotation interface ready (Streamlit, Flask, or Google Forms)
  - [ ] Interface tested with 5 practice examples
  - [ ] Interface saves data in correct format (JSONL with required fields)

- [ ] **Annotator training:**
  - [ ] Annotators read [Annotation Guidelines](./Web4_RL_Annotation_Guidelines.md)
  - [ ] Annotators completed 10 practice examples
  - [ ] Inter-annotator agreement tested on 20 overlapping pairs
  - [ ] Cohen's κ ≥ 0.7 achieved (or training repeated)

### During Annotation

- [ ] **Quality monitoring:**
  - [ ] Random 10% of annotations checked daily
  - [ ] Annotation speed tracked (target: 1 min per comparison)
  - [ ] Tag distribution monitored (matches expected distribution)
  - [ ] Ambiguous cases flagged for review

- [ ] **Progress tracking:**
  - [ ] Target: 500 minimum, 1,500 optimal pairs
  - [ ] Current count: _____ pairs annotated
  - [ ] Estimated completion date: _______

### Before Training

- [ ] **Data validation:**
  - [ ] Preference dataset loaded successfully
  - [ ] No corrupted or malformed entries
  - [ ] Train/val/test split created (80/10/10)
  - [ ] Category balance verified (roughly equal tool/style/guardrail)

- [ ] **Hyperparameters configured:**
  - [ ] Config file created from [Hyperparameter Guide](./Web4_RL_Hyperparameters.md)
  - [ ] Learning rate: 5e-6 (or adjusted per hardware)
  - [ ] Beta parameter: 0.1
  - [ ] Batch size and gradient accumulation set for hardware
  - [ ] Logging and checkpointing intervals configured

- [ ] **Training script tested:**
  - [ ] Dry run on 10 samples completes without errors
  - [ ] Memory usage acceptable (<90% of available)
  - [ ] Checkpoint saving works
  - [ ] Logging appears in WandB/TensorBoard

### During Training

- [ ] **Monitor metrics:**
  - [ ] Loss decreasing smoothly
  - [ ] Gradient norms in healthy range (0.1-2.0)
  - [ ] Perplexity stable (3-15)
  - [ ] No NaN or Inf values

- [ ] **Checkpoints:**
  - [ ] Checkpoints saved every 100 steps
  - [ ] Disk space monitored (checkpoints can be large)
  - [ ] Top-3 checkpoints retained by validation loss

- [ ] **Eval gates:**
  - [ ] Run eval every 200-500 steps
  - [ ] JSON validity, schema compliance tracked
  - [ ] Compare to SFT baseline
  - [ ] Human spot-check 10 random outputs per eval

### After Training

- [ ] **Evaluation:**
  - [ ] Full eval on 2,000 sample eval set
  - [ ] All metrics recorded in eval report
  - [ ] Human evaluation on 100 random samples
  - [ ] Preference win-rate vs SFT ≥ 65%?

- [ ] **Success criteria met:**
  - [ ] JSON validity ≥ 99% (+2% vs SFT)
  - [ ] Schema compliance ≥ 97% (+2%)
  - [ ] Lint pass = 100% (+2%)
  - [ ] Guardrail violations ≤ 1% (-1%)
  - [ ] No catastrophic regressions

- [ ] **Deliverables:**
  - [ ] `ORPO_v1.lora` saved and backed up
  - [ ] Preference dataset saved: `preference_pairs_v1.jsonl`
  - [ ] Eval report written: `stage1_eval_report.md`
  - [ ] Training log documented with key decisions
  - [ ] Best checkpoint tagged in git

- [ ] **Decision:**
  - [ ] Proceed to Stage 2? (Yes if metrics pass)
  - [ ] Iterate on Stage 1? (Yes if metrics regress)
  - [ ] Deploy Stage 1? (Yes if meets goals)

---

## 3️⃣ Stage 2: AWR / RS-SFT Checklist

### Before Starting

- [ ] **Stage 1 complete:**
  - [ ] `ORPO.lora` available **OR** fallback to `SFT.lora`
  - [ ] Stage 1 eval metrics recorded as baseline

- [ ] **Reward function implemented:**
  - [ ] JSON validator (returns 1.0 or 0.0)
  - [ ] Schema validator (returns 1.0 or 0.0)
  - [ ] Mock tool executor (returns 1.0 or 0.0)
  - [ ] ESLint checker (returns 1.0 or 0.0)
  - [ ] AST validator (returns 0.5 or 0.0)
  - [ ] Guardrail checker (returns -2.0 if violated)
  - [ ] Verbosity penalty (-0.1 per extra step)
  - [ ] Reward normalization to [0, 1]

- [ ] **Reward function tested:**
  - [ ] Test on 100 known good/bad examples
  - [ ] Reward distribution looks reasonable (mean ~0.6-0.7)
  - [ ] No exploitable edge cases found
  - [ ] Logging captures all reward components

- [ ] **Data generation:**
  - [ ] 5,000-20,000 diverse prompts selected
  - [ ] Coverage spans all task types
  - [ ] Prompts include some challenging examples

### During Data Generation

- [ ] **Sample generation:**
  - [ ] Generate 4-8 outputs per prompt
  - [ ] Use temperature sampling: 0.6, 0.8, 1.0, 1.2
  - [ ] Outputs stored with metadata (prompt, temperature, etc.)
  - [ ] Generation doesn't hang or crash

- [ ] **Scoring:**
  - [ ] All outputs scored with reward function
  - [ ] Scores logged with breakdown of components
  - [ ] Reward distribution analyzed:
    - [ ] Mean reward: _____ (target: 0.6-0.7)
    - [ ] Std dev: _____ (target: 0.1-0.2)
    - [ ] Samples with reward > 0.8: _____%
    - [ ] Samples with reward < 0.3: _____%

- [ ] **Quality checks:**
  - [ ] Human inspection of 20 high-reward samples (reward hacking?)
  - [ ] Human inspection of 20 low-reward samples (reasonable?)
  - [ ] Spot-check reward component consistency

### Before Training

- [ ] **Method selection:**
  - [ ] **RS-SFT** (simpler, M1-friendly) **OR**
  - [ ] **AWR** (better sample efficiency) **OR**
  - [ ] **RLAIF** (hybrid with preferences)

- [ ] **Dataset construction:**
  - [ ] For RS-SFT: Keep only top-1 per prompt, filter by threshold (≥0.6)
  - [ ] For AWR: Compute advantages, normalize, clip to [-10, 10]
  - [ ] Final dataset size: _____ samples (target: 5K-20K)
  - [ ] Train/val/test split created

- [ ] **Hyperparameters configured:**
  - [ ] Config from [Hyperparameter Guide](./Web4_RL_Hyperparameters.md)
  - [ ] Learning rate: 3e-6 (lower than Stage 1)
  - [ ] Epochs: 2
  - [ ] Advantage beta (AWR): 5.0
  - [ ] Batch size and gradient accumulation

- [ ] **Training script tested:**
  - [ ] Dry run on 100 samples
  - [ ] Memory usage acceptable
  - [ ] Weighted loss computed correctly (if AWR)

### During Training

- [ ] **Monitor metrics:**
  - [ ] Loss decreasing
  - [ ] Average reward on val set increasing
  - [ ] Perplexity not increasing significantly
  - [ ] Gradient norms stable

- [ ] **Distribution monitoring:**
  - [ ] Vocab diversity ≥ 80% of baseline
  - [ ] N-gram overlap (BLEU self-similarity) < 0.5
  - [ ] Output length within ±20% of baseline

- [ ] **Reward hacking checks:**
  - [ ] Sample 10 high-reward outputs per 500 steps
  - [ ] Human review: are they genuinely good?
  - [ ] Look for: extremely short, repetitive, exploits

### After Training

- [ ] **Evaluation:**
  - [ ] Full eval on 2,000 samples
  - [ ] Compare reward distribution: Stage 2 vs Stage 1
  - [ ] Check all eval gates

- [ ] **Success criteria met:**
  - [ ] JSON validity ≥ 99% (maintain)
  - [ ] Schema compliance ≥ 98% (+1%)
  - [ ] Tool success rate ≥ 95%
  - [ ] Plan minimality: avg steps reduced 10-20%
  - [ ] No distribution collapse

- [ ] **Deliverables:**
  - [ ] `AWR_v1.lora` (or `RSSFT_v1.lora`)
  - [ ] Scored dataset: `scored_outputs_v1.jsonl`
  - [ ] Reward logs: `reward_traces_v1.csv`
  - [ ] Eval report: `stage2_eval_report.md`

- [ ] **Decision:**
  - [ ] Proceed to Stage 3? (optional, if compute available)
  - [ ] Deploy Stage 2? (if meets goals)
  - [ ] Iterate? (if reward hacking or collapse detected)

---

## 4️⃣ Stage 3: PPO / GRPO Checklist

**⚠️ Note:** This stage is optional and computationally intensive. Cloud GPU highly recommended.

### Before Starting

- [ ] **Feasibility check:**
  - [ ] Cloud GPU available (A100 recommended) **OR**
  - [ ] Prepared for 2-3 days of M1 training
  - [ ] Budget allows for compute costs

- [ ] **Prerequisites:**
  - [ ] Stage 1 or Stage 2 adapter available as policy init
  - [ ] SFT adapter available as reference model
  - [ ] [Simulator Design](./Web4_RL_Simulator_Design.md) reviewed

### Simulator Implementation

- [ ] **Core components:**
  - [ ] `MockFileSystem` class implemented
  - [ ] `Web4Simulator` environment class
  - [ ] OpenAI Gym API compatibility verified

- [ ] **Tools implemented:**
  - [ ] `read_file` tool
  - [ ] `write` tool
  - [ ] `search_replace` tool
  - [ ] `grep` tool
  - [ ] `glob_file_search` tool
  - [ ] `codebase_search` tool (mock semantic search)
  - [ ] `list_dir` tool
  - [ ] `run_terminal_cmd` tool (safe subset only)

- [ ] **Reward function:**
  - [ ] Task completion: +10.0
  - [ ] Correct tool: +5.0 per step
  - [ ] Schema pass: +2.0
  - [ ] Style pass: +1.0
  - [ ] Wrong tool: -3.0
  - [ ] Schema fail: -5.0
  - [ ] Guardrail violation: -10.0 (episode ends)
  - [ ] Step penalty: -0.5
  - [ ] KL penalty: -β × KL(policy || ref)

- [ ] **Environment validation:**
  - [ ] Determinism test: same actions → same results
  - [ ] Termination: episodes end properly
  - [ ] Performance: >10 episodes/sec
  - [ ] No memory leaks over 1000 episodes

### Task Generation

- [ ] **Handcrafted tasks:**
  - [ ] 50+ tasks created across difficulties
  - [ ] Coverage: tool-use, multi-step, search-edit, etc.
  - [ ] Each task has clear success criteria
  - [ ] Tasks tested manually (can be solved)

- [ ] **Task generator:**
  - [ ] `TaskGenerator` class implemented
  - [ ] Sampling by difficulty works
  - [ ] Procedural generation (optional) works

- [ ] **Curriculum scheduler:**
  - [ ] `CurriculumScheduler` implemented
  - [ ] Phase 1 (0-2K episodes): 70% simple
  - [ ] Phase 2 (2-10K episodes): 50% medium
  - [ ] Phase 3 (10K+ episodes): balanced distribution

### Before Training

- [ ] **Hyperparameters configured:**
  - [ ] Config from [Hyperparameter Guide](./Web4_RL_Hyperparameters.md)
  - [ ] Learning rate: 1e-6 (very conservative)
  - [ ] PPO clip range: 0.2
  - [ ] KL coefficient: 0.05
  - [ ] Entropy coefficient: 0.01
  - [ ] Batch size: 16-32 episodes
  - [ ] PPO epochs: 4-8

- [ ] **PPO/GRPO library:**
  - [ ] TRL library installed
  - [ ] PPOTrainer or GRPOTrainer initialized
  - [ ] Policy and reference models loaded
  - [ ] Value function initialized

- [ ] **Training script tested:**
  - [ ] 10 episodes run successfully
  - [ ] Rewards computed correctly
  - [ ] KL divergence logged
  - [ ] Checkpointing works

### During Training

- [ ] **Monitor metrics:**
  - [ ] Episode reward increasing (with noise)
  - [ ] KL divergence < 0.1 (warning if > 0.2)
  - [ ] Policy entropy > 2.0 (critical if < 1.0)
  - [ ] Episode length decreasing (efficiency improving)
  - [ ] Success rate increasing

- [ ] **Checkpoints:**
  - [ ] Save every 2000 episodes
  - [ ] Tag checkpoints with success rate

- [ ] **Warning signs:**
  - [ ] KL divergence > 0.2 → increase KL penalty, consider rollback
  - [ ] Entropy < 1.0 → add entropy bonus, rollback
  - [ ] Reward increasing but eval failing → reward hacking

- [ ] **Curriculum progression:**
  - [ ] Track success rate per difficulty
  - [ ] Adjust task distribution if needed

### After Training

- [ ] **Evaluation:**
  - [ ] Test on 500 held-out tasks
  - [ ] Episode success rate: ____% (target: ≥75%)
  - [ ] Multi-step planning accuracy vs Stage 2
  - [ ] Run all eval gates

- [ ] **Success criteria met:**
  - [ ] Episode success rate ≥ 75%
  - [ ] Multi-step plan accuracy +15-25%
  - [ ] All Stage 2 metrics maintained
  - [ ] KL divergence from SFT < 0.15
  - [ ] Perplexity increase < 10%

- [ ] **Deliverables:**
  - [ ] `PPO_v1.lora` (or `GRPO_v1.lora`)
  - [ ] Episode logs: `episodes_v1.jsonl`
  - [ ] Reward curves: `training_curves_v1.png`
  - [ ] Eval report: `stage3_eval_report.md`

- [ ] **Decision:**
  - [ ] Proceed to Stage 4 deployment? (if metrics pass)
  - [ ] Rollback to Stage 2? (if catastrophic forgetting)
  - [ ] Iterate? (if promising but not there yet)

---

## 5️⃣ Stage 4: Deployment Checklist

### Comprehensive Evaluation

- [ ] **Run all adapters on full eval set:**
  - [ ] SFT baseline
  - [ ] ORPO/DPO (Stage 1)
  - [ ] AWR/RS-SFT (Stage 2)
  - [ ] PPO/GRPO (Stage 3, if available)

- [ ] **Metrics comparison:**
  - [ ] JSON validity, schema compliance, lint pass
  - [ ] Tool success rate
  - [ ] Plan minimality
  - [ ] Code quality (AST, naming)
  - [ ] Guardrail compliance
  - [ ] Language quality (perplexity, BLEU)
  - [ ] Diversity (distinct n-grams)

- [ ] **Human evaluation (100 samples):**
  - [ ] Preference ranking across all stages
  - [ ] Overall quality scores (1-5 scale)
  - [ ] Bug detection
  - [ ] Mean quality ≥ 4.0?

### Adapter Selection

- [ ] **Compare stages:**
  - [ ] Which stage best meets goals?
  - [ ] Trade-offs documented

- [ ] **Merging exploration (optional):**
  - [ ] Sequential loading tested
  - [ ] Parameter averaging tested
  - [ ] Task routing strategy defined
  - [ ] Merged adapter re-evaluated

- [ ] **Final adapter selected:**
  - [ ] Adapter name: _______
  - [ ] Justification documented

### Production Preparation

- [ ] **Export adapter:**
  - [ ] Format: GGUF, SafeTensors, or appropriate for deployment
  - [ ] Size verified: fits in deployment memory budget
  - [ ] Loading tested on target hardware

- [ ] **Model card created:**
  - [ ] Training details (stages, hyperparameters)
  - [ ] Eval metrics
  - [ ] Known limitations
  - [ ] Usage examples
  - [ ] License information

- [ ] **Documentation:**
  - [ ] Deployment guide written
  - [ ] Inference code provided
  - [ ] Known issues documented
  - [ ] Troubleshooting guide

- [ ] **Monitoring setup:**
  - [ ] Production logging configured
  - [ ] JSON validity rate tracked
  - [ ] Tool success rate tracked
  - [ ] Distribution shift detection
  - [ ] Alerting configured for anomalies

### Deployment Execution

- [ ] **Phase 1: Shadow mode**
  - [ ] Run alongside baseline
  - [ ] Log all comparisons
  - [ ] No user-facing changes
  - [ ] Duration: 1-2 weeks
  - [ ] Metrics match eval expectations?

- [ ] **Phase 2: A/B test**
  - [ ] 50/50 traffic split
  - [ ] Track success metrics per variant
  - [ ] User feedback collected
  - [ ] Duration: 2-4 weeks
  - [ ] New model wins or ties?

- [ ] **Phase 3: Full rollout**
  - [ ] Gradual ramp to 100%
  - [ ] Monitor closely for first week
  - [ ] Rollback plan ready
  - [ ] Success!

### Final Deliverables

- [ ] **Artifacts:**
  - [ ] `Web4_PROD_v1.lora`
  - [ ] `model_card.md`
  - [ ] `deployment_guide.md`
  - [ ] `final_eval_report.md`

- [ ] **Backup & archival:**
  - [ ] All adapters backed up
  - [ ] All training logs backed up
  - [ ] Git tags for all milestones
  - [ ] Documentation archived

- [ ] **Post-deployment:**
  - [ ] Monitor for 1 month
  - [ ] Collect edge case examples
  - [ ] Plan next iteration (if needed)

---

## 🎉 Completion

Congratulations! You've successfully trained and deployed a reinforcement learning enhanced model.

### Post-Deployment

- [ ] **Continuous monitoring:**
  - [ ] Weekly metric reviews
  - [ ] Monthly human evaluation
  - [ ] Quarterly retraining with new data

- [ ] **Feedback loop:**
  - [ ] Collect production errors
  - [ ] Add to training data for next iteration
  - [ ] Update guardrails as needed

- [ ] **Documentation updates:**
  - [ ] Lessons learned documented
  - [ ] This checklist updated based on experience
  - [ ] Share findings with team

---

## 🔄 Version History

- **v1.0 (2025-10-27):** Initial implementation checklist

---

**End of Implementation Checklist**  
**Version:** 1.0  
**Date:** 2025-10-27

