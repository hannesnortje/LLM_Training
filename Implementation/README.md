# Web4 Balanced LoRA Training - Implementation Guide

**Complete step-by-step implementation guides for deploying the Web4 Agent**

---

## Overview

This directory contains detailed, actionable implementation guides for each phase of the Web4 Balanced LoRA Training Strategy. Each guide provides complete scripts, commands, validation checklists, and troubleshooting steps.

---

## Implementation Phases

### [Phase 1: Setup & RAG Bootstrap](Phase1_Setup_RAG_Bootstrap.md)
**Duration:** 1-2 weeks (flexible)  
**Goal:** Establish three-tier RAG system with all source data indexed

**What You'll Build:**
- Complete development environment (Python, Ollama, ChromaDB, Redis, SQLite)
- Three-tier RAG system (semantic + graph + temporal)
- 534 PDCAs indexed (~2,670 chunks)
- 3,477 TypeScript files indexed
- 12K tool examples indexed
- Validation test suite

**Key Deliverables:**
- ✓ RAG system operational
- ✓ All data indexed and queryable
- ✓ Test harness baseline established

---

### [Phase 2: Sample Generation](Phase2_Sample_Generation.md)
**Duration:** 1-2 weeks (flexible)  
**Goal:** Generate 37K training samples + 2K eval samples from RAG queries

**What You'll Build:**
- RAG-driven sample generation scripts
- 37K training samples across 7 categories:
  - style_core (12K): TypeScript coding patterns
  - domain_patterns (8K): Distilled PDCA patterns
  - process_framework (5K): PDCA/TRON/CMM templates
  - domain_representatives (3K): Top quality PDCAs
  - style_refactor (3K): CMM2→CMM3 transformations
  - guardrails (2K): Violation examples
  - tool_awareness (1K): Generic tool concepts
- 2K eval samples (stratified hold-out set)
- Validation suite (~20M tokens)

**Key Deliverables:**
- ✓ 37K training samples generated
- ✓ 2K eval samples (never trained)
- ✓ Total ~20M tokens validated
- ✓ All JSONL files ready

---

### [Phase 3: Training & Deployment](Phase3_Training_and_Deployment.md)
**Duration:** 1+ weeks (mostly compute time)  
**Goal:** Train LoRA adapter, merge & quantize, evaluate, deploy to production

**What You'll Build:**
- LoRA training pipeline (8-11 hours)
- Merge & quantization pipeline (2 hours)
- 6 test harnesses + 20 canary tasks (4 hours)
- Production deployment (1 hour)

**Training Steps:**
1. **LoRA Training:** 37K samples, 2 epochs, ~20M tokens → 80MB adapter
2. **Merge:** Adapter + base model → 14GB FP16 merged model
3. **Quantize:** 14GB FP16 → 4GB Q4_K_M GGUF
4. **Evaluate:** 6 test harnesses, must pass Ship Gates (≥95%)
5. **Deploy:** Import to Ollama, connect RAG, run smoke tests

**Key Deliverables:**
- ✓ Trained LoRA adapter
- ✓ 4GB GGUF model (web4-agent:latest)
- ✓ All quality gates passed (≥90% overall)
- ✓ Production deployment complete

---

### [Phase 4: Production & Continuous Learning](Phase4_Production_and_Continuous_Learning.md)
**Duration:** Ongoing  
**Goal:** Monitor production, establish evening training loop, achieve continuous improvement

**What You'll Build:**
- Production monitoring dashboard
- Evening training loop (nightly at 10 PM)
- Automated quality validation
- Performance optimization (RAG parameters, caching)
- Operational runbooks

**Continuous Learning Cycle:**
```
Day: Production serving → Daily work generated → Indexed to daily_buffer
Night (10 PM): Query buffer → Generate samples → Train 1 epoch (2-3 hrs)
           → Run canary tests → Deploy if pass → Clear buffer
Morning: Improved model in production → Better responses
```

**Key Deliverables:**
- ✓ Production monitoring operational
- ✓ Evening training loop running nightly
- ✓ Model improving daily from real work
- ✓ Self-improving virtuous cycle established

---

## Quick Start

### Prerequisites
- M1 Mac with 32GB RAM (or equivalent Linux system)
- macOS/Linux with bash shell
- ~30GB free disk space
- Access to Web4Articles repository
- HuggingFace account (free tier)

### Installation Sequence

**Week 1-2: Phase 1 (Setup & RAG Bootstrap)**
```bash
# Navigate to LLM_Training directory
cd /media/hannesn/storage/Code/CeruleanCircle/Planning/LLM_Training

# Follow Phase 1 guide step-by-step
open Implementation/Phase1_Setup_RAG_Bootstrap.md

# Expected outcome: RAG system operational, all data indexed
```

**Week 3-4: Phase 2 (Sample Generation)**
```bash
# Generate all training samples
open Implementation/Phase2_Sample_Generation.md

# Expected outcome: 37K training samples + 2K eval samples (~20M tokens)
```

**Week 5-6: Phase 3 (Training & Deployment)**
```bash
# Train, evaluate, deploy
open Implementation/Phase3_Training_and_Deployment.md

# Expected outcome: Model deployed to production, all gates passed
```

**Week 7+: Phase 4 (Production & Continuous Learning)**
```bash
# Establish monitoring and evening loop
open Implementation/Phase4_Production_and_Continuous_Learning.md

# Expected outcome: Self-improving system operational
```

---

## Implementation Timeline

### Typical Timeline (Full-Time)

| Phase | Duration | Compute Time | Manual Time |
|-------|----------|--------------|-------------|
| Phase 1 | 1 week | ~8 hours | ~32 hours |
| Phase 2 | 1 week | ~4 hours | ~36 hours |
| Phase 3 | 1 week | ~15 hours | ~25 hours |
| Phase 4 | 1 week+ | Ongoing | ~16 hours |
| **Total** | **4+ weeks** | **~27 hours** | **~109 hours** |

### Realistic Timeline (Part-Time)

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1 | 2 weeks | Setup, indexing, validation |
| Phase 2 | 2 weeks | Sample generation, QA |
| Phase 3 | 2 weeks | Training (overnight), evaluation |
| Phase 4 | Ongoing | Monitoring, optimization |
| **Total** | **6-8 weeks to production** | Then continuous |

---

## Critical Success Factors

### Phase 1 Success Criteria
- ✓ RAG system operational (all 3 tiers)
- ✓ 534 PDCAs indexed and queryable
- ✓ Query latency < 1 second
- ✓ Metadata complete (15+ fields)

### Phase 2 Success Criteria
- ✓ 37K training samples generated
- ✓ 2K eval samples stratified
- ✓ Total tokens ~20M (19M-21M acceptable)
- ✓ Schema compliance 100%

### Phase 3 Success Criteria
- ✓ Training loss 0.6-1.0 (good learning)
- ✓ All Ship Gates passed (≥95%)
- ✓ Overall score ≥90%
- ✓ Model deployed to production

### Phase 4 Success Criteria
- ✓ Production stable (metrics healthy)
- ✓ Evening loop running nightly
- ✓ Model improving daily
- ✓ Team trained and confident

---

## Key Scripts & Tools

### Phase 1 Scripts
- `scripts/initial_indexing.py` - Index all PDCAs, TypeScript, tools
- `scripts/test_rag_queries.py` - Validate RAG system

### Phase 2 Scripts
- `scripts/generate_style_core.py` - Generate 12K coding pattern samples
- `scripts/generate_domain_patterns.py` - Generate 8K PDCA patterns
- `scripts/generate_process_framework.py` - Generate 5K methodology samples
- `scripts/validate_samples.py` - Validate all 37K samples

### Phase 3 Scripts
- `scripts/train_lora_mps.py` - LoRA training (8-11 hours)
- `scripts/merge_and_quantize.py` - Merge adapter, quantize to GGUF (2 hours)
- `scripts/run_full_evaluation.sh` - Run all test harnesses (4 hours)
- `scripts/smoke_tests.py` - Production smoke tests

### Phase 4 Scripts
- `scripts/monitoring_dashboard.py` - Production metrics
- `scripts/evening_training_loop.py` - Nightly training automation
- `scripts/validate_improvements.py` - Morning validation
- `scripts/optimize_rag_parameters.py` - RAG tuning

---

## Troubleshooting

### Common Issues

**Phase 1: Redis Connection Errors**
```bash
# Check Redis is running
redis-cli ping

# Start if needed
brew services start redis  # macOS
sudo systemctl start redis-server  # Linux
```

**Phase 2: Token Count Off Target**
- Adjust sample content length
- Review distillation rules
- Check for duplicates

**Phase 3: Training OOM Crashes**
- Reduce `per_device_train_batch_size` to 1
- Reduce `gradient_accumulation_steps`
- Close other applications

**Phase 4: Evening Loop Failures**
- Check canary test logs
- Verify daily_buffer has quality data
- Test rollback procedure

See individual phase guides for detailed troubleshooting.

---

## Architecture Overview

### Training-First Production

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION RUNTIME                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Query → Trained Knowledge (80-90%, <200ms)           │
│       ↓                                                     │
│  Need History? → RAG PDCA Historical (10-20%, +300ms)      │
│       ↓                                                     │
│  Need Tools? → RAG Tool Examples (30%, +150ms)             │
│       ↓                                                     │
│  Response                                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   TRAINING PREPARATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RAG System → Sample Generation → 37K Samples               │
│       ↓                                                     │
│  LoRA Training (8-11 hrs) → 80MB Adapter                   │
│       ↓                                                     │
│  Merge & Quantize → 4GB GGUF Model                         │
│       ↓                                                     │
│  Evaluation (6 harnesses) → Deploy                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  CONTINUOUS LEARNING                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Daily Work → daily_buffer → Evening Loop (10 PM)           │
│       ↓                                                     │
│  Generate Samples → Train 1 Epoch (2-3 hrs)                │
│       ↓                                                     │
│  Canary Tests → Deploy if Pass → Improved Model            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Resource Requirements

### Hardware
- **CPU:** Apple M1/M2/M3 or equivalent (8+ cores)
- **RAM:** 32GB minimum (64GB recommended)
- **Storage:** 30GB free (50GB recommended)
- **GPU:** Apple Silicon MPS or CUDA-capable GPU

### Software
- **OS:** macOS 12+ or Linux (Ubuntu 20.04+)
- **Python:** 3.10+ with pip
- **Ollama:** Latest version
- **Redis:** 6.0+ with RedisGraph module
- **Git:** For version control

### Network
- **Bandwidth:** Stable connection for model downloads (~14GB)
- **HuggingFace:** Access to download base model

---

## Support & Documentation

### Primary Documentation
- [Phase 1: Setup & RAG Bootstrap](Phase1_Setup_RAG_Bootstrap.md)
- [Phase 2: Sample Generation](Phase2_Sample_Generation.md)
- [Phase 3: Training & Deployment](Phase3_Training_and_Deployment.md)
- [Phase 4: Production & Continuous Learning](Phase4_Production_and_Continuous_Learning.md)

### Related Documentation
- `../Training/Web4_Balanced_Training_Strategy.md` - Overall strategy
- `../Training/Web4_Balanced_Training_Architecture.drawio` - Visual diagrams

### Community & Help
- **Issues:** Document problems encountered
- **Improvements:** Suggest enhancements
- **Questions:** Refer to troubleshooting sections first

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-28 | Initial implementation guides created |

---

## License & Usage

These implementation guides are part of the Web4 LLM Training project. Follow all guidelines, especially:

- **Quality Gates:** Never skip Ship Gates (≥95%)
- **Evening Loop:** Always validate with canary tests
- **Rollback:** Test rollback procedure before going live
- **Documentation:** Keep runbooks up-to-date

---

## Getting Started

**Ready to begin?**

1. **Review prerequisites** - Ensure you have required hardware/software
2. **Clone repository** - Get latest code
3. **Start Phase 1** - Open `Phase1_Setup_RAG_Bootstrap.md`
4. **Follow step-by-step** - Each phase builds on the previous
5. **Validate thoroughly** - Use all checklists
6. **Document issues** - Help improve these guides

**🚀 Let's build a self-improving Web4 Agent!**

---

*Document Version: 1.0*  
*Last Updated: 2025-10-28*  
*Part of: Web4 Balanced LoRA Training Strategy*

