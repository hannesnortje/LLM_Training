# 🧠 Web4 LoRA Reinforcement Learning Add-On Plan

> Extension of the Web4 LoRA training pipeline with Human-Feedback and RL-based optimization.  
> Goal: Improve **tool-use precision**, **style consistency**, and **guardrail compliance** beyond SFT.

**Status:** Planning Phase  
**Last Updated:** 2025-10-27  
**Dependencies:** SFT LoRA baseline (from Core10Phase training)

---

## 📋 Quick Navigation

- [Overview](#1️⃣-overview--where-rl-fits)
- [Requirements & Feasibility](#2️⃣-requirements--feasibility)
- [Core Concepts](#3️⃣-core-acronyms-and-what-they-mean)
- [Stage Breakdown](#4️⃣-stage-breakdown--step-by-step-plan)
- [Evaluation Strategy](#5️⃣-evaluation--monitoring)
- [Warning Signs & Rollback](#6️⃣-warning-signs--rollback-procedures)
- [Next Steps](#7️⃣-next-steps)

**Supplementary Documents:**
- [Simulator Design](./Web4_RL_Simulator_Design.md) - Environment architecture for Stage 3
- [Annotation Guidelines](./Web4_RL_Annotation_Guidelines.md) - Human feedback collection
- [Hyperparameter Guide](./Web4_RL_Hyperparameters.md) - Tuning recommendations per stage
- [Implementation Checklist](./Web4_RL_Implementation_Checklist.md) - Pre-flight checks

---

## 1️⃣ Overview — Where RL Fits

**Purpose:**  
You already have a trained **SFT LoRA adapter** (Supervised Fine-Tuning).  
Now you'll extend it with **Reinforcement Learning phases** that refine the model's behavior using **human** and/or **AI feedback**.

**High-level pipeline:**

```
Base Model (DeepSeek-Coder 6.7B / Qwen2.5-Coder 7B)
   ↓
SFT LoRA (10 phases)  ← supervised data (Tool-Core, Style-Core, Guardrails)
   ↓
Stage 1: Preference Optimization (DPO / ORPO) — Human feedback
   ↓
Stage 2: Offline Reinforcement (RS-SFT / AWR) — AI feedback
   ↓
Stage 3: Online RL (PPO / GRPO with simulator) — [OPTIONAL: Cloud recommended]
   ↓
Stage 4: Evaluation & Deployment (Tool / Style / Guardrail gates)
```

**Key Decision Points:**
- ✅ Stages 0-2 are **M1 Max feasible** (confirmed)
- ⚠️ Stage 3 (PPO/GRPO) is **computationally intensive** (cloud recommended, see Feasibility section)
- 🎯 Each stage is **independent** - can stop after any stage if metrics plateau

---

## 2️⃣ Requirements & Feasibility

### Hardware Requirements

| Stage | Method | M1 Max (64GB) | Cloud Alternative | Est. Time |
|-------|--------|---------------|-------------------|-----------|
| 0 | SFT LoRA | ✅ Feasible | N/A | Already done |
| 1 | ORPO/DPO | ✅ Feasible | Optional | 4-8 hours |
| 2 | RS-SFT/AWR | ✅ Feasible | Optional | 6-12 hours |
| 3 | PPO/GRPO | ⚠️ Slow (1-2 days) | ✅ Recommended | 4-8 hours (cloud) |
| 4 | Eval/Merge | ✅ Feasible | N/A | 2-4 hours |

### Dataset Size Requirements

| Stage | Dataset Type | Minimum Size | Target Size | Effort Required |
|-------|--------------|--------------|-------------|-----------------|
| 0 | SFT Examples | 2,000 | 10,000 | Already collected |
| 1 | Preference Pairs | 500 | 1,500 | 8-15 hrs human annotation |
| 2 | AI-Scored Samples | 5,000 | 20,000 | Automated generation |
| 3 | Environment Episodes | 10,000 | 50,000 | Simulator runtime |

### Human Resource Requirements

| Task | Time Estimate | Skill Level | Notes |
|------|---------------|-------------|-------|
| Annotator training | 2 hours | Medium | See [Annotation Guidelines](./Web4_RL_Annotation_Guidelines.md) |
| Preference annotation (500 pairs) | 8-10 hours | Medium | ~1 min per comparison |
| Preference annotation (1,500 pairs) | 20-25 hours | Medium | Can split across annotators |
| Inter-annotator agreement check | 2 hours | High | Test on 100 overlapping pairs |

### Base Model Specifications

**Primary Target:** DeepSeek-Coder-6.7B or Qwen2.5-Coder-7B  
**Context Window:** 16K tokens  
**Quantization:** 4-bit (Q4_K_M) for M1, FP16 for cloud  
**LoRA Config:** r=16, alpha=32, dropout=0.05

---

## 3️⃣ Core Acronyms and What They Mean

| Acronym | Full Name | Meaning |
|----------|------------|----------|
| **SFT** | Supervised Fine-Tuning | Teach the model directly from gold examples (prompt → correct output). |
| **LoRA** | Low-Rank Adaptation | Lightweight fine-tuning adapters; train small matrices instead of all weights. |
| **RLHF** | Reinforcement Learning from Human Feedback | Humans compare outputs; model learns to prefer better ones. |
| **RM** | Reward Model | A model that scores how “good” an output is based on human judgments. |
| **PPO** | Proximal Policy Optimization | RL algorithm that updates the model with KL constraint to prevent drift. |
| **KL** | Kullback-Leibler Divergence | Distance between your new model and the SFT baseline; prevents instability. |
| **DPO / ORPO** | Direct / Odds-Ratio Preference Optimization | Train directly from (chosen, rejected) human pairs; simpler than PPO. |
| **RLAIF** | Reinforcement Learning from AI Feedback | Use automated rules (JSON/lint/AST) to produce feedback instead of humans. |
| **RS-SFT** | Rejection Sampling Fine-Tuning | Generate several outputs, keep the best (by reward), and fine-tune on those. |
| **AWR** | Advantage-Weighted Regression | Weighted fine-tuning: high-reward samples get higher weight. |
| **GRPO** | Group Relative PPO | PPO variant comparing candidates in groups (better stability). |

---

## 4️⃣ Stage Breakdown — Step-by-Step Plan

### 🟦 Stage 0 — Baseline (Already Done)

**Input:**  
- Curated buckets: Tool-Core, Style-Core, Guardrails  
- Training set: 8,000 examples  
- Eval set: 2,000 examples

**Process:**  
- Train SFT LoRA adapter across 10 phases (see Web4_LoRA_Core10Phase.md)

**Output:**  
- `SFT.lora` (checkpoint from best phase)  
- Baseline eval metrics logged

**Success Criteria:**  
- JSON validity ≥ 97%  
- Schema compliance ≥ 95%  
- Lint pass ≥ 98%  
- Guardrail violations ≤ 2%

**Status:** ✅ Complete

---

### 🟩 Stage 1 — Human Preference Optimization (DPO / ORPO)

**Goal:**  
Refine JSON accuracy, code style, and refusal correctness using human judgment.

**Timeline:** 2-3 weeks (1 week annotation, 1-2 weeks training/eval)

**Detailed Steps:**

1. **Sample Selection (Day 1-2)**
   - Select 500-1,500 diverse prompts from eval set
   - Ensure coverage: 40% tool-use, 30% style, 20% multi-step, 10% guardrails
   - Generate 3-5 outputs per prompt using `SFT.lora` with varying temperatures (0.7, 0.9, 1.1)

2. **Human Annotation (Week 1-2)**
   - Train annotators using [Annotation Guidelines](./Web4_RL_Annotation_Guidelines.md)
   - Collect preferences: which output is best?
   - Tag rejection reasons: wrong tool, schema fail, verbose, style off, unsafe
   - Target: 500 minimum, 1,500 optimal pairs
   - Quality check: 100 overlapping pairs for inter-annotator agreement (target κ ≥ 0.7)

3. **Dataset Construction (Day 1)**
   - Build (chosen, rejected) pairs
   - Split: 80% train, 10% val, 10% test
   - Balance categories (equal tool/style/guardrail representation)

4. **Training (Week 2-3)**
   - **Method:** ORPO (recommended) or DPO
   - **Hardware:** M1 Max (4-8 hours) or cloud
   - **Config:** See [Hyperparameter Guide](./Web4_RL_Hyperparameters.md)
   - **Checkpoints:** Every 100 steps, keep top-3 by validation loss

5. **Evaluation (Day 1-2)**
   - Run full eval gates (see Section 5)
   - Compare against SFT baseline
   - Human spot-check: 50 random outputs

**Output:**  
- `ORPO_v1.lora` (or `DPO_v1.lora`)
- Preference dataset: `preference_pairs_v1.jsonl`
- Eval report: `stage1_eval_report.md`

**Success Criteria (vs SFT baseline):**
- JSON validity ≥ 99% (+2%)
- Schema compliance ≥ 97% (+2%)
- Lint pass = 100% (+2%)
- Guardrail violations ≤ 1% (-1%)
- Human preference win-rate ≥ 65% (on held-out test set)

**Exit Criteria:**
- ✅ All metrics pass → Proceed to Stage 2
- ⚠️ Metrics plateau but no regression → Proceed to Stage 2
- 🛑 Any metric regresses >3% → Debug or rollback (see Section 6)

**Why ORPO First:** M1-friendly, no separate reward model needed, stable training, simultaneous SFT+preference optimization

---

### 🟨 Stage 2 — Offline Reinforcement (RLAIF / RS-SFT / AWR)

**Goal:**  
Scale up training using automated evaluators to improve minimality, argument precision, and code cleanliness.

**Timeline:** 1-2 weeks (automated pipeline)

**Detailed Steps:**

1. **Reward Function Implementation (Day 1-2)**
   - Build automated scoring pipeline
   - Components:
     - JSON validator: +1.0 if valid, 0.0 otherwise
     - Schema validator: +1.0 if passes, 0.0 otherwise
     - Tool executor (mock): +1.0 if successful, 0.0 otherwise
     - Lint/Format: +1.0 if passes, 0.0 otherwise
     - AST checker: +0.5 if correct structure
     - Guardrail: -2.0 if violates policy
     - Verbosity penalty: -0.1 per unnecessary plan step
     - Off-policy penalty: -0.5 if deviates from expected tool sequence
   - Normalize final score to [0, 1]
   - Log reward components for debugging

2. **Data Generation (Day 2-4)**
   - Select 5,000-20,000 diverse prompts
   - Generate 4-8 outputs per prompt using `ORPO.lora` (from Stage 1) or `SFT.lora`
   - Use temperature sampling: 0.6, 0.8, 1.0, 1.2
   - Score all outputs with reward function
   - Log reward distribution (aim for mean ~0.6-0.7)

3. **Method Selection**
   - **RS-SFT (Recommended for M1):** Keep top-1 output per prompt, continue SFT
   - **AWR (More sophisticated):** Weight each sample by advantage = reward - baseline
   - **RLAIF (Hybrid):** Generate preference pairs where |reward_diff| > threshold

4. **Training (Week 1-2)**
   - **Method:** RS-SFT or AWR
   - **Hardware:** M1 Max (6-12 hours) or cloud
   - **Base:** Continue from `ORPO.lora` or `SFT.lora`
   - **Config:** See [Hyperparameter Guide](./Web4_RL_Hyperparameters.md)
   - **Monitor:** Average reward, distribution shift, perplexity

5. **Evaluation (Day 1-2)**
   - Run full eval gates
   - Compare reward distribution: Stage 2 vs Stage 1
   - Check for reward hacking (e.g., model exploits JSON validator quirks)
   - Sample diversity check (n-gram overlap, BLEU self-similarity)

**Output:**  
- `AWR_v1.lora` (or `RSSFT_v1.lora`)
- Scored dataset: `scored_outputs_v1.jsonl`
- Reward logs: `reward_traces_v1.csv`
- Eval report: `stage2_eval_report.md`

**Success Criteria (vs Stage 1):**
- JSON validity ≥ 99% (maintain)
- Schema compliance ≥ 98% (+1%)
- Tool success rate ≥ 95% (new metric)
- Plan minimality: avg steps reduced by 10-20%
- No distribution collapse (vocab diversity ≥ 0.8 of baseline)

**Exit Criteria:**
- ✅ All metrics pass & reward improves → Optionally proceed to Stage 3
- ⚠️ Metrics plateau → Stop here, deploy Stage 1/2 adapter
- 🛑 Reward hacking detected → Debug reward function, retrain
- 🛑 Distribution collapse → Rollback, increase KL penalty

**Method Choice:**
- Use **RS-SFT** if: compute-limited, want simplicity, don't need fine-grained weighting
- Use **AWR** if: have more compute, want better sample efficiency
- Use **RLAIF** if: want to combine with Stage 1 human preferences

---

### 🟥 Stage 3 — Online RL (PPO / GRPO with Simulator) [OPTIONAL]

**Goal:**  
Teach model to succeed in multi-step tool plans through live environment interaction.

**⚠️ Feasibility Warning:**  
This stage is computationally intensive. **Cloud GPU recommended** unless you have 2-3 days for M1 training.

**Timeline:** 2-4 weeks (simulator dev + training + eval)

**Prerequisites:**
- Functional simulator (see [Simulator Design](./Web4_RL_Simulator_Design.md))
- Stage 1 or Stage 2 adapter as policy initialization
- Reference model for KL penalty (typically `SFT.lora`)

**Detailed Steps:**

1. **Simulator Setup (Week 1)**
   - Implement mock file system (in-memory)
   - Implement tool stubs (deterministic behavior)
   - Define reward function:
     - +10 for task completion
     - +5 per correct tool call
     - +2 for schema compliance
     - +1 for style compliance
     - -1 per unnecessary action
     - -5 for schema failure
     - -10 for policy violation
   - KL penalty: -β × KL(policy || reference) where β ≈ 0.01-0.1
   - Test with 100 handcrafted episodes

2. **Environment Validation (Day 2-3)**
   - Verify deterministic behavior
   - Check reward function not exploitable
   - Ensure episodes terminate properly
   - Log episode statistics (length, reward, success rate)

3. **PPO/GRPO Training (Week 2-3)**
   - **Method:** PPO or GRPO (GRPO preferred for stability)
   - **Hardware:** Cloud GPU (4-8 hours) or M1 Max (1-2 days)
   - **Batch size:** 16-32 episodes (use gradient accumulation on M1)
   - **PPO epochs:** 4-8 per batch
   - **Config:** See [Hyperparameter Guide](./Web4_RL_Hyperparameters.md)
   - **Monitor:**
     - Episode reward (should increase)
     - KL divergence (keep < 0.1)
     - Policy entropy (should remain > 2.0)
     - Success rate (target 70-90%)

4. **Training Phases**
   - **Phase 1 (2-5K episodes):** Simple single-tool tasks
   - **Phase 2 (5-10K episodes):** 2-3 step chains
   - **Phase 3 (10-20K episodes):** Complex multi-step plans
   - Gradually increase task difficulty (curriculum learning)

5. **Evaluation (Week 3-4)**
   - Test on held-out task distribution
   - Run full eval gates
   - Compare episode success rate: Stage 3 vs Stage 2
   - Human review: watch 20 episode replays

**Output:**  
- `PPO_v1.lora` (or `GRPO_v1.lora`)
- Episode logs: `episodes_v1.jsonl`
- Reward curves: `training_curves_v1.png`
- Eval report: `stage3_eval_report.md`

**Success Criteria (vs Stage 2):**
- Episode success rate ≥ 75%
- Multi-step plan accuracy +15-25%
- All Stage 2 metrics maintained
- KL divergence from SFT < 0.15
- No catastrophic forgetting (perplexity increase < 10%)

**Exit Criteria:**
- ✅ All metrics pass → Proceed to Stage 4
- ⚠️ Success rate plateaus but ≥60% → Accept and proceed
- 🛑 KL divergence > 0.2 → Increase KL penalty, restart from checkpoint
- 🛑 Catastrophic forgetting → Rollback to Stage 2
- 🛑 Policy collapse (entropy < 1.0) → Add entropy bonus, restart

**Skip Stage 3 If:**
- Your use case doesn't require complex multi-step planning
- Stage 2 metrics already meet your goals
- Compute budget is constrained
- Simulator implementation too complex for your domain

---

### 🟧 Stage 4 — Evaluation & Deployment

**Goal:**  
Final validation, adapter merging/selection, and production deployment.

**Timeline:** 1 week

**Steps:**

1. **Comprehensive Evaluation (Day 1-3)**
   - Run **all** adapters on full eval set (2,000 examples)
   - Metrics tracked:
     - JSON validity, schema compliance, lint pass (automated)
     - Tool success rate (mock executor)
     - Plan minimality (avg steps vs gold)
     - Code quality (AST correctness, naming conventions)
     - Guardrail compliance (violation rate)
     - Language quality (perplexity, BLEU vs baseline)
     - Diversity (distinct n-grams, vocab size)
   - Human evaluation (100 samples):
     - Preference ranking: SFT vs ORPO vs AWR vs PPO
     - Overall quality score (1-5 scale)
     - Bug detection

2. **Adapter Selection (Day 3-4)**
   - Compare all stages on eval gates:
     - If Stage 1 meets all goals → Use `ORPO.lora`
     - If Stage 2 significantly better → Use `AWR.lora`
     - If Stage 3 improves multi-step → Use `PPO.lora`
   - Consider merging strategies:
     - **Sequential loading:** SFT + ORPO + AWR (stack adapters)
     - **Parameter averaging:** Interpolate adapter weights
     - **Task routing:** Use different adapters for different task types
   - Test merged adapters if pursuing combination

3. **Adapter Merging Options (Optional)**
   - **Option A:** Keep adapters separate, route by task type
   - **Option B:** Merge into base model (permanent)
   - **Option C:** Stack multiple LoRAs (if framework supports)
   - **Testing:** Re-run eval gates on merged model

4. **Production Prep (Day 4-5)**
   - Export final adapter(s) in deployment format (GGUF, SafeTensors, etc.)
   - Create model card with training details
   - Document known limitations
   - Set up monitoring for production use:
     - Log JSON validity rate
     - Track tool success rate
     - Monitor for distribution shift
   - Package with inference code

5. **Rollout Plan (Day 5-7)**
   - **Phase 1:** Shadow mode (run alongside baseline, log comparisons)
   - **Phase 2:** A/B test (50/50 traffic split)
   - **Phase 3:** Full rollout if metrics hold
   - Rollback plan: revert to `SFT.lora` if issues detected

**Output:**  
- Selected/merged adapter: `Web4_PROD_v1.lora`
- Model card: `model_card.md`
- Deployment guide: `deployment_guide.md`
- Final eval report: `final_eval_report.md`

**Deployment Checklist:**
- [ ] All eval gates pass thresholds
- [ ] Human spot-check approved (≥90% quality)
- [ ] Inference speed acceptable (< 2s per tool call)
- [ ] Memory footprint acceptable (< 10GB RAM)
- [ ] Model card complete
- [ ] Rollback procedure tested
- [ ] Monitoring dashboards configured

---

## 5️⃣ Evaluation & Monitoring

### Automated Eval Gates

Run these on **every checkpoint** (minimum 500 diverse samples):

| Metric | Threshold | Tool | Failure Action |
|--------|-----------|------|----------------|
| JSON validity | ≥ 99% | Python `json.loads()` | Flag checkpoint, investigate |
| Schema compliance | ≥ 97% | `jsonschema` validator | Review failing examples |
| Lint pass | 100% | ESLint (generated code) | Auto-fix if possible |
| AST correctness | ≥ 90% | TypeScript parser | Check for syntax errors |
| Naming conventions | ≥ 95% | Regex patterns | Retrain if systematic |
| Guardrail violations | ≤ 1% | Keyword/pattern match | Hard stop if > 5% |

### Continuous Monitoring

Track these **during training** (logged every 100 steps):

| Metric | Healthy Range | Warning Sign | Interpretation |
|--------|---------------|--------------|----------------|
| Loss | Decreasing | Increasing | Overfitting or bad batch |
| Perplexity | 3-15 | > 20 or < 2 | Language quality issue |
| KL divergence (RL stages) | 0.01-0.10 | > 0.2 | Policy drifting too far |
| Gradient norm | 0.1-2.0 | > 5.0 | Instability |
| Learning rate | Scheduled | N/A | Check scheduler |
| Avg reward (RL stages) | Increasing | Flat or decreasing | Learning stalled |
| Policy entropy (PPO) | > 2.0 | < 1.0 | Policy collapse |

### Distribution Shift Detection

Run **every 1,000 steps** (compare to SFT baseline):

| Metric | Tool | Acceptable Range | Action if Outside Range |
|--------|------|------------------|-------------------------|
| Vocab diversity | Distinct unigrams | ≥ 80% of baseline | Increase temperature/entropy |
| N-gram overlap | BLEU self-similarity | < 0.5 | Check for repetition |
| Token distribution | KL(generated || baseline) | < 0.3 | Review training data balance |
| Avg output length | Token count | ±20% of baseline | Check for verbosity/terseness |

### Human Evaluation Protocol

Run on **100 random samples** at each stage boundary:

1. **Quality Ranking (1-5 scale)**
   - 5 = Perfect (gold standard quality)
   - 4 = Good (minor issues, still usable)
   - 3 = Acceptable (noticeable issues but functional)
   - 2 = Poor (major issues, barely usable)
   - 1 = Broken (unusable)
   - **Target:** Mean ≥ 4.0, Median ≥ 4

2. **Preference Comparison**
   - Show output from current stage vs baseline
   - Annotator picks better one (or "tie")
   - **Target:** Win rate ≥ 60% vs baseline

3. **Bug Detection**
   - Annotators flag: wrong tool, schema error, unsafe code, style violation
   - **Target:** Bug rate ≤ 5%

4. **Inter-Annotator Agreement**
   - 20 overlapping samples between 2+ annotators
   - Calculate Cohen's κ
   - **Target:** κ ≥ 0.65

---

## 6️⃣ Warning Signs & Rollback Procedures

### Warning Signs by Type

#### 🔴 Critical (Stop Training Immediately)

| Warning Sign | Possible Cause | Action |
|--------------|----------------|--------|
| Guardrail violations > 5% | Reward hacking or bad data | STOP, rollback to last good checkpoint |
| JSON validity < 90% | Catastrophic forgetting | STOP, rollback |
| Loss exploding (NaN/Inf) | Learning rate too high | STOP, reduce LR by 10x, restart |
| KL divergence > 0.3 | Policy collapse | STOP, increase KL penalty, rollback |
| Policy entropy < 0.5 (PPO) | Mode collapse | STOP, add entropy bonus, rollback |

#### 🟡 Warning (Monitor Closely, Consider Intervention)

| Warning Sign | Possible Cause | Action |
|--------------|----------------|--------|
| Metrics plateaued (no improvement for 2K steps) | Learning stalled | Try: increase LR, change data mix, or stop and proceed |
| Reward increasing but gates failing | Reward hacking | Revise reward function, add constraints |
| Output becoming very short or very long | Distribution shift | Adjust length penalty |
| Perplexity increasing gradually | Forgetting base knowledge | Add regularization or reduce LR |
| Validation loss increasing while train loss decreasing | Overfitting | Add dropout, reduce epochs, more data |

#### 🟢 Informational (Normal Variations)

| Observation | Interpretation | Action |
|-------------|----------------|--------|
| Small KL divergence fluctuations (±0.02) | Normal training dynamics | Continue |
| Slight perplexity increase (< 5%) | Acceptable specialization cost | Continue if gates pass |
| Metrics improving slowly | Normal for later stages | Be patient, monitor |

### Rollback Procedure

**When to Rollback:**
- Any critical warning sign appears
- Multiple warning signs accumulate
- Human eval reveals serious quality degradation
- Production deployment shows issues

**How to Rollback:**

1. **Identify Last Good Checkpoint**
   - Review eval logs: find last checkpoint where all gates passed
   - Verify human eval scores if available
   - Tag as `rollback_safe_<stage>_<step>`

2. **Execute Rollback**
   ```bash
   # Stop current training
   # Load last good checkpoint
   # Re-run eval gates to confirm
   # Document rollback reason in logs
   ```

3. **Debug & Fix**
   - Analyze what went wrong:
     - Bad training data?
     - Hyperparameter issue?
     - Reward function exploit?
   - Make targeted fix
   - Test fix on small subset

4. **Resume or Restart**
   - If minor fix → Resume from rollback checkpoint
   - If major fix → Restart stage from beginning
   - Document changes in training log

**Baseline Fallback:**
- Always keep `SFT.lora` as emergency fallback
- If all RL stages fail → revert to SFT
- SFT should always be production-ready

### Reward Hacking Detection

**Common Patterns:**

| Hack Type | Detection | Fix |
|-----------|-----------|-----|
| JSON exploit | Valid JSON but semantically wrong | Add semantic checks to reward |
| Length gaming | Extremely short outputs score high | Add minimum length penalty |
| Tool spam | Calls many tools to boost score | Penalize unnecessary tool calls |
| Copy-paste | Repeats prompt as output | Check BLEU vs prompt |
| Schema bypass | Exploits validator edge cases | Tighten schema, add examples |

**Prevention:**
- Use multiple independent validators
- Human spot-check high-reward samples
- Add diversity bonus to reward
- Cap maximum reward per component

---

## 7️⃣ Summary — Stage-by-Stage Outputs

| Stage | Name | Output | Feedback Source | Dataset Size | Timeline | Key Benefit |
|-------|------|---------|-----------------|--------------|----------|-------------|
| 0 | SFT LoRA | `SFT.lora` | Gold data | 8,000 | Complete | Baseline correctness |
| 1 | DPO/ORPO | `ORPO.lora` | Humans | 500-1,500 pairs | 2-3 weeks | JSON/style/guardrail precision |
| 2 | RLAIF/AWR | `AWR.lora` | Automated judges | 5K-20K | 1-2 weeks | Minimality & argument precision |
| 3 | PPO/GRPO | `PPO.lora` | Simulator | 10K-50K episodes | 2-4 weeks | Multi-step planning |
| 4 | Merge/Deploy | `Web4_PROD.lora` | Eval scripts | N/A | 1 week | Integrated best-of behaviors |

---

## 8️⃣ Next Steps

### Immediate (Week 1)

1. **Review supplementary docs**
   - [ ] Read [Simulator Design](./Web4_RL_Simulator_Design.md)
   - [ ] Read [Annotation Guidelines](./Web4_RL_Annotation_Guidelines.md)
   - [ ] Read [Hyperparameter Guide](./Web4_RL_Hyperparameters.md)
   - [ ] Complete [Implementation Checklist](./Web4_RL_Implementation_Checklist.md)

2. **Prepare Stage 1 (ORPO)**
   - [ ] Select 500-1,500 prompts for annotation
   - [ ] Generate 3-5 outputs per prompt using SFT.lora
   - [ ] Set up annotation interface (Streamlit/Flask/Google Forms)
   - [ ] Train annotators on guidelines

3. **Infrastructure setup**
   - [ ] Set up eval harness (automated gates)
   - [ ] Configure checkpoint saving strategy
   - [ ] Set up monitoring dashboards (WandB/TensorBoard)
   - [ ] Test rollback procedure

### Short-term (Month 1)

4. **Execute Stage 1**
   - [ ] Collect 500+ preference pairs
   - [ ] Check inter-annotator agreement
   - [ ] Train ORPO adapter
   - [ ] Run full evaluation
   - [ ] Decision: proceed to Stage 2 or iterate?

5. **Prepare Stage 2 (if Stage 1 succeeds)**
   - [ ] Implement automated reward function
   - [ ] Generate and score 5K-20K outputs
   - [ ] Validate reward distribution

### Medium-term (Month 2-3)

6. **Execute Stage 2**
   - [ ] Train AWR/RS-SFT adapter
   - [ ] Monitor for reward hacking
   - [ ] Run full evaluation
   - [ ] Decision: proceed to Stage 3 or deploy Stage 2?

7. **Prepare Stage 3 (if pursuing)**
   - [ ] Implement simulator environment
   - [ ] Validate reward function in simulator
   - [ ] Test on 100 handcrafted episodes

8. **Execute Stage 3 (optional)**
   - [ ] Train PPO/GRPO adapter (cloud recommended)
   - [ ] Monitor KL divergence and entropy
   - [ ] Run full evaluation

### Long-term (Month 3+)

9. **Stage 4: Deploy**
   - [ ] Select best adapter(s)
   - [ ] Test merging strategies if applicable
   - [ ] Create model card and docs
   - [ ] Shadow deployment
   - [ ] A/B testing
   - [ ] Full rollout

10. **Continuous improvement**
    - [ ] Collect production feedback
    - [ ] Add new preference pairs from edge cases
    - [ ] Periodic retraining with updated data
    - [ ] Monitor for distribution drift

---

## 9️⃣ Draw.io Diagram Structure

**For Cursor diagram generation**, create these visual components:

### Main Pipeline (Vertical Flow)

```
┌─────────────────────────────────────────────┐
│  Stage 0: SFT LoRA (Baseline)               │
│  Input: 8K examples | Output: SFT.lora      │
│  Status: ✅ Complete                         │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│  Stage 1: ORPO (Human Preferences)          │
│  Input: 500-1.5K pairs | Output: ORPO.lora  │
│  Timeline: 2-3 weeks | Hardware: M1 ✅       │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│  Stage 2: AWR (AI Feedback)                 │
│  Input: 5K-20K scored | Output: AWR.lora    │
│  Timeline: 1-2 weeks | Hardware: M1 ✅       │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│  Stage 3: PPO (Simulator) [OPTIONAL]        │
│  Input: 10K-50K episodes | Output: PPO.lora │
│  Timeline: 2-4 weeks | Hardware: Cloud ⚠️    │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│  Stage 4: Evaluation & Deployment           │
│  Output: Web4_PROD.lora                     │
│  Timeline: 1 week                           │
└─────────────────────────────────────────────┘
```

### Feedback Loops (Side Annotations)

- **Human Loop** (connects to Stage 1)
  - Annotators → Preferences → Training
- **AI Loop** (connects to Stage 2)
  - Automated validators → Scores → Training
- **Simulator Loop** (connects to Stage 3)
  - Environment → Rewards → Policy Update

### Decision Diamonds

Add after each stage:
- ✅ Metrics Pass → Next Stage
- ⚠️ Metrics Plateau → Evaluate Options
- 🛑 Metrics Regress → Rollback

### Icons/Colors

- 🧠 Model checkpoints (blue boxes)
- 👤 Human involvement (green boxes)
- ⚙️ Automated systems (yellow boxes)
- 🎮 Simulator (red box)
- 📊 Evaluation gates (purple diamonds)

---

## 🔗 Related Documents

- [Web4_LoRA_Core10Phase.md](../Training/Web4_LoRA_Core10Phase.md) - SFT baseline training
- [Web4_RL_Simulator_Design.md](./Web4_RL_Simulator_Design.md) - Stage 3 environment architecture
- [Web4_RL_Annotation_Guidelines.md](./Web4_RL_Annotation_Guidelines.md) - Human feedback collection
- [Web4_RL_Hyperparameters.md](./Web4_RL_Hyperparameters.md) - Training configuration
- [Web4_RL_Implementation_Checklist.md](./Web4_RL_Implementation_Checklist.md) - Pre-flight validation

---

**End of RL Add-On Plan**  
**Version:** 2.0 (Refactored)  
**Date:** 2025-10-27
