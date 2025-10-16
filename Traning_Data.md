# 📘 Training Data Analysis: Framework Data Requirements and Public Dataset Sources

## 1️⃣ Purpose

This document analyzes:
- **How much of YOUR framework data** you need for meaningful behavior change in different model sizes,
- **Research-based thresholds** for framework-aligned training (30%+ of dataset must follow your patterns),
- **Public datasets** available for scaling up training,
- **Training from scratch strategy**: Taking public datasets and reworking them with your specific framework, methodologies, constraints, instructions, and boundaries,
- **Data collection requirements** in GB, tokens, and file counts for different model sizes.

---

## 2️⃣ Token estimation fundamentals

**Tokens ≠ words or characters.**

Rough conversion averages (for English + code):

| Source Type | Approx. tokens per word | Approx. tokens per character | Example |
|:-------------|:----------------------:|:-----------------------------:|:--------|
| **Natural text (English)** | 1.3 tokens/word | 0.25 tokens/char | Documentation, comments |
| **Programming code (TypeScript)** | 1.5–2.0 tokens/word | 0.33–0.40 tokens/char | Code, identifiers, symbols |

Rule of thumb:  
> **1 MB of text ≈ 700–1000 tokens**  
> **1 GB of source + docs ≈ 0.7–1 billion tokens**

---

## 3️⃣ Framework Data Requirements for Meaningful Impact

**Research Finding**: 30%+ of training data must follow specific patterns for the model to reliably exhibit those patterns. Below 30%, models show mostly generic behavior.

### 📊 How Much Framework Data You Need

| Model Size | Total Dataset Needed | Your Framework Data Required | Framework Impact | Expected Behavior |
|:-----------|:-------------------:|:---------------------------:|:----------------:|:-----------------:|
| **150M Model** | 3B tokens (4.3 GB, ~2M files) | 1.5B tokens (2.1 GB, ~1M files) | 50% of dataset | 90-95% framework behavior |
| **1.3B Model** | 26B tokens (37 GB, ~17M files) | 7.8B tokens (11 GB, ~5M files) | 30% of dataset | 80-85% framework behavior |
| **3B Model** | 60B tokens (86 GB, ~40M files) | 18B tokens (26 GB, ~12M files) | 30% of dataset | 75-80% framework behavior |
| **7B Model** | 140B tokens (200 GB, ~93M files) | 42B tokens (60 GB, ~28M files) | 30% of dataset | 70-75% framework behavior |

### 🎯 What This Means

- **150M Model**: Most practical starting point - need 2.1 GB of your framework code for 90-95% framework behavior
- **1.3B+ Models**: Require substantial framework ecosystems (11-60 GB) but still show some generic behavior
- **Quality over Quantity**: Well-structured framework examples matter more than raw volume
- **Pattern Consistency**: Your data must demonstrate consistent framework usage across different scenarios

---

## 4️⃣ Data Collection Timeline and Effort

### 📅 Realistic Collection Timelines

| Model Size | Framework Data Needed | Collection Focus | Timeline | Effort Level |
|:-----------|:-------------------:|:----------------|:---------|:------------|
| **150M Model** | 2.1 GB (1M files) | Core patterns, examples, docs | 2-4 weeks | Focused collection |
| **1.3B Model** | 11 GB (5M files) | Comprehensive examples, edge cases | 2-3 months | Systematic collection |
| **3B Model** | 26 GB (12M files) | Full ecosystem, real projects | 4-6 months | Extensive collection |
| **7B Model** | 60 GB (28M files) | Complete framework universe | 6-12 months | Massive collection effort |

### 🎯 What You Need to Collect

**Source Code**: All your framework implementations (DFrame, ONCE, components, utils)
**Documentation**: Comprehensive guides, API docs, examples, tutorials
**Test Cases**: Unit tests, integration tests showing proper usage patterns
**Real Projects**: Actual applications using your framework
**Edge Cases**: Error handling, complex scenarios, advanced usage patterns
**Examples**: Code samples, templates, best practices demonstrations

### ⚠️ Critical Questions

- **Do you have 2-60 GB of framework code?**
- **Can you systematically collect comprehensive examples?**
- **Is 70-95% framework behavior sufficient for your needs?**
- **What's your current framework ecosystem size?**

---

## 5️⃣ Training from scratch: Reworking public datasets with your framework

### 🎯 Why Train from Scratch?

**The goal**: Take public datasets and rework them to embed your specific:
- **Framework patterns** (DFrame, ONCE, component libraries)
- **Methodologies** (coding standards, architectural patterns)
- **Constraints** (security, performance, maintainability rules)
- **Instructions** (API usage, best practices, conventions)
- **Boundaries** (what to do/not do, domain limits)

### 📊 Data Strategy for Framework-Embedded Training

| Scenario | Your Framework Data | Public Data | Processing Strategy | Model Size |
|:-----------|:-------------|:------------|:-------------------|:-----------|
| **Framework-embedded 150M** | 1.5B tokens (50%) | 1.5B tokens (50%) | Train from scratch with your patterns | 150M parameters |
| **Framework-embedded 1.3B** | 7.8B tokens (30%) | 18.2B tokens (70%) | Rework public data with your framework | 1.3B parameters |
| **Framework-embedded 3B** | 18B tokens (30%) | 42B tokens (70%) | Transform public code to your patterns | 3B parameters |
| **Framework-embedded 7B** | 42B tokens (30%) | 98B tokens (70%) | Large-scale framework integration | 7B parameters |

### 🔄 Data Transformation Pipeline

1. **Public Dataset Ingestion**: Download and parse public code/text datasets
2. **Framework Pattern Injection**: Transform code examples to use your framework patterns
3. **Methodology Integration**: Rewrite examples to follow your methodologies
4. **Constraint Enforcement**: Filter and modify content to respect your constraints
5. **Instruction Embedding**: Add your specific instructions and guidelines
6. **Boundary Definition**: Ensure content stays within your domain boundaries
7. **Quality Validation**: Verify transformed data maintains quality and coherence

---

## 6️⃣ Scaling with Open Source Datasets

### 📊 Public Data Requirements for Different Models

| Model Size | Your Framework Data | Public Data Needed | Total Dataset | Public Data Sources |
|:-----------|:------------------:|:------------------:|:-------------:|:-------------------|
| **150M Model** | 1.5B tokens (2.1 GB) | 1.5B tokens (2.1 GB) | 3B tokens | GitHub TypeScript repos, NPM packages |
| **1.3B Model** | 7.8B tokens (11 GB) | 18.2B tokens (26 GB) | 26B tokens | The Stack, GitHub repos, documentation |
| **3B Model** | 18B tokens (26 GB) | 42B tokens (60 GB) | 60B tokens | Dolma, RedPajama, The Stack, GitHub |
| **7B Model** | 42B tokens (60 GB) | 98B tokens (140 GB) | 140B tokens | Full Dolma/RedPajama, The Stack, comprehensive sources |

### 🎯 Key Insight

**You need substantial amounts of YOUR framework data** (30-50% of total dataset) for meaningful behavior change. Public datasets provide the remaining 50-70% but must be transformed to embed your framework patterns.

### 📚 Major Open Source Datasets

| Dataset | Size | Tokens | Focus | License | Access |
|:--------|:-----|:-------|:------|:--------|:-------|
| **Dolma** (AI2) | 3TB | 3T+ | Web text, code, scientific | Apache 2.0 | [HuggingFace](https://huggingface.co/datasets/allenai/dolma) |
| **RedPajama** | 1.2TB | 1.2T+ | Web, books, code, scientific | Apache 2.0 | [RedPajama](https://github.com/togethercomputer/RedPajama-Data) |
| **The Stack** (BigCode) | 6.4TB | 3.2T+ | Code (multi-language) | Various | [HuggingFace](https://huggingface.co/datasets/bigcode/the-stack) |
| **StarCoder** | 1TB | 1T+ | Code (multi-language) | Various | [HuggingFace](https://huggingface.co/datasets/bigcode/starcoderdata) |
| **C4** (Common Crawl) | 750GB | 156B | Web text (English) | CC BY-SA 4.0 | [TensorFlow](https://www.tensorflow.org/datasets/catalog/c4) |
| **OpenWebText** | 38GB | 9B | Web text (Reddit links) | MIT | [HuggingFace](https://huggingface.co/datasets/openwebtext) |
| **BookCorpus** | 11GB | 1B | Books | Various | [HuggingFace](https://huggingface.co/datasets/bookcorpus) |
| **Wikipedia** | 20GB | 3B | Encyclopedia articles | CC BY-SA 3.0 | [HuggingFace](https://huggingface.co/datasets/wikipedia) |

### 🔧 Code-Specific Datasets

| Dataset | Size | Tokens | Languages | License | Access |
|:--------|:-----|:-------|:----------|:--------|:-------|
| **CodeSearchNet** | 2GB | 2M | 6 languages | MIT | [GitHub](https://github.com/github/CodeSearchNet) |
| **CodeXGLUE** | 1GB | 1M | 6 languages | MIT | [GitHub](https://github.com/microsoft/CodeXGLUE) |
| **HumanEval** | 164 problems | - | Python | MIT | [GitHub](https://github.com/openai/human-eval) |
| **MBPP** | 974 problems | - | Python | Apache 2.0 | [HuggingFace](https://huggingface.co/datasets/mbpp) |
| **TypeScript Corpus** | 50GB | 40B | TypeScript/JavaScript | Various | [GitHub](https://github.com/microsoft/TypeScript) |

---

## 7️⃣ Data management plan

| Step | Task | Recommended Tool | Output |
|:------|:------|:----------------:|:--------|
| 1 | Collect & deduplicate repos | `git-sizer`, `rclone`, `ripgrep` | Clean corpus directory |
| 2 | Filter by license (MIT/BSD/Apache) | `scancode-toolkit` | Compliance report |
| 3 | Clean code/comments | `pylint`, `eslint`, custom regex filters | Sanitized dataset |
| 4 | Tokenize & shard | `SentencePiece`, `HuggingFace datasets` | `.arrow` or `.jsonl.zst` shards |
| 5 | Store metadata | JSON/YAML manifest | Reproducibility |

---

## 8️⃣ Takeaway Summary

| Item | Value | Meaning |
|:------|:------|:---------|
| **Framework data needed for 150M model** | 1.5B tokens (2.1 GB, ~1M files) | 90-95% framework behavior, most practical starting point |
| **Framework data needed for 1.3B model** | 7.8B tokens (11 GB, ~5M files) | 80-85% framework behavior, requires systematic collection |
| **Framework data needed for 3B model** | 18B tokens (26 GB, ~12M files) | 75-80% framework behavior, extensive collection effort |
| **Framework data needed for 7B model** | 42B tokens (60 GB, ~28M files) | 70-75% framework behavior, massive collection effort |
| **Research threshold** | 30%+ of dataset must follow your patterns | Below this, models show mostly generic behavior |
| **Public dataset availability** | 1T+ tokens accessible | Provides remaining 50-70% of dataset after transformation |

---

**The Bottom Line:**  
**You need substantial amounts of YOUR framework data** (30-50% of total dataset) for meaningful behavior change. The 150M model is most practical - you need 2.1 GB of your framework code for 90-95% framework behavior.

**Critical Questions:**
- **Do you have 2-60 GB of framework code?**
- **Can you systematically collect comprehensive examples?**
- **Is 70-95% framework behavior sufficient for your needs?**

**Recommendation:** Start with 150M model (2.1 GB needed). Only pursue larger models if you have substantial framework ecosystems and can accept some generic behavior mixed with framework patterns.

**Key Insight**: Training from scratch allows you to create models that are fundamentally aligned with your framework from the ground up, rather than trying to retrofit existing models through fine-tuning. This approach ensures your specific patterns, methodologies, and constraints are deeply embedded in the model's knowledge base.

---

## 9️⃣ Data Acquisition Strategy

### 🎯 Recommended Data Mix for Different Goals

| Goal | Your Framework Data | Public Data | Total Tokens | Model Size |
|:-----|:-------------|:------------|:-------------|:-----------|
| **Domain-specific fine-tuning** | 1.5B tokens (100%) | 0B tokens | 1.5B | Any size (LoRA/QLoRA) |
| **Small custom model** | 1.5B tokens (50%) | 1.5B tokens (50%) | 3B | 150M parameters |
| **Medium model (1.3B)** | 7.8B tokens (30%) | 18.2B tokens (70%) | 26B | 1.3B parameters |
| **Large model (3B)** | 18B tokens (30%) | 42B tokens (70%) | 60B | 3B parameters |
| **Very large model (7B)** | 42B tokens (30%) | 98B tokens (70%) | 140B | 7B parameters |

### 📊 Data Quality Considerations for Framework Integration

| Data Source | Quality | Diversity | Framework Integration Potential | Recommended Use |
|:------------|:--------|:----------|:------------------------------|:----------------|
| **Your framework code** | High | Low | Perfect (already uses your framework) | Direct training, pattern examples |
| **GitHub TypeScript repos** | Medium-High | Medium | High (can be transformed) | Transform to your framework patterns |
| **The Stack (code)** | Medium | High | Medium (requires significant transformation) | Rewrite using your methodologies |
| **Dolma/RedPajama** | Medium | Very High | Low (general text, needs heavy processing) | Extract patterns, add framework context |
| **Wikipedia** | High | High | Low (general knowledge) | Add framework-specific examples |
| **Books/Web text** | Variable | Very High | Low (needs domain adaptation) | Transform to your domain context |

### 🎯 Framework-Specific Data Transformation Examples

| Original Public Content | Framework Transformation | Result |
|:------------------------|:------------------------|:--------|
| `React.useState()` | `DFrame.useState()` | Framework-specific state management |
| Generic API calls | `ONCE.apiClient.get()` | Your API client patterns |
| Standard error handling | Your error boundary patterns | Consistent error management |
| Generic TypeScript types | Your domain-specific types | Framework-aligned type system |
| Standard testing patterns | Your testing methodologies | Consistent testing approach |

### 🔄 Framework-Embedded Data Processing Pipeline

1. **Collection**: Gather internal repos + selected public datasets
2. **Framework Pattern Analysis**: Identify your framework patterns, methodologies, constraints
3. **Public Data Transformation**: 
   - Rewrite code examples to use your framework patterns
   - Transform generic patterns to your specific methodologies
   - Apply your constraints and boundaries
   - Inject your instructions and guidelines
4. **Deduplication**: Remove exact and near-duplicates using MinHash/LSH
5. **Quality filtering**: Remove low-quality, toxic, or irrelevant content
6. **Framework Validation**: Ensure transformed content follows your patterns
7. **Tokenization**: Train custom tokenizer on your domain data
8. **Sharding**: Split into training/validation/test sets
9. **Metadata**: Track source, license, quality scores, transformation applied

---

*Prepared: October 2025*  
*References: DeepMind Chinchilla (2022), AI2 Dolma (2024), RedPajama (2023), BigCode/StarCoder (2024).*
