# 📝 Web4 RL Annotation Guidelines

> Human feedback collection guidelines for ORPO/DPO preference training (Stage 1)

**Version:** 1.0  
**Last Updated:** 2025-10-27  
**Target Users:** Human annotators providing preference judgments

---

## 🎯 Purpose

This document guides human annotators in providing high-quality preference judgments for reinforcement learning from human feedback (RLHF). Your annotations will teach the model to:

1. Use correct tools with valid parameters
2. Generate minimal, efficient plans
3. Follow code style conventions
4. Respect safety guardrails

---

## 📋 Table of Contents

1. [Annotator Training](#1️⃣-annotator-training)
2. [Task Overview](#2️⃣-task-overview)
3. [Evaluation Criteria](#3️⃣-evaluation-criteria)
4. [Decision Process](#4️⃣-decision-process)
5. [Edge Cases](#5️⃣-edge-cases)
6. [Quality Standards](#6️⃣-quality-standards)
7. [Examples](#7️⃣-examples)

---

## 1️⃣ Annotator Training

### Prerequisites

- **Time Required:** 2 hours initial training
- **Background:** Basic understanding of:
  - JSON format
  - Programming concepts (functions, parameters)
  - File operations (read, write, search)
- **Materials:** This document + 20 practice examples

### Training Process

1. **Read this document** (30 mins)
2. **Review 10 worked examples** with explanations (30 mins)
3. **Annotate 10 practice examples** independently (45 mins)
4. **Review with trainer** - discuss disagreements (15 mins)
5. **Quality check:** Annotate 20 overlapping examples with experienced annotator
   - Target: Cohen's κ ≥ 0.7 (substantial agreement)
   - If κ < 0.7, review disagreements and retrain

### Certification

- **Pass Criteria:** κ ≥ 0.7 on 20 practice pairs
- **Ongoing:** Random 10% of annotations checked for quality
- **Recalibration:** Monthly review session (30 mins)

---

## 2️⃣ Task Overview

### What You'll See

For each annotation task, you'll be shown:

1. **User Prompt:** The instruction given to the AI
2. **Output A:** First model response
3. **Output B:** Second model response (sometimes 3-5 outputs)
4. **Context:** Sometimes includes file contents or prior conversation

### What You'll Do

1. **Compare** the outputs based on evaluation criteria (Section 3)
2. **Choose** which output is better (or mark as "tie")
3. **Tag** rejection reasons for worse outputs
4. **Provide** brief justification (1-2 sentences)
5. **Time:** Aim for ~1 minute per comparison

### Example Interface

```
┌─────────────────────────────────────────────────────────────┐
│ Prompt: Use file_search to find all TypeScript files, then  │
│         read main.ts                                         │
├─────────────────────────────────────────────────────────────┤
│ Output A:                                                    │
│ {"tool": "file_search", "args": {"pattern": "*.ts"}}        │
│                                                              │
│ Output B:                                                    │
│ {"tool": "glob_file_search", "args": {"glob": "*.ts"}}      │
├─────────────────────────────────────────────────────────────┤
│ Which is better? [A] [B] [Tie]                              │
│ Rejection reason: [wrong_tool] [schema_fail] [verbose] ...  │
│ Justification: ________________________________              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3️⃣ Evaluation Criteria

Rate outputs based on these criteria **in order of priority**:

### Priority 1: Correctness (Critical)

| Criterion | Good | Bad |
|-----------|------|-----|
| **Valid JSON** | Parseable, no syntax errors | Malformed, missing braces |
| **Correct Tool** | Tool exists and matches intent | Non-existent or wrong tool |
| **Schema Match** | All required fields present, correct types | Missing fields, wrong types |
| **Safety** | No guardrail violations | Attempts unsafe operations |

**If Output violates Priority 1, it's automatically worse** (even if better on other criteria)

### Priority 2: Efficiency

| Criterion | Good | Bad |
|-----------|------|-----|
| **Plan Minimality** | Fewest necessary steps | Redundant or extra steps |
| **Argument Precision** | Only required parameters | Unnecessary parameters |
| **Single Responsibility** | One clear action per step | Multiple mixed actions |

### Priority 3: Style & Clarity

| Criterion | Good | Bad |
|-----------|------|-----|
| **Code Style** | Matches conventions (camelCase, etc.) | Inconsistent naming |
| **Readability** | Clear parameter names | Cryptic abbreviations |
| **Formatting** | Clean, consistent indentation | Messy or inconsistent |

### Priority 4: Robustness

| Criterion | Good | Bad |
|-----------|------|-----|
| **Error Handling** | Considers edge cases | Assumes happy path only |
| **Completeness** | Fulfills entire request | Partial solution |
| **Context Awareness** | Uses available information | Ignores context |

---

## 4️⃣ Decision Process

### Step-by-Step

1. **Quick Validity Check** (5 seconds)
   - Is JSON valid for both?
   - Do tools exist?
   - If one fails, choose the other → DONE

2. **Correctness Check** (10 seconds)
   - Do parameters match tool schema?
   - Does output match user intent?
   - Any guardrail violations?
   - If one fails, choose the other → DONE

3. **Efficiency Comparison** (20 seconds)
   - Count steps: fewer is usually better
   - Check for redundant operations
   - Prefer simpler approach if both work

4. **Style Comparison** (15 seconds)
   - Which follows conventions better?
   - Which is more readable?
   - Minor differences → might be a tie

5. **Make Decision** (10 seconds)
   - Clear winner? Choose it
   - Very close? Mark as "tie" (but try to pick if possible)
   - Document reasoning briefly

### Decision Confidence

Tag each annotation with confidence:

- **High:** Clear difference, easy decision (target 70%+ of annotations)
- **Medium:** Noticeable difference but close call (20-25%)
- **Low:** Very similar, hard to decide (< 10%)

**If low confidence on >20% of annotations, request calibration session**

---

## 5️⃣ Edge Cases

### When Outputs Are Very Similar

**Scenario:** Both outputs are correct and nearly identical

**Action:**
- Look for subtle differences (parameter names, arg order)
- Prefer clearer/more explicit version
- If truly identical in substance → mark as "Tie"
- **Note:** Ties should be <15% of annotations

### When Both Outputs Are Wrong

**Scenario:** Neither output is correct or safe

**Action:**
- Choose "lesser evil" (which is closer to correct?)
- Tag both with rejection reasons
- Add note: "Both incorrect, chose less wrong option"
- **Example:** JSON error vs wrong tool → choose JSON error (fixable)

### When Outputs Use Different Approaches

**Scenario:** Output A: one tool, multiple params. Output B: multiple tools, simple params

**Action:**
- Both might be valid!
- Prefer approach that:
  1. Uses fewer tool calls
  2. Is more explicit/readable
  3. Is easier to debug
- Document reasoning clearly

### When Context Is Ambiguous

**Scenario:** User prompt is unclear or under-specified

**Action:**
- Prefer output that makes reasonable assumptions
- Prefer output that fails safely rather than guesses dangerously
- Tag with "ambiguous_prompt" flag
- Add note explaining what's unclear

### When Outputs Are Partial

**Scenario:** User asks for multi-step task, output shows only first step

**Action:**
- This might be intentional (models generate one step at a time)
- Evaluate based on: "Is this first step correct?"
- Don't penalize for not showing all future steps
- **Exception:** If output is clearly incomplete (mid-sentence), mark as worse

---

## 6️⃣ Quality Standards

### Inter-Annotator Agreement

**Target:** Cohen's κ ≥ 0.7 (substantial agreement)

**Monitoring:**
- Random 10% of annotations done by multiple annotators
- Monthly calibration sessions
- If κ drops below 0.6 → re-training required

### Annotation Speed

**Target:** 1 minute per comparison

**Guidelines:**
- 30-60 seconds = good pace
- <30 seconds = might be rushing, check quality
- >2 minutes = overthinking, trust your judgment

### Rejection Tag Usage

Track your tag distribution (should roughly match):

| Tag | Expected % | Meaning |
|-----|------------|---------|
| `correct_tool` | 60-70% | No issues |
| `wrong_tool` | 10-15% | Incorrect tool choice |
| `schema_fail` | 8-12% | Missing/wrong parameters |
| `verbose` | 5-10% | Unnecessarily complex |
| `style_off` | 5-8% | Style violations |
| `unsafe` | <2% | Guardrail violation |
| `ambiguous` | 3-5% | Unclear prompt/context |

**If your distribution differs significantly, discuss with trainer**

### Quality Checks

Random audits will check for:

- **Consistency:** Same prompt/output pairs should get same judgment
- **Accuracy:** Judgments align with objective criteria
- **Justification Quality:** Explanations are clear and specific
- **Tag Accuracy:** Tags match actual issues

---

## 7️⃣ Examples

### Example 1: Clear Winner (Tool Correctness)

**Prompt:** "Find all Python files in the project"

**Output A:**
```json
{"tool": "glob_file_search", "args": {"glob_pattern": "*.py"}}
```

**Output B:**
```json
{"tool": "search_files", "args": {"pattern": "*.py"}}
```

**Decision:** Output A  
**Reason:** `glob_file_search` is the correct tool name; `search_files` doesn't exist  
**Tags (B):** `wrong_tool`  
**Confidence:** High

---

### Example 2: Efficiency vs Clarity Trade-off

**Prompt:** "Read package.json and check if 'react' is a dependency"

**Output A:**
```json
{"tool": "read_file", "args": {"target_file": "package.json"}}
```

**Output B:**
```json
{
  "tool": "read_file",
  "args": {
    "target_file": "package.json"
  },
  "explanation": "Reading to check for react in dependencies"
}
```

**Decision:** Tie (or slight preference for B)  
**Reason:** Both correct; B adds helpful explanation without being verbose  
**Tags:** None  
**Confidence:** Medium

---

### Example 3: Style Violation

**Prompt:** "Create a new file called user-profile.ts"

**Output A:**
```json
{"tool": "write", "args": {"file_path": "user-profile.ts", "contents": ""}}
```

**Output B:**
```json
{"tool": "write", "args": {"file_path": "userProfile.ts", "contents": ""}}
```

**Decision:** Output A  
**Reason:** Preserves user's specified filename format (kebab-case)  
**Tags (B):** `style_off` (changed user's naming convention)  
**Confidence:** High

---

### Example 4: Minimal vs Complete

**Prompt:** "Search for the term 'TODO' in all JavaScript files"

**Output A:**
```json
{"tool": "grep", "args": {"pattern": "TODO", "type": "js"}}
```

**Output B:**
```json
{
  "tool": "grep",
  "args": {
    "pattern": "TODO",
    "type": "js",
    "output_mode": "content",
    "-i": false
  }
}
```

**Decision:** Output A  
**Reason:** B adds unnecessary default parameters (output_mode, -i are defaults)  
**Tags (B):** `verbose`  
**Confidence:** High

---

### Example 5: Both Wrong (Choose Lesser Evil)

**Prompt:** "Delete the temporary file /tmp/cache.json"

**Output A:**
```json
{"tool": "delete_file", "args": {"target_file": "/tmp/cache.json"}}
```

**Output B:**
```json
{"tool": "run_terminal_cmd", "args": {"command": "rm -rf /tmp/cache.json"}}
```

**Decision:** Output A  
**Reason:** Both might work, but A uses safer, purpose-built tool vs risky shell command  
**Tags (B):** `unsafe` (rm -rf is dangerous)  
**Confidence:** High

---

### Example 6: Ambiguous Prompt

**Prompt:** "Find the config file"

**Output A:**
```json
{"tool": "glob_file_search", "args": {"glob_pattern": "*config*"}}
```

**Output B:**
```json
{"tool": "glob_file_search", "args": {"glob_pattern": "config.{json,yaml,yml,js}"}}
```

**Decision:** Output B  
**Reason:** More specific; handles common config file extensions explicitly  
**Tags (A):** `ambiguous` (prompt didn't specify format)  
**Confidence:** Medium

---

### Example 7: Multi-Step Planning

**Prompt:** "Find all TODO comments in TypeScript files and count them"

**Output A:**
```json
{"tool": "grep", "args": {"pattern": "TODO", "type": "ts", "output_mode": "count"}}
```

**Output B:**
```json
{"tool": "grep", "args": {"pattern": "TODO", "type": "ts"}}
```
*[Implies second step would parse results]*

**Decision:** Output A  
**Reason:** Completes task in one efficient step using built-in count feature  
**Tags (B):** `verbose` (would need additional step)  
**Confidence:** High

---

## 🔧 Tools & Support

### Annotation Interface

- **URL:** [To be provided]
- **Login:** Individual credentials
- **Support:** [Contact info]

### Reference Materials

- **Tool Schema:** See [tool_schemas.json](./tool_schemas.json)
- **Style Guide:** See [Web4_Style_Guide.md](../Training/Web4_Style_Guide.md)
- **Common Tools:** Quick reference below

### Quick Tool Reference

| Tool | Primary Use | Key Parameters |
|------|-------------|----------------|
| `read_file` | Read file contents | `target_file` |
| `write` | Create/overwrite file | `file_path`, `contents` |
| `search_replace` | Edit file | `file_path`, `old_string`, `new_string` |
| `grep` | Search file contents | `pattern`, optional: `path`, `type` |
| `glob_file_search` | Find files by name | `glob_pattern` |
| `codebase_search` | Semantic code search | `query`, `target_directories` |
| `run_terminal_cmd` | Execute shell command | `command`, `is_background` |
| `list_dir` | List directory contents | `target_directory` |

---

## 📊 Your Progress

Track your annotation statistics:

- **Total Annotations:** [Shown in interface]
- **Agreement Rate:** [vs other annotators]
- **Average Time:** [per annotation]
- **Tag Distribution:** [breakdown of rejection reasons]

**Goal:** 500-1,500 high-quality annotations for Stage 1

---

## ❓ FAQ

**Q: What if I don't understand the prompt?**  
A: Tag with "ambiguous_prompt" and make your best judgment. Add note explaining what's unclear.

**Q: Can I mark both outputs as wrong?**  
A: Yes, but you must still choose which is "less wrong." Tag both with issues.

**Q: How often should outputs be "Tie"?**  
A: <15% of annotations. Try to pick a winner if reasonably possible.

**Q: What if I change my mind after submitting?**  
A: Contact supervisor to flag annotation for review. Include your annotation ID.

**Q: How long should my justification be?**  
A: 1-2 sentences. Be specific (e.g., "Output A uses correct tool; Output B tool doesn't exist")

**Q: Should I consider performance/speed?**  
A: Only if dramatically different (e.g., one approach is 10x slower). Usually focus on correctness first.

---

## 🔄 Feedback & Improvement

Your input helps improve these guidelines!

**Submit feedback on:**
- Unclear instructions
- Missing edge cases
- Tool reference errors
- Example requests

**Contact:** [To be provided]

---

**End of Annotation Guidelines**  
**Version:** 1.0  
**Date:** 2025-10-27

