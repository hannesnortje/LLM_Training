# Web4 LoRA Training Dataset Generator

## Overview

This automated dataset generator creates high-quality training data for Web4 LoRA fine-tuning across all required buckets with universal quality standards.

## Generated Datasets

### Total: ~23,000 examples

1. **Tool-Core (10,000 examples)** - Correct usage of Continue extension tools
2. **Tool-Negative (2,000 examples)** - Incorrect tool usage patterns for negative learning
3. **Style-Core (5,000 examples)** - Web4 coding conventions and component patterns
4. **Style-Refactor (3,000 examples)** - Code improvement and refactoring patterns
5. **Guardrail (2,000 examples)** - Safety and ethical compliance patterns
6. **Eval (1,000 examples)** - Comprehensive evaluation and testing examples

## Universal Quality Standards

All generated examples meet these requirements:

- ✅ **Valid JSONL format** (1 object per line)
- ✅ **Required fields present**: `task_type`, `instruction`, `input`, `output`
- ✅ **Token limit compliance**: < 2048 tokens per record
- ✅ **No parsing errors**: Valid JSON structure for tool calls
- ✅ **Tokenizer compatibility**: Works with Qwen/DeepSeek tokenizers
- ✅ **Format consistency**: Uniform structure across all buckets

## Usage

### Generate All Datasets

```bash
cd Training
python3 generate_web4_datasets.py
```

This will create a `data/` directory with 6 JSONL files:

```
data/
├── tool_core.jsonl       # 10,000 correct tool usage examples
├── tool_neg.jsonl        # 2,000 incorrect tool usage examples
├── style_core.jsonl      # 5,000 Web4 style examples
├── style_refactor.jsonl  # 3,000 refactoring examples
├── guardrail.jsonl       # 2,000 safety compliance examples
└── eval.jsonl            # 1,000 evaluation examples
```

### Output Format

Each JSONL file contains one JSON object per line with this structure:

```json
{
  "task_type": "tool_call|tool_neg|style_core|style_refactor|guardrail|eval",
  "instruction": "User's request or prompt",
  "input": "Context or additional information",
  "output": "Expected model response"
}
```

## Continue Extension Tools Covered

All 11 Continue extension tools are included in the training data:

1. `read_file` - Read file contents
2. `create_new_file` - Create new files
3. `run_terminal_command` - Execute terminal commands
4. `file_glob_search` - Search files by pattern
5. `view_diff` - View git differences
6. `read_currently_open_file` - Read active file
7. `ls` - List directory contents
8. `create_rule_block` - Create coding rules
9. `fetch_url_content` - Fetch web content
10. `edit_existing_file` - Edit existing files
11. `single_find_and_replace` - Find and replace operations

## Data Validation

The generator includes automatic validation:

- **Field Validation**: Ensures all required fields are present
- **JSON Validation**: Verifies tool call outputs are valid JSON
- **Token Count Validation**: Checks that examples stay under 2048 tokens
- **Format Consistency**: Ensures uniform structure across all examples

## Training Pipeline Integration

Use these datasets with the Web4 LoRA Training Pipeline:

1. **Dataset Sanity Check** - Validate all JSONL files
2. **Dry Run** - Test with 100 samples
3. **Mini Fine-Tune** - Train on 2-3k samples
4. **Full LoRA Training** - Use all 23k samples
5. **Evaluation** - Test with eval.jsonl
6. **Merge & Quantize** - Create deployable artifacts
7. **Deployment** - Use with Ollama or Docker Desktop Models

## File Sizes

Approximate file sizes:

- `tool_core.jsonl`: ~3.1 MB
- `tool_neg.jsonl`: ~450 KB
- `style_core.jsonl`: ~2.2 MB
- `style_refactor.jsonl`: ~1.6 MB
- `guardrail.jsonl`: ~1.1 MB
- `eval.jsonl`: ~330 KB

**Total: ~8.7 MB**

## Customization

To customize the generator:

1. Edit `generate_web4_datasets.py`
2. Modify example counts in the `generate_all_datasets()` method
3. Add new instruction templates in the `_get_tool_instruction()` method
4. Adjust validation rules in the `validate_examples()` method

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Quality Assurance

Each dataset bucket undergoes:

1. **Format Validation** - JSONL structure verification
2. **Content Validation** - JSON tool call structure checks
3. **Size Validation** - Token count limits
4. **Consistency Validation** - Uniform field presence

## Next Steps

After generation:

1. Run sanity check on all JSONL files
2. Test tokenization with Qwen/DeepSeek tokenizers
3. Validate random samples manually
4. Begin training pipeline with dry run
5. Monitor training metrics and adjust as needed

## Support

For issues or questions about the dataset generator, refer to:

- `Web4_LoRA_Training_Checklist.md` - Training pipeline overview
- `Web4_LoRA_Timing_and_Evaluation.md` - Timing and evaluation parameters
- `Web4_FineTuning_Dataset_Examples_Expanded.md` - Dataset examples and guidelines

