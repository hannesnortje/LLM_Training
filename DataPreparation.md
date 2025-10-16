# 🧩 7B TypeScript LLM Development Pipeline (PDCA Methodology)

## OVERVIEW
A full, end-to-end process for developing a **7B-parameter TypeScript LLM** trained with your own framework, conventions, restrictions, and PDCA-style methodology.

The workflow proceeds in **six major phases**:

1️⃣ Dataset Assembly →  
2️⃣ Data Filtering & Integration →  
3️⃣ Tokenization & Sharding →  
4️⃣ Continued Pretraining →  
5️⃣ PDCA & Instruction Fine-Tuning →  
6️⃣ Evaluation & Deployment.

---

## 🔶 PHASE 1 — DATASET ASSEMBLY

### Sources
- **Open Source Code Corpora**
  - The Stack v2 (TypeScript + JavaScript)
  - CodeParrot GitHub-Code-Clean (TS/JS subset)
  - StarCoderData (optional supplement)
- **Internal Corpora**
  - DFrame / ONCE framework source
  - Documentation, coding conventions, and architectural guidelines
  - Code reviews, pull requests, test cases, and examples
  - PDCA cycles: Plan–Do–Check–Act pairs
- **Optional Contextual Text**
  - Technical documentation
  - API references and comments

### Outputs
- Raw dataset repository (`/datasets/raw`)
- Dataset manifest with metadata (source, license, language, tokens)
- Size target ≈ 140B tokens (500 GB–1 TB uncompressed)

---

## 🔶 PHASE 2 — DATA FILTERING & INTEGRATION

### 2.1 License Filtering
- Keep **MIT, Apache-2.0, BSD, MPL-2.0**
- Remove GPL, AGPL, proprietary licenses
- Tools: `scancode-toolkit`, The Stack v2 license metadata

### 2.2 Deduplication
- Exact deduplication via `xxhash64`
- Near-duplicate detection using MinHash + LSH
- Drop minified, auto-generated, and vendor files

### 2.3 Syntax & Quality Validation
- TypeScript syntax validation: `tsc --noEmit`
- ESLint or custom static analysis
- Minimum 50 LOC; remove empty or trivial files
- Measure comment/code ratio and complexity

### 2.4 Documentation Alignment
- Pair `.md` files with their referenced `.ts` files
- Keep documentation that refers to framework entities or code APIs

### 2.5 Integration of Internal Data
- Merge internal code and documentation
- Tag internal data as `internal=true` for oversampling
- Extract PDCA segments into structured JSONL:
  ```json
  {
    "plan": "...",
    "do": "...",
    "check": "...",
    "act": "...",
    "tags": ["TypeScript", "architecture", "lint", "security"]
  }
