#!/usr/bin/env python3
"""
Web4 LoRA Training Dataset Generator
Generates high-quality training data for all dataset buckets with universal quality standards.
"""

import json
import random
from typing import Dict, List
from pathlib import Path


class Web4DatasetGenerator:
    def __init__(self):
        self.continue_tools = [
            "read_file", "create_new_file", "run_terminal_command", 
            "file_glob_search", "view_diff", "read_currently_open_file",
            "ls", "create_rule_block", "fetch_url_content", 
            "edit_existing_file", "single_find_and_replace"
        ]
        
        self.web4_components = [
            "Button", "Input", "Card", "Modal", "Header", "Footer", 
            "Sidebar", "Navigation", "Form", "Table", "List", "Grid"
        ]

    def generate_tool_core_examples(self, count: int = 10000) -> List[Dict]:
        """Generate Tool-Core examples for Continue extension tools"""
        examples = []
        examples_per_tool = count // len(self.continue_tools)
        
        for tool in self.continue_tools:
            for i in range(examples_per_tool):
                example = {
                    "task_type": "tool_call",
                    "instruction": self._get_tool_instruction(tool, i),
                    "input": self._get_context(i),
                    "output": self._get_correct_tool_call(tool, i)
                }
                examples.append(example)
        
        return examples

    def generate_tool_neg_examples(self, count: int = 2000) -> List[Dict]:
        """Generate Tool-Negative examples with various error patterns"""
        examples = []
        error_patterns = [
            "wrong_tool_selection",
            "malformed_parameters", 
            "missing_required_params",
            "wrong_parameter_types"
        ]
        
        examples_per_pattern = count // len(error_patterns)
        
        for pattern in error_patterns:
            for i in range(examples_per_pattern):
                tool = random.choice(self.continue_tools)
                example = {
                    "task_type": "tool_neg",
                    "instruction": self._get_tool_instruction(tool, i),
                    "input": self._get_context(i),
                    "output": self._get_incorrect_tool_call(tool, pattern, i)
                }
                examples.append(example)
        
        return examples

    def generate_style_core_examples(self, count: int = 5000) -> List[Dict]:
        """Generate Style-Core examples following Web4 conventions"""
        examples = []
        
        for i in range(count):
            component = self.web4_components[i % len(self.web4_components)]
            example = {
                "task_type": "style_core",
                "instruction": f"Create a {component} component following Web4 conventions",
                "input": "Building a React application with TypeScript",
                "output": self._get_web4_component(component)
            }
            examples.append(example)
        
        return examples

    def generate_style_refactor_examples(self, count: int = 3000) -> List[Dict]:
        """Generate Style-Refactor examples with improvement patterns"""
        examples = []
        refactor_types = [
            "modern JavaScript features",
            "performance improvements",
            "better maintainability",
            "functional programming principles"
        ]
        
        for i in range(count):
            refactor_type = refactor_types[i % len(refactor_types)]
            example = {
                "task_type": "style_refactor",
                "instruction": f"Refactor this code to use {refactor_type}",
                "input": "Legacy code that needs improvement",
                "output": self._get_refactored_code()
            }
            examples.append(example)
        
        return examples

    def generate_guardrail_examples(self, count: int = 2000) -> List[Dict]:
        """Generate Guardrail examples with safety patterns"""
        examples = []
        harmful_requests = [
            "Generate code that violates security best practices",
            "Create code that could be used for malicious purposes",
            "Write code that bypasses authentication",
            "Generate code that could cause data breaches"
        ]
        
        for i in range(count):
            instruction = harmful_requests[i % len(harmful_requests)]
            example = {
                "task_type": "guardrail",
                "instruction": instruction,
                "input": "User requesting potentially harmful code",
                "output": self._get_guardrail_response()
            }
            examples.append(example)
        
        return examples

    def generate_eval_examples(self, count: int = 1000) -> List[Dict]:
        """Generate Eval examples with test cases"""
        examples = []
        eval_types = [
            "tool calling functionality",
            "code quality and style",
            "guardrail compliance",
            "overall model performance"
        ]
        
        for i in range(count):
            eval_type = eval_types[i % len(eval_types)]
            example = {
                "task_type": "eval",
                "instruction": f"Test the {eval_type}",
                "input": "Comprehensive evaluation of model capabilities",
                "output": self._get_eval_response()
            }
            examples.append(example)
        
        return examples

    def _get_tool_instruction(self, tool: str, index: int) -> str:
        """Generate instructions for Continue tools"""
        instructions = {
            "read_file": [
                "Read the contents of src/components/Header.tsx",
                "Show me the main configuration file",
                "Open the package.json file"
            ],
            "create_new_file": [
                "Create a new React component called Button.tsx",
                "Make a new utility file for API calls",
                "Create a new test file for the UserService"
            ],
            "run_terminal_command": [
                "Install the required dependencies",
                "Run the test suite",
                "Start the development server"
            ],
            "file_glob_search": [
                "Find all TypeScript files in the src directory",
                "Search for components that import React",
                "Locate all test files"
            ],
            "view_diff": [
                "Show me what changed in the last commit",
                "Display the current git diff",
                "What files have been modified?"
            ],
            "read_currently_open_file": [
                "Show me the current file content",
                "Display what's in the active editor",
                "Read the file I'm currently working on"
            ],
            "ls": [
                "List the files in the current directory",
                "Show me what's in this folder",
                "Display the directory contents"
            ],
            "create_rule_block": [
                "Create a rule for code generation",
                "Add a new coding guideline",
                "Set up a rule for component structure"
            ],
            "fetch_url_content": [
                "Get the content from the API documentation",
                "Fetch the latest documentation",
                "Retrieve the content from the URL"
            ],
            "edit_existing_file": [
                "Update the component to use hooks",
                "Modify the function to handle errors",
                "Change the styling to use CSS modules"
            ],
            "single_find_and_replace": [
                "Replace all instances of 'var' with 'const'",
                "Change 'function' to 'arrow function'",
                "Replace 'class' with 'functional component'"
            ]
        }
        
        tool_instructions = instructions.get(tool, ["Generic instruction"])
        return tool_instructions[index % len(tool_instructions)]

    def _get_context(self, index: int) -> str:
        """Generate development context"""
        contexts = [
            "Working on a React project with TypeScript",
            "Developing a Node.js API with Express",
            "Building a Next.js application",
            "Working on a Python Django project",
            "Developing a Vue.js frontend application"
        ]
        return contexts[index % len(contexts)]

    def _get_correct_tool_call(self, tool: str, index: int) -> str:
        """Generate correct tool calls"""
        tool_calls = {
            "read_file": {
                "tool_calls": [{
                    "name": "read_file",
                    "parameters": {"path": "src/components/Header.tsx"}
                }]
            },
            "create_new_file": {
                "tool_calls": [{
                    "name": "create_new_file",
                    "parameters": {
                        "path": "src/components/Button.tsx",
                        "content": "import React from 'react';\\n\\nexport const Component = () => {\\n  return <div>Hello</div>;\\n};"
                    }
                }]
            },
            "run_terminal_command": {
                "tool_calls": [{
                    "name": "run_terminal_command",
                    "parameters": {
                        "command": "npm install",
                        "working_directory": "."
                    }
                }]
            },
            "file_glob_search": {
                "tool_calls": [{
                    "name": "file_glob_search",
                    "parameters": {"pattern": "src/**/*.ts"}
                }]
            },
            "view_diff": {
                "tool_calls": [{
                    "name": "view_diff",
                    "parameters": {}
                }]
            },
            "read_currently_open_file": {
                "tool_calls": [{
                    "name": "read_currently_open_file",
                    "parameters": {}
                }]
            },
            "ls": {
                "tool_calls": [{
                    "name": "ls",
                    "parameters": {"path": "."}
                }]
            },
            "create_rule_block": {
                "tool_calls": [{
                    "name": "create_rule_block",
                    "parameters": {"rule": "RULE: Use TypeScript for all new code"}
                }]
            },
            "fetch_url_content": {
                "tool_calls": [{
                    "name": "fetch_url_content",
                    "parameters": {"url": "https://docs.example.com/api"}
                }]
            },
            "edit_existing_file": {
                "tool_calls": [{
                    "name": "edit_existing_file",
                    "parameters": {
                        "path": "src/components/Button.tsx",
                        "changes": "Update imports to use TypeScript"
                    }
                }]
            },
            "single_find_and_replace": {
                "tool_calls": [{
                    "name": "single_find_and_replace",
                    "parameters": {
                        "file_path": "src/components/Button.tsx",
                        "find": "var",
                        "replace": "const"
                    }
                }]
            }
        }
        
        return json.dumps(tool_calls.get(tool, {}), indent=2)

    def _get_incorrect_tool_call(self, tool: str, error_pattern: str, index: int) -> str:
        """Generate incorrect tool calls"""
        if error_pattern == "wrong_tool_selection":
            wrong_tool = [t for t in self.continue_tools if t != tool][0]
            return json.dumps({
                "tool_calls": [{
                    "name": wrong_tool,
                    "parameters": {"path": "file.txt"}
                }]
            })
        elif error_pattern == "malformed_parameters":
            return json.dumps({
                "tool_calls": [{
                    "name": tool,
                    "parameters": {"file_path": "file.txt"}  # Wrong parameter name
                }]
            })
        elif error_pattern == "missing_required_params":
            return json.dumps({
                "tool_calls": [{
                    "name": tool,
                    "parameters": {}  # Missing required parameters
                }]
            })
        elif error_pattern == "wrong_parameter_types":
            return json.dumps({
                "tool_calls": [{
                    "name": tool,
                    "parameters": {"path": 123}  # Wrong type
                }]
            })
        return "Invalid JSON structure"

    def _get_web4_component(self, component: str) -> str:
        """Generate Web4-style component code"""
        return f"""import React from 'react';
import {{ {component}Props }} from './types';

export const {component}: React.FC<{component}Props> = ({{
  className = '',
  children,
  ...props
}}) => {{
  return (
    <div className={{className}} {{...props}}>
      {{children}}
    </div>
  );
}};

export default {component};"""

    def _get_refactored_code(self) -> str:
        """Generate refactored code examples"""
        return """// Before: Legacy code
function oldFunction(data) {
  var result = [];
  for (var i = 0; i < data.length; i++) {
    if (data[i].active) {
      result.push(data[i].name);
    }
  }
  return result;
}

// After: Modern refactored code
const getActiveNames = (data: User[]): string[] => 
  data
    .filter(user => user.active)
    .map(user => user.name);"""

    def _get_guardrail_response(self) -> str:
        """Generate guardrail refusal responses"""
        return """<REFUSAL>
I cannot help with generating code that violates security best practices or could be used for malicious purposes.

Instead, I can help you with:
- Secure coding practices
- Authentication and authorization best practices
- Data protection and privacy compliance
- Ethical software development

Please let me know how I can assist you with secure and ethical code development.
</REFUSAL>"""

    def _get_eval_response(self) -> str:
        """Generate eval responses"""
        return """{
  "tool_calls": [{
    "name": "evaluate_model",
    "parameters": {
      "metrics": ["accuracy", "performance", "safety"],
      "threshold": 0.95
    }
  }]
}"""

    def validate_examples(self, examples: List[Dict]) -> List[Dict]:
        """Validate generated examples"""
        valid_examples = []
        
        for example in examples:
            # Check required fields
            if not all(field in example for field in ["task_type", "instruction", "input", "output"]):
                continue
            
            # Check JSON validity for tool calls
            if example["task_type"] in ["tool_call", "tool_neg"]:
                try:
                    json.loads(example["output"])
                except json.JSONDecodeError:
                    continue
            
            # Basic token count check
            total_text = f"{example['instruction']} {example['input']} {example['output']}"
            if len(total_text.split()) > 2048:
                continue
            
            valid_examples.append(example)
        
        return valid_examples

    def save_to_jsonl(self, examples: List[Dict], filename: str):
        """Save examples to JSONL file"""
        with open(filename, 'w', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')

    def generate_all_datasets(self, output_dir: str = "data"):
        """Generate all dataset buckets"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print("🚀 Generating Web4 training datasets...")
        print("=" * 60)
        
        # Generate Tool-Core examples
        print("\n📊 Generating Tool-Core examples...")
        tool_core = self.generate_tool_core_examples(10000)
        tool_core_valid = self.validate_examples(tool_core)
        self.save_to_jsonl(tool_core_valid, output_path / "tool_core.jsonl")
        print(f"   ✅ Generated {len(tool_core_valid)} Tool-Core examples")
        
        # Generate Tool-Negative examples
        print("\n📊 Generating Tool-Negative examples...")
        tool_neg = self.generate_tool_neg_examples(2000)
        tool_neg_valid = self.validate_examples(tool_neg)
        self.save_to_jsonl(tool_neg_valid, output_path / "tool_neg.jsonl")
        print(f"   ✅ Generated {len(tool_neg_valid)} Tool-Negative examples")
        
        # Generate Style-Core examples
        print("\n📊 Generating Style-Core examples...")
        style_core = self.generate_style_core_examples(5000)
        style_core_valid = self.validate_examples(style_core)
        self.save_to_jsonl(style_core_valid, output_path / "style_core.jsonl")
        print(f"   ✅ Generated {len(style_core_valid)} Style-Core examples")
        
        # Generate Style-Refactor examples
        print("\n📊 Generating Style-Refactor examples...")
        style_refactor = self.generate_style_refactor_examples(3000)
        style_refactor_valid = self.validate_examples(style_refactor)
        self.save_to_jsonl(style_refactor_valid, output_path / "style_refactor.jsonl")
        print(f"   ✅ Generated {len(style_refactor_valid)} Style-Refactor examples")
        
        # Generate Guardrail examples
        print("\n📊 Generating Guardrail examples...")
        guardrail = self.generate_guardrail_examples(2000)
        guardrail_valid = self.validate_examples(guardrail)
        self.save_to_jsonl(guardrail_valid, output_path / "guardrail.jsonl")
        print(f"   ✅ Generated {len(guardrail_valid)} Guardrail examples")
        
        # Generate Eval examples
        print("\n📊 Generating Eval examples...")
        eval_examples = self.generate_eval_examples(1000)
        eval_valid = self.validate_examples(eval_examples)
        self.save_to_jsonl(eval_valid, output_path / "eval.jsonl")
        print(f"   ✅ Generated {len(eval_valid)} Eval examples")
        
        # Generate summary
        total_examples = (len(tool_core_valid) + len(tool_neg_valid) + 
                         len(style_core_valid) + len(style_refactor_valid) + 
                         len(guardrail_valid) + len(eval_valid))
        
        print("\n" + "=" * 60)
        print("📈 DATASET GENERATION SUMMARY")
        print("=" * 60)
        print(f"   Tool-Core:        {len(tool_core_valid):>6} examples")
        print(f"   Tool-Negative:    {len(tool_neg_valid):>6} examples")
        print(f"   Style-Core:       {len(style_core_valid):>6} examples")
        print(f"   Style-Refactor:   {len(style_refactor_valid):>6} examples")
        print(f"   Guardrail:        {len(guardrail_valid):>6} examples")
        print(f"   Eval:             {len(eval_valid):>6} examples")
        print("   " + "-" * 30)
        print(f"   TOTAL:            {total_examples:>6} examples")
        print("=" * 60)
        print(f"\n✨ Dataset generation complete!")
        print(f"📁 Files saved to: {output_dir}/")
        
        return {
            "tool_core": len(tool_core_valid),
            "tool_neg": len(tool_neg_valid),
            "style_core": len(style_core_valid),
            "style_refactor": len(style_refactor_valid),
            "guardrail": len(guardrail_valid),
            "eval": len(eval_valid),
            "total": total_examples
        }


def main():
    generator = Web4DatasetGenerator()
    results = generator.generate_all_datasets("data")


if __name__ == "__main__":
    main()

