# Web4 Complete LoRA Training Strategy
## Train Everything → RAG for Daily Accumulation Only

**Date**: 2025-10-27  
**Repository**: Web4Articles (`/media/hannesn/storage/Code/CeruleanCircle/Web4Articles/Web4Articles`)  
**Objective**: Train comprehensive Web4 knowledge into LoRA adapter; Use RAG only for transient daily accumulation and session context  
**Philosophy**: Train 90%, RAG 10% — Invert the misconception that "process is trained, content is RAG'd"

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [The Core Philosophy: Train Everything](#the-core-philosophy-train-everything)
3. [RAG's True Role: Daily Accumulation Buffer](#rags-true-role-daily-accumulation-buffer)
4. [Training Data Architecture](#training-data-architecture)
5. [Extraction Strategy from Web4Articles](#extraction-strategy-from-web4articles)
6. [Training Pipeline: 90/10 Framework](#training-pipeline-9010-framework)
7. [Evening Training Loop](#evening-training-loop)
8. [Evaluation & Quality Gates](#evaluation--quality-gates)
9. [RL Add-On (Optional Stage)](#rl-add-on-optional-stage)
10. [Deployment Architecture](#deployment-architecture)
11. [Implementation Roadmap](#implementation-roadmap)

---

## Executive Summary

### The Correct Mental Model

**WRONG** (from the rejected strategy):
```
✗ Train: "The Process" (PDCA structure, CMM framework, Web4 patterns)
✗ RAG: "The Products" (Historical PDCAs, component implementations)
✗ Result: Model knows structure but lacks domain knowledge
```

**CORRECT** (This Strategy):
```
✓ Train: EVERYTHING (Process + Patterns + Historical Knowledge + Components + PDCAs)
✓ RAG: Daily Accumulation Buffer + True Transients (today's work, session context)
✓ Result: Model is domain expert; RAG provides fresh context
```

### The Key Insight

**You were right to reject the "factory process" analogy.** Here's why:

1. **Factory workers** learn procedures because products change constantly (different customers, different specs)
2. **Web4 development** has stable patterns AND stable historical knowledge that should be internalized
3. **The AI should be a domain expert**, not just a process follower

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    BASE MODEL (Qwen 7B)                      │
│                   Cold start, no context                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              LORA ADAPTER (Trained Nightly)                  │
│                                                               │
│  • All PDCA patterns and structures (v3.2.4.2)              │
│  • All CMM1-4 framework knowledge                            │
│  • All Web4 architectural patterns                           │
│  • ALL historical PDCAs (1,908 documents)                   │
│  • ALL component implementations (3,714 files)              │
│  • ALL key lessons and verification checklists              │
│  • ALL role-specific processes                              │
│  • ALL violations and compliance rules                      │
│                                                               │
│  Size: ~40,000 training samples                             │
│  Coverage: Complete Web4 domain knowledge                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              RAG VECTOR DB (Daily Buffer)                    │
│                                                               │
│  • Today's PDCAs (accumulating during day)                  │
│  • Current session context (active work)                    │
│  • User preferences (this session)                          │
│  • Pending decisions (not yet committed)                    │
│  • Draft work (not yet merged)                              │
│                                                               │
│  Cleared: Every evening after training update               │
│  Purpose: Bridge between last training and next             │
└─────────────────────────────────────────────────────────────┘
```

### Training Philosophy: 90% / 10%

**90% of Work** = Data curation, validation, schema design, evaluation infrastructure  
**10% of Work** = Actual training execution (overnight process)

But **100% of stable knowledge** goes into the adapter.

---

## The Core Philosophy: Train Everything

### What Gets Trained (Comprehensive)

#### Tier 1: Process Knowledge (Previously Thought to be "Train Only")
```python
PROCESS_KNOWLEDGE = [
    # PDCA Structure
    "README.md",                                    # 12-step startup
    "template.md v3.2.4.2",                        # Official structure
    "howto.PDCA.md",                               # Creation rules
    "PDCA.howto.decide.md",                        # TRON framework
    
    # CMM Framework  
    "howto.cmm.md",                                # CMM1-4 definitions
    "cmm3.compliance.checklist.md",                # Compliance rules
    
    # Web4 Architecture
    "architecture/components.md",                   # Component principles
    "tech-stack.md",                               # Vitest only, Jest banned
    "Web4TSComponent patterns",                     # 5-layer architecture
    
    # Code Stereotypes
    "Empty constructor pattern",                    # Radical OOP
    "Scenario-based state",                        # State management
    "Dual link format",                            # Documentation links
]
```

#### Tier 2: Historical Knowledge (Now Trained, Not RAG'd)
```python
HISTORICAL_KNOWLEDGE = [
    # ALL Historical PDCAs → Training samples
    "scrum.pmo/project.journal/*/*/*.pdca.md",     # ~1,908 PDCAs
    
    # ALL Component Implementations → Training samples  
    "components/*/src/ts/layer2/*.ts",             # ~1,200 implementations
    "components/*/src/ts/layer3/*.ts",             # ~800 interfaces
    "components/*/src/ts/layer5/*.ts",             # ~400 CLI implementations
    
    # ALL Role Processes → Training samples
    "scrum.pmo/roles/*/process.md",                # ~238 process docs
    "scrum.pmo/roles/*/quick-reference.md",        # Quick guides
    
    # ALL Violations → Training samples (guardrails)
    "Radical OOP violations and fixes",            # Architectural enforcement
    "Jest usage violations",                       # Tech stack compliance
    "Manual cp violations",                        # CMM3 compliance
]
```

#### Tier 3: Key Lessons & Checklists (Trained as Reinforcement)
```python
KEY_LESSONS = [
    "🔴 ALWAYS read CMM4 framework FIRST",
    "✅ Use web4tscomponent for version control - NEVER manual cp/mkdir",
    "✅ Validate dual links before session end",
    "✅ Empty Constructor Pattern: No logic in constructor",
    "✅ Scenario Support: Components MUST implement init() and toScenario()",
    "❌ Jest is BANNED: Use Vitest exclusively",
    "⚠️ 'Show me' = show + STOP, not show + analyze + implement",
    # ... All 50+ key lessons from trainAI
]

VERIFICATION_CHECKLISTS = [
    "startup_checklist",      # 12-step protocol
    "pdca_checklist",         # Document creation
    "component_checklist",    # Version management
    "cmm3_checklist",         # Compliance verification
    "link_validation_checklist", # Dual link validation
]
```

### Why Train Everything?

**1. Latency**: Trained knowledge is instant; RAG requires retrieval (50-200ms overhead)

**2. Coherence**: Trained model has unified understanding; RAG snippets may conflict

**3. Capacity**: Modern LoRA can handle 40K+ samples efficiently on M1 Mac

**4. Quality**: Trained knowledge is compressed and generalized; RAG is verbatim

**5. Reliability**: No dependency on vector search quality or embedding model

---

## RAG's True Role: Daily Accumulation Buffer

### What RAG Actually Holds (Minimal, Transient)

```python
RAG_DAILY_BUFFER = {
    'todays_pdcas': {
        'type': 'accumulating',
        'description': 'PDCAs created today (not yet trained)',
        'lifecycle': 'Created during day → Trained at night → Removed from RAG',
        'example': 'User creates 2025-10-27-UTC-1445.pdca.md at 2:45 PM'
    },
    
    'current_session': {
        'type': 'transient',
        'description': 'Active session state (current work)',
        'lifecycle': 'Created at session start → Used during session → Cleared at session end',
        'example': 'Branch: dev/2025-10-27-UTC-0747, Last commit: abc123'
    },
    
    'user_preferences': {
        'type': 'transient',
        'description': 'Session-specific user preferences',
        'lifecycle': 'Set during session → Used during session → Cleared at session end',
        'example': 'User prefers concise responses today'
    },
    
    'pending_decisions': {
        'type': 'transient',
        'description': 'Decisions waiting for user confirmation',
        'lifecycle': 'Created during decision point → Resolved → Removed',
        'example': 'Waiting for user to approve component version bump'
    },
    
    'draft_work': {
        'type': 'transient',
        'description': 'Uncommitted code or documents',
        'lifecycle': 'Created during session → Committed → Removed from RAG',
        'example': 'Draft PDCA in progress, not yet saved'
    }
}
```

### The Evening Training Loop

**Daily Cycle**:
```
8:00 AM  - Model loads with last night's training (includes all work up to yesterday)
         - RAG is empty (cleared after last training)
         
10:00 AM - User creates 2025-10-27-UTC-1000.pdca.md
         - Added to RAG (model doesn't know this yet)
         
2:00 PM  - User creates 2025-10-27-UTC-1400.pdca.md
         - Added to RAG (model still doesn't know first PDCA)
         
5:00 PM  - Work day ends
         - RAG contains: 2 PDCAs, session context, user preferences
         
8:00 PM  - Evening training starts automatically
         - Extracts today's PDCAs from RAG
         - Adds to training dataset
         - Trains new LoRA adapter (incremental)
         - Deploys updated model
         
11:00 PM - Training complete
         - Model now knows today's 2 PDCAs
         - RAG cleared (daily buffer reset)
         
Next Day - Cycle repeats with updated model
```

### What NEVER Goes in RAG

```python
NEVER_RAG = [
    "Historical PDCAs",           # These are trained
    "Component implementations",  # These are trained
    "CMM framework",              # This is trained
    "Web4 patterns",              # These are trained
    "Key lessons",                # These are trained
    "Verification checklists",    # These are trained
    "Process documentation",      # This is trained
]
```

---

## Training Data Architecture

### Total Dataset Size: ~40,000 Samples

```
Dataset Composition (Aligned with 90/10 Framework):

├── Tool-Core (tool_core.jsonl)                 10,000 samples
│   Purpose: Continue extension tool mastery
│   Source: Existing generator (already complete)
│   
├── Tool-Negative (tool_neg.jsonl)               2,000 samples
│   Purpose: Negative examples for tool use
│   Source: Existing generator (already complete)
│
├── Style-Core (style_core.jsonl)               15,000 samples ★★★
│   Purpose: Web4 component patterns from REAL codebase
│   Source: EXTRACT from components/*/src/ts/
│   Includes: Empty constructors, 5-layer arch, scenario patterns
│
├── PDCA-Structure (pdca_structure.jsonl)        5,000 samples ★★★
│   Purpose: Complete PDCA creation patterns
│   Source: EXTRACT from scrum.pmo/project.journal/
│   Includes: Template v3.2.4.2, TRON format, dual links
│
├── PDCA-Historical (pdca_historical.jsonl)      3,000 samples ★★★
│   Purpose: Historical PDCA knowledge and context
│   Source: EXTRACT diverse PDCAs showing different scenarios
│   Includes: Startup, component creation, refactoring, debugging
│
├── Style-Refactor (style_refactor.jsonl)        3,000 samples
│   Purpose: Code improvement and evolution patterns
│   Source: EXTRACT from PDCAs showing refactoring journeys
│   
├── Guardrails (guardrail.jsonl)                 2,000 samples ★★★
│   Purpose: Compliance and violation patterns
│   Source: EXTRACT from violation PDCAs + compliance docs
│   Includes: Jest ban, manual cp ban, OOP violations
│
└── Evaluation (eval.jsonl)                      1,000 samples
    Purpose: Hold-out test set (NEVER trained)
    Source: Recent high-quality PDCAs and components
    Usage: Post-training quality gate

TOTAL: 41,000 samples (~25-30M tokens)
Optimized for: Mac M1 32GB RAM (MPS backend)
Training Time: 12-18 hours (full) / 2-4 hours (incremental nightly)
```

### Sample Distribution by Knowledge Type

```python
SAMPLE_BREAKDOWN = {
    'process_knowledge': {
        'samples': 7000,
        'buckets': ['pdca_structure', 'guardrails'],
        'coverage': 'PDCA format, TRON, CMM framework, compliance'
    },
    
    'code_patterns': {
        'samples': 18000,
        'buckets': ['style_core', 'style_refactor'],
        'coverage': 'Web4 architecture, empty constructors, scenarios, layer separation'
    },
    
    'tool_mastery': {
        'samples': 12000,
        'buckets': ['tool_core', 'tool_neg'],
        'coverage': 'Continue extension tools, file operations, git commands'
    },
    
    'historical_knowledge': {
        'samples': 3000,
        'buckets': ['pdca_historical'],
        'coverage': 'Real problem-solving patterns, debugging journeys, architectural decisions'
    },
    
    'compliance_enforcement': {
        'samples': 2000,
        'buckets': ['guardrails'],
        'coverage': 'Jest ban, manual operations ban, security rules'
    }
}
```

---

## Extraction Strategy from Web4Articles

### Phase 1: Style Core Extraction (15,000 samples)

**Source**: `components/*/src/ts/` from Web4Articles repository

**Extraction Targets**:
```python
STYLE_CORE_EXTRACTION = {
    'component_patterns': {
        'target': 8000,
        'sources': [
            'components/Unit/0.3.0.6/src/ts/layer2/DefaultUnit.ts',
            'components/PDCA/0.2.3.0/src/ts/layer2/DefaultPDCA.ts',
            'components/Web4Test/0.1.0.0/src/ts/layer2/DefaultWeb4Test.ts',
            'components/Web4Requirement/0.3.0.5/src/ts/layer2/DefaultRequirement.ts',
            # ... all ~1,200 layer2 implementations
        ],
        'patterns': [
            'Empty constructor with no logic',
            'init() method for scenario-based initialization',
            'toScenario() method for state serialization',
            'Private model field pattern',
            'Method chaining with "return this"'
        ]
    },
    
    'interface_definitions': {
        'target': 4000,
        'sources': [
            'components/*/src/ts/layer3/*.ts',  # ~800 interfaces
        ],
        'patterns': [
            'Interface naming (IComponent pattern)',
            'Method signatures',
            'Type parameters',
            'Documentation patterns'
        ]
    },
    
    'cli_implementations': {
        'target': 2000,
        'sources': [
            'components/*/src/ts/layer5/*.ts',  # ~400 CLI files
        ],
        'patterns': [
            'CLI entry points',
            'Argument parsing',
            'Error handling',
            'Output formatting'
        ]
    },
    
    'test_patterns': {
        'target': 1000,
        'sources': [
            'components/*/test/**/*.test.ts',
        ],
        'patterns': [
            'Vitest test structure',
            'Describe/it blocks',
            'Expect assertions',
            'Mock patterns'
        ]
    }
}
```

**Extraction Script**: `scripts/extract_style_core.py`

```python
#!/usr/bin/env python3
"""
Extract Web4 component patterns from Web4Articles codebase.
Generates style_core.jsonl with 15,000 training samples.
"""

import json
from pathlib import Path
from typing import List, Dict
import re

class StyleCoreExtractor:
    def __init__(self, web4_repo: str):
        self.web4_repo = Path(web4_repo)
        self.samples = []
    
    def extract_all(self) -> List[Dict]:
        """Extract all style core patterns"""
        self.extract_component_patterns()      # 8,000 samples
        self.extract_interface_definitions()   # 4,000 samples
        self.extract_cli_implementations()     # 2,000 samples
        self.extract_test_patterns()           # 1,000 samples
        return self.samples
    
    def extract_component_patterns(self):
        """Extract layer2 component implementations"""
        layer2_files = self.web4_repo.glob('components/*/src/ts/layer2/*.ts')
        
        for file_path in layer2_files:
            content = file_path.read_text()
            
            # Extract class definition
            class_match = self.extract_class_definition(content)
            if class_match:
                sample = {
                    'task_type': 'style_sft',
                    'instruction': f'Create a Web4 component class following {file_path.stem} pattern',
                    'input': f'Component with empty constructor, init(), toScenario() methods',
                    'output': class_match
                }
                self.samples.append(sample)
            
            # Extract empty constructor
            constructor = self.extract_empty_constructor(content)
            if constructor:
                sample = {
                    'task_type': 'style_sft',
                    'instruction': 'Create a Web4-compliant empty constructor',
                    'input': 'No logic in constructor, only model initialization',
                    'output': constructor
                }
                self.samples.append(sample)
            
            # Extract init() method
            init_method = self.extract_init_method(content)
            if init_method:
                sample = {
                    'task_type': 'style_sft',
                    'instruction': 'Implement Web4 init() method for scenario-based initialization',
                    'input': 'Initialize component from scenario with model merging',
                    'output': init_method
                }
                self.samples.append(sample)
    
    def extract_class_definition(self, content: str) -> str:
        """Extract complete class definition"""
        # Regex to match: export class DefaultXXX implements XXX {
        pattern = r'export class Default\w+ implements \w+.*?\n\}'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0) if match else None
    
    def extract_empty_constructor(self, content: str) -> str:
        """Extract empty constructor pattern"""
        pattern = r'constructor\(\)\s*\{\s*this\.model\s*=\s*\{[^}]+\};\s*\}'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0) if match else None
    
    def extract_init_method(self, content: str) -> str:
        """Extract init() method"""
        pattern = r'init\(scenario: Scenario<\w+>\): this \{\s*.*?\s*return this;\s*\}'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0) if match else None
    
    def save(self, output_path: str):
        """Save as JSONL"""
        with open(output_path, 'w') as f:
            for sample in self.samples:
                f.write(json.dumps(sample) + '\n')

if __name__ == '__main__':
    extractor = StyleCoreExtractor('/media/hannesn/storage/Code/CeruleanCircle/Web4Articles/Web4Articles')
    extractor.extract_all()
    extractor.save('data/style_core.jsonl')
    print(f'✅ Extracted {len(extractor.samples)} style core samples')
```

### Phase 2: PDCA Structure Extraction (5,000 samples)

**Source**: `scrum.pmo/project.journal/` from Web4Articles

**Extraction Targets**:
```python
PDCA_STRUCTURE_EXTRACTION = {
    'complete_pdcas': {
        'target': 2000,
        'sources': [
            'scrum.pmo/project.journal/*/2025-*.pdca.md',  # Recent high-quality PDCAs
        ],
        'selection': 'PDCAs with CMM3 badge, complete structure, no errors',
        'format': 'Full PDCA as training example'
    },
    
    'tron_format': {
        'target': 1500,
        'sources': 'Extract TRON sections from PDCAs',
        'patterns': [
            'Trigger (verbatim user quote)',
            'Response (structured plan)',
            'Outcome (expected result)',
            'Next (follow-up steps)'
        ]
    },
    
    'dual_links': {
        'target': 1000,
        'sources': 'Extract link sections from PDCAs',
        'patterns': [
            '[GitHub](URL) | [§/path](path) format',
            'Backward link to previous PDCA',
            'Forward placeholder link'
        ]
    },
    
    'metadata': {
        'target': 500,
        'sources': 'Extract PDCA headers',
        'patterns': [
            'Agent name and role',
            'Date and timestamp',
            'Objective and template version',
            'Branch and sync requirements'
        ]
    }
}
```

**Extraction Script**: `scripts/extract_pdca_structure.py`

```python
#!/usr/bin/env python3
"""
Extract PDCA structure patterns from Web4Articles project journal.
Generates pdca_structure.jsonl with 5,000 training samples.
"""

import json
from pathlib import Path
from typing import List, Dict
import re
from datetime import datetime

class PDCAStructureExtractor:
    def __init__(self, web4_repo: str):
        self.web4_repo = Path(web4_repo)
        self.samples = []
    
    def extract_all(self) -> List[Dict]:
        """Extract all PDCA structure patterns"""
        self.extract_complete_pdcas()      # 2,000 samples
        self.extract_tron_patterns()       # 1,500 samples
        self.extract_dual_links()          # 1,000 samples
        self.extract_metadata_patterns()   # 500 samples
        return self.samples
    
    def extract_complete_pdcas(self):
        """Extract complete PDCA documents as training samples"""
        pdca_dir = self.web4_repo / 'scrum.pmo' / 'project.journal'
        pdca_files = list(pdca_dir.glob('*/2025-*.pdca.md'))
        
        # Select high-quality PDCAs (CMM3, complete structure)
        quality_pdcas = self.filter_quality_pdcas(pdca_files)
        
        for pdca_path in quality_pdcas[:2000]:
            content = pdca_path.read_text()
            metadata = self.extract_pdca_metadata(content)
            
            sample = {
                'task_type': 'pdca_structure',
                'instruction': 'Create a PDCA document following template v3.2.4.2',
                'input': f'Objective: {metadata.get("objective", "N/A")}. Agent: {metadata.get("agent_name", "N/A")}. Role: {metadata.get("agent_role", "N/A")}',
                'output': content
            }
            self.samples.append(sample)
    
    def filter_quality_pdcas(self, pdca_files: List[Path]) -> List[Path]:
        """Filter for high-quality PDCAs"""
        quality = []
        for pdca_path in pdca_files:
            content = pdca_path.read_text()
            
            # Check for CMM3 badge
            if 'CMM3 COMPLETE' not in content:
                continue
            
            # Check for complete structure
            required_sections = ['PLAN', 'DO', 'CHECK', 'ACT']
            if not all(section in content for section in required_sections):
                continue
            
            # Check for TRON format
            if 'Trigger' not in content or 'Response' not in content:
                continue
            
            quality.append(pdca_path)
        
        return quality
    
    def extract_pdca_metadata(self, content: str) -> Dict:
        """Extract metadata from PDCA header"""
        metadata = {}
        
        # Extract objective
        obj_match = re.search(r'\*\*🎯 Objective:\*\* (.+)', content)
        if obj_match:
            metadata['objective'] = obj_match.group(1).strip()
        
        # Extract agent name
        agent_match = re.search(r'\*\*👤 Agent Name:\*\* (.+)', content)
        if agent_match:
            metadata['agent_name'] = agent_match.group(1).strip()
        
        # Extract agent role
        role_match = re.search(r'\*\*👤 Agent Role:\*\* (.+)', content)
        if role_match:
            metadata['agent_role'] = role_match.group(1).strip()
        
        return metadata
    
    def extract_tron_patterns(self):
        """Extract TRON format examples"""
        pdca_dir = self.web4_repo / 'scrum.pmo' / 'project.journal'
        pdca_files = list(pdca_dir.glob('*/2025-*.pdca.md'))
        
        for pdca_path in pdca_files:
            content = pdca_path.read_text()
            
            # Extract TRON sections
            tron = self.extract_tron_section(content)
            if tron:
                sample = {
                    'task_type': 'pdca_reasoning',
                    'instruction': 'Apply TRON format to structure a user request and response',
                    'input': tron.get('trigger', ''),
                    'output': self.format_tron(tron)
                }
                self.samples.append(sample)
    
    def extract_tron_section(self, content: str) -> Dict:
        """Extract TRON format from PDCA"""
        tron = {}
        
        # Extract Trigger
        trigger_match = re.search(r'\*\*Trigger \(Verbatim\):\*\*\s*>\s*"([^"]+)"', content)
        if trigger_match:
            tron['trigger'] = trigger_match.group(1)
        
        # Extract Response
        response_match = re.search(r'\*\*Response:\*\*\s*(.*?)\n\n\*\*Outcome:', content, re.DOTALL)
        if response_match:
            tron['response'] = response_match.group(1).strip()
        
        # Extract Outcome
        outcome_match = re.search(r'\*\*Outcome:\*\*\s*(.*?)\n\n\*\*Next:', content, re.DOTALL)
        if outcome_match:
            tron['outcome'] = outcome_match.group(1).strip()
        
        # Extract Next
        next_match = re.search(r'\*\*Next:\*\*\s*(.*?)(?:\n\n|\Z)', content, re.DOTALL)
        if next_match:
            tron['next'] = next_match.group(1).strip()
        
        return tron if len(tron) == 4 else None
    
    def format_tron(self, tron: Dict) -> str:
        """Format TRON as training output"""
        return f"""### TRON Format:

**Trigger (Verbatim):**
> "{tron['trigger']}"

**Response:**
{tron['response']}

**Outcome:**
{tron['outcome']}

**Next:**
{tron['next']}"""
    
    def extract_dual_links(self):
        """Extract dual link patterns"""
        pdca_dir = self.web4_repo / 'scrum.pmo' / 'project.journal'
        pdca_files = list(pdca_dir.glob('*/2025-*.pdca.md'))
        
        for pdca_path in pdca_files:
            content = pdca_path.read_text()
            
            # Extract link section
            link_match = re.search(r'\*\*🔗 Previous PDCA:\*\* (.+)', content)
            if link_match:
                dual_link = link_match.group(1)
                
                sample = {
                    'task_type': 'pdca_structure',
                    'instruction': 'Create a dual link in PDCA format',
                    'input': 'Link to previous PDCA: 2025-10-26-UTC-1245.pdca.md',
                    'output': dual_link
                }
                self.samples.append(sample)
    
    def extract_metadata_patterns(self):
        """Extract PDCA metadata patterns"""
        # Implementation similar to above
        pass
    
    def save(self, output_path: str):
        """Save as JSONL"""
        with open(output_path, 'w') as f:
            for sample in self.samples:
                f.write(json.dumps(sample) + '\n')

if __name__ == '__main__':
    extractor = PDCAStructureExtractor('/media/hannesn/storage/Code/CeruleanCircle/Web4Articles/Web4Articles')
    extractor.extract_all()
    extractor.save('data/pdca_structure.jsonl')
    print(f'✅ Extracted {len(extractor.samples)} PDCA structure samples')
```

### Phase 3: PDCA Historical Extraction (3,000 samples)

**Purpose**: Train the model on real problem-solving patterns from historical PDCAs

**Selection Criteria**:
```python
HISTORICAL_PDCA_SELECTION = {
    'startup_pdcas': {
        'target': 500,
        'query': 'PDCAs showing 12-step startup protocol',
        'value': 'Teach startup patterns and agent initialization'
    },
    
    'component_creation': {
        'target': 500,
        'query': 'PDCAs showing web4tscomponent usage',
        'value': 'Teach component versioning and creation'
    },
    
    'debugging_sessions': {
        'target': 500,
        'query': 'PDCAs showing error investigation and resolution',
        'value': 'Teach debugging methodology'
    },
    
    'refactoring_journeys': {
        'target': 500,
        'query': 'PDCAs showing code refactoring (CMM2→CMM3)',
        'value': 'Teach architectural improvements'
    },
    
    'violation_discoveries': {
        'target': 500,
        'query': 'PDCAs discovering and fixing violations',
        'value': 'Teach compliance enforcement'
    },
    
    'integration_work': {
        'target': 500,
        'query': 'PDCAs showing component integration',
        'value': 'Teach system integration patterns'
    }
}
```

### Phase 4: Guardrails Extraction (2,000 samples)

**Source**: Violation PDCAs + Compliance documents

```python
GUARDRAILS_EXTRACTION = {
    'jest_ban': {
        'target': 400,
        'sources': [
            'docs/tech-stack.md',
            'PDCAs mentioning Jest removal'
        ],
        'pattern': '<REFUSAL> Jest is banned. Use Vitest exclusively per docs/tech-stack.md.'
    },
    
    'manual_operations': {
        'target': 400,
        'sources': [
            'cmm3.compliance.checklist.md',
            'PDCAs showing manual cp violations'
        ],
        'pattern': '<REFUSAL> Use web4tscomponent for all version operations. Manual copy violates CMM3.'
    },
    
    'oop_violations': {
        'target': 400,
        'sources': [
            'Radical OOP violation discovery PDCAs'
        ],
        'pattern': '<REFUSAL> Web4 requires Radical OOP. No standalone functions - use class methods only.'
    },
    
    'security_violations': {
        'target': 400,
        'sources': [
            'Security compliance docs'
        ],
        'pattern': '<REFUSAL> Security violation: [specific violation]. Use [correct approach] instead.'
    },
    
    'general_compliance': {
        'target': 400,
        'sources': [
            'Various compliance docs'
        ],
        'pattern': '<REFUSAL> [Framework requirement violation]. Follow [correct pattern] from docs.'
    }
}
```

---

## Training Pipeline: 90/10 Framework

### Phase Breakdown (Aligned with Established Process)

| Phase | Focus | Effort | Time | Purpose |
|-------|-------|--------|------|---------|
| **1️⃣ Data Foundation** | Dataset extraction & validation | 25% | 2 weeks | Extract 41K samples from Web4Articles |
| **2️⃣ Template Governance** | Prompt format consistency | 10% | 4 days | Ensure chat template alignment |
| **3️⃣ Evaluation Infrastructure** | Metrics & benchmarks | 20% | 1.5 weeks | Build evaluation harness |
| **4️⃣ Data QA Loop** | Continuous curation | 15% | 1 week | Iterate and refine dataset |
| **5️⃣ Training Orchestration** | LoRA training run | 5% | 12-18 hrs | Train on all 41K samples |
| **6️⃣ Artifact Packaging** | Merge & quantize | 2% | 2 hours | Create GGUF artifact |
| **7️⃣ Deployment** | Serving & testing | 3% | 1 hour | Deploy to Ollama |
| **8️⃣ Documentation** | Knowledge capture | 10% | 3 days | Document process and results |
| **9️⃣ Continuous Improvement** | Governance & scaling | 10% | Ongoing | Maintain and improve |

**Total**: 90% planning/data, 10% execution

### Stage 1: Dataset Sanity Check (1 hour)

```bash
# Validate all JSONL files
python scripts/validate_dataset.py \
    --input data/*.jsonl \
    --check format,schema,tokenization,web4_compliance

# Expected output:
# ✅ tool_core.jsonl: 10,000 samples, all valid
# ✅ tool_neg.jsonl: 2,000 samples, all valid
# ✅ style_core.jsonl: 15,000 samples, all valid
# ✅ pdca_structure.jsonl: 5,000 samples, all valid
# ✅ pdca_historical.jsonl: 3,000 samples, all valid
# ✅ style_refactor.jsonl: 3,000 samples, all valid
# ✅ guardrail.jsonl: 2,000 samples, all valid
# ✅ eval.jsonl: 1,000 samples, all valid
# 
# Total: 41,000 samples, ~28M tokens, 0 errors
```

### Stage 2: Dry Run (2-3 hours)

```bash
# Test on 100 samples
python scripts/train_lora_mps.py \
    --config config/dry_run.json \
    --samples 100 \
    --epochs 1 \
    --batch_size 1 \
    --base_model Qwen/Qwen2.5-Coder-7B-Instruct

# Success criteria:
# - Loss decreases from ~2.5 to ~1.0
# - No MPS errors
# - Memory stable (<28 GB)
# - Model generates valid PDCA structure
```

### Stage 3: Mini Fine-Tune (3-4 hours)

```bash
# Train on 3,000 samples (sample from each bucket)
python scripts/train_lora_mps.py \
    --config config/mini_finetune.json \
    --samples 3000 \
    --epochs 1 \
    --batch_size 1 \
    --grad_accumulation 8

# Success criteria:
# - Loss stabilizes around 0.8-1.2
# - Outputs valid PDCA structure
# - Generates proper Web4 code
# - Refuses violations correctly
```

### Stage 4: Full LoRA Training (12-18 hours)

```bash
# Train on all 41,000 samples
python scripts/train_lora_mps.py \
    --config config/full_training.json \
    --base_model Qwen/Qwen2.5-Coder-7B-Instruct \
    --dataset data/ \
    --lora_r 16 \
    --lora_alpha 32 \
    --lora_dropout 0.05 \
    --batch_size 1 \
    --grad_accumulation 12 \
    --learning_rate 2e-4 \
    --epochs 2 \
    --warmup_steps 100 \
    --output outputs/web4_complete_lora_$(date +%Y%m%d)

# Monitoring:
# - Loss should plateau at 0.6-1.0
# - No divergence (loss explosion)
# - Memory stable (<28 GB on M1 Mac)
# - Checkpoint every 500 steps
```

---

## Evening Training Loop

### Automated Nightly Training

**Purpose**: Incorporate today's work into the model automatically

**Schedule**: Every night at 8:00 PM

```python
#!/usr/bin/env python3
"""
evening_training_loop.py

Automated nightly training loop that:
1. Extracts today's PDCAs from RAG
2. Adds to training dataset
3. Trains incremental LoRA adapter
4. Deploys updated model
5. Clears RAG buffer
"""

import json
from pathlib import Path
from datetime import datetime, date
import subprocess
import logging

class EveningTrainingLoop:
    def __init__(self):
        self.today = date.today()
        self.rag_buffer_path = Path('vector_db/daily_buffer/')
        self.training_data_path = Path('data/incremental/')
        self.model_output_path = Path('outputs/nightly/')
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('EveningTraining')
    
    def run(self):
        """Execute the evening training loop"""
        self.logger.info(f'🌙 Starting evening training loop for {self.today}')
        
        # Step 1: Extract today's PDCAs from RAG
        todays_pdcas = self.extract_from_rag()
        self.logger.info(f'📊 Extracted {len(todays_pdcas)} PDCAs from today')
        
        if len(todays_pdcas) == 0:
            self.logger.info('✅ No new PDCAs today, skipping training')
            return
        
        # Step 2: Convert to training samples
        training_samples = self.convert_to_samples(todays_pdcas)
        self.logger.info(f'📝 Generated {len(training_samples)} training samples')
        
        # Step 3: Append to training dataset
        self.append_to_dataset(training_samples)
        
        # Step 4: Train incremental LoRA (fast mode: 2-4 hours)
        self.train_incremental_lora()
        
        # Step 5: Merge and quantize
        self.merge_and_quantize()
        
        # Step 6: Deploy updated model
        self.deploy_model()
        
        # Step 7: Clear RAG buffer
        self.clear_rag_buffer()
        
        self.logger.info(f'✅ Evening training complete for {self.today}')
    
    def extract_from_rag(self):
        """Extract today's PDCAs from RAG buffer"""
        pdcas = []
        
        # Query RAG for today's documents
        today_str = self.today.strftime('%Y-%m-%d')
        rag_files = list(self.rag_buffer_path.glob(f'{today_str}*.pdca.md'))
        
        for pdca_path in rag_files:
            content = pdca_path.read_text()
            pdcas.append({
                'filename': pdca_path.name,
                'content': content,
                'date': self.today
            })
        
        return pdcas
    
    def convert_to_samples(self, pdcas):
        """Convert PDCAs to training samples"""
        samples = []
        
        for pdca in pdcas:
            # Complete PDCA as structure sample
            samples.append({
                'task_type': 'pdca_structure',
                'instruction': 'Create a PDCA document following template v3.2.4.2',
                'input': f'PDCA from {pdca["date"]}',
                'output': pdca['content']
            })
            
            # Extract TRON format
            tron = self.extract_tron(pdca['content'])
            if tron:
                samples.append({
                    'task_type': 'pdca_reasoning',
                    'instruction': 'Apply TRON format to structure a user request',
                    'input': tron['trigger'],
                    'output': self.format_tron(tron)
                })
        
        return samples
    
    def append_to_dataset(self, samples):
        """Append samples to incremental training dataset"""
        output_path = self.training_data_path / f'incremental_{self.today}.jsonl'
        
        with open(output_path, 'w') as f:
            for sample in samples:
                f.write(json.dumps(sample) + '\n')
        
        self.logger.info(f'💾 Saved {len(samples)} samples to {output_path}')
    
    def train_incremental_lora(self):
        """Train LoRA on today's data + recent history"""
        # Use last 7 days of incremental data
        recent_files = sorted(self.training_data_path.glob('incremental_*.jsonl'))[-7:]
        
        # Combine with today's file
        combined_data = self.training_data_path / f'combined_{self.today}.jsonl'
        
        with open(combined_data, 'w') as outf:
            for data_file in recent_files:
                with open(data_file, 'r') as inf:
                    outf.write(inf.read())
        
        # Train (fast mode: only 1 epoch, higher learning rate)
        cmd = [
            'python', 'scripts/train_lora_mps.py',
            '--config', 'config/incremental_training.json',
            '--dataset', str(combined_data),
            '--base_model', 'Qwen/Qwen2.5-Coder-7B-Instruct',
            '--resume_from', str(self.model_output_path / 'latest/'),
            '--epochs', '1',
            '--learning_rate', '1e-4',  # Higher for fast adaptation
            '--output', str(self.model_output_path / f'nightly_{self.today}')
        ]
        
        self.logger.info(f'🏋️ Starting incremental training...')
        subprocess.run(cmd, check=True)
    
    def merge_and_quantize(self):
        """Merge LoRA and quantize"""
        model_path = self.model_output_path / f'nightly_{self.today}'
        
        # Merge
        self.logger.info('🔧 Merging LoRA adapter...')
        subprocess.run([
            'python', 'scripts/merge_lora.py',
            '--adapter', str(model_path),
            '--output', str(model_path / 'merged')
        ], check=True)
        
        # Quantize
        self.logger.info('📦 Quantizing to GGUF...')
        subprocess.run([
            'python', 'llama.cpp/convert-hf-to-gguf.py',
            str(model_path / 'merged'),
            '--outfile', str(model_path / 'model.gguf')
        ], check=True)
        
        subprocess.run([
            './llama.cpp/quantize',
            str(model_path / 'model.gguf'),
            str(model_path / 'model.Q4_K_M.gguf'),
            'Q4_K_M'
        ], check=True)
    
    def deploy_model(self):
        """Deploy to Ollama"""
        model_path = self.model_output_path / f'nightly_{self.today}'
        
        # Create Modelfile
        modelfile_content = f"""FROM {model_path}/model.Q4_K_M.gguf
PARAMETER temperature 0
TEMPLATE \"\"\"{{ .System }}\\n{{ .Prompt }}\"\"\"
"""
        modelfile_path = model_path / 'Modelfile'
        modelfile_path.write_text(modelfile_content)
        
        # Register with Ollama
        self.logger.info('🚀 Deploying to Ollama...')
        subprocess.run([
            'ollama', 'create', 'web4-agent:latest',
            '-f', str(modelfile_path)
        ], check=True)
        
        # Update symlink to latest
        latest_link = self.model_output_path / 'latest'
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(model_path)
    
    def clear_rag_buffer(self):
        """Clear RAG buffer after training"""
        # Move to archive instead of deleting
        archive_path = Path('vector_db/archive') / str(self.today)
        archive_path.mkdir(parents=True, exist_ok=True)
        
        for pdca_file in self.rag_buffer_path.glob('*.pdca.md'):
            pdca_file.rename(archive_path / pdca_file.name)
        
        self.logger.info('🗑️ RAG buffer cleared (archived)')
    
    def extract_tron(self, content):
        """Extract TRON from PDCA"""
        # Implementation from earlier
        pass
    
    def format_tron(self, tron):
        """Format TRON"""
        # Implementation from earlier
        pass

if __name__ == '__main__':
    loop = EveningTrainingLoop()
    loop.run()
```

**Cron Schedule**:
```bash
# Add to crontab
0 20 * * * cd /media/hannesn/storage/Code/CeruleanCircle/Planning/LLM_Training && python3 evening_training_loop.py >> logs/nightly_training.log 2>&1
```

---

## Evaluation & Quality Gates

### Evaluation Metrics (Aligned with Established Framework)

| Metric | Target | Gate | Bucket |
|--------|--------|------|--------|
| **JSON Validity** | ≥99% | Ship gate | Tool-Core |
| **Tool Selection Accuracy** | ≥92% | Ship gate | Tool-Core |
| **PDCA Template Compliance** | ≥95% | Ship gate | PDCA-Structure |
| **TRON Format Accuracy** | ≥90% | Quality gate | PDCA-Structure |
| **Dual Link Format** | ≥95% | Ship gate | PDCA-Structure |
| **Empty Constructor Pattern** | ≥95% | Ship gate | Style-Core |
| **Scenario Pattern** | ≥90% | Quality gate | Style-Core |
| **Lint Pass** | 100% | Ship gate | Style-Core |
| **Jest Refusal** | ≥98% | Ship gate | Guardrails |
| **CMM3 Compliance** | ≥90% | Quality gate | Guardrails |
| **Overall Weighted Score** | ≥90% | Ship gate | Combined |

### Post-Training Evaluation

```python
#!/usr/bin/env python3
"""
evaluate_web4_model.py

Comprehensive evaluation of trained Web4 LoRA model.
Tests all quality gates before deployment approval.
"""

import json
from pathlib import Path
from typing import Dict, List
import subprocess
import re

class Web4ModelEvaluator:
    def __init__(self, model_path: str, eval_data_path: str):
        self.model_path = model_path
        self.eval_data_path = Path(eval_data_path)
        self.results = {}
    
    def evaluate_all(self) -> Dict:
        """Run all evaluation tests"""
        self.results['tool_use'] = self.evaluate_tool_use()
        self.results['pdca_structure'] = self.evaluate_pdca_structure()
        self.results['style_compliance'] = self.evaluate_style_compliance()
        self.results['guardrails'] = self.evaluate_guardrails()
        self.results['overall'] = self.calculate_overall_score()
        
        return self.results
    
    def evaluate_tool_use(self) -> Dict:
        """Evaluate tool calling accuracy"""
        eval_file = self.eval_data_path / 'eval_tool.jsonl'
        samples = self.load_samples(eval_file)
        
        metrics = {
            'json_validity': 0,
            'tool_selection': 0,
            'argument_correctness': 0
        }
        
        for sample in samples:
            output = self.generate(sample['instruction'], sample['input'])
            
            # Check JSON validity
            try:
                parsed = json.loads(output)
                metrics['json_validity'] += 1
                
                # Check tool selection
                if self.check_tool_selection(parsed, sample):
                    metrics['tool_selection'] += 1
                
                # Check arguments
                if self.check_arguments(parsed, sample):
                    metrics['argument_correctness'] += 1
            except json.JSONDecodeError:
                pass
        
        # Calculate percentages
        total = len(samples)
        return {
            'json_validity': metrics['json_validity'] / total * 100,
            'tool_selection': metrics['tool_selection'] / total * 100,
            'argument_correctness': metrics['argument_correctness'] / total * 100
        }
    
    def evaluate_pdca_structure(self) -> Dict:
        """Evaluate PDCA generation quality"""
        eval_file = self.eval_data_path / 'eval_pdca.jsonl'
        samples = self.load_samples(eval_file)
        
        metrics = {
            'template_compliance': 0,
            'tron_format': 0,
            'dual_links': 0,
            'cmm_badge': 0
        }
        
        for sample in samples:
            output = self.generate(sample['instruction'], sample['input'])
            
            # Check template compliance (all required sections)
            if self.check_template_compliance(output):
                metrics['template_compliance'] += 1
            
            # Check TRON format
            if self.check_tron_format(output):
                metrics['tron_format'] += 1
            
            # Check dual links
            if self.check_dual_links(output):
                metrics['dual_links'] += 1
            
            # Check CMM badge
            if 'CMM3' in output or 'CMM4' in output:
                metrics['cmm_badge'] += 1
        
        total = len(samples)
        return {
            'template_compliance': metrics['template_compliance'] / total * 100,
            'tron_format': metrics['tron_format'] / total * 100,
            'dual_links': metrics['dual_links'] / total * 100,
            'cmm_badge': metrics['cmm_badge'] / total * 100
        }
    
    def evaluate_style_compliance(self) -> Dict:
        """Evaluate code style and Web4 patterns"""
        eval_file = self.eval_data_path / 'eval_style.jsonl'
        samples = self.load_samples(eval_file)
        
        metrics = {
            'empty_constructor': 0,
            'scenario_pattern': 0,
            'layer_separation': 0,
            'lint_pass': 0
        }
        
        for sample in samples:
            output = self.generate(sample['instruction'], sample['input'])
            
            # Check empty constructor
            if self.check_empty_constructor(output):
                metrics['empty_constructor'] += 1
            
            # Check scenario pattern
            if 'init(scenario: Scenario' in output and 'toScenario()' in output:
                metrics['scenario_pattern'] += 1
            
            # Check layer separation
            if self.check_layer_separation(output):
                metrics['layer_separation'] += 1
            
            # Check lint (save to temp file and run eslint)
            if self.check_lint(output):
                metrics['lint_pass'] += 1
        
        total = len(samples)
        return {
            'empty_constructor': metrics['empty_constructor'] / total * 100,
            'scenario_pattern': metrics['scenario_pattern'] / total * 100,
            'layer_separation': metrics['layer_separation'] / total * 100,
            'lint_pass': metrics['lint_pass'] / total * 100
        }
    
    def evaluate_guardrails(self) -> Dict:
        """Evaluate refusal accuracy"""
        eval_file = self.eval_data_path / 'eval_guardrail.jsonl'
        samples = self.load_samples(eval_file)
        
        metrics = {
            'refusal_accuracy': 0,
            'jest_ban': 0,
            'manual_op_ban': 0
        }
        
        for sample in samples:
            output = self.generate(sample['instruction'], sample['input'])
            
            # Check refusal
            if '<REFUSAL>' in output:
                metrics['refusal_accuracy'] += 1
            
            # Check Jest ban
            if 'Jest' in sample['instruction'] and 'Vitest' in output:
                metrics['jest_ban'] += 1
            
            # Check manual operation ban
            if 'cp -r' in sample['instruction'] or 'manual' in sample['instruction'].lower():
                if 'web4tscomponent' in output:
                    metrics['manual_op_ban'] += 1
        
        total = len(samples)
        return {
            'refusal_accuracy': metrics['refusal_accuracy'] / total * 100,
            'jest_ban': metrics['jest_ban'] / total * 100 if metrics['jest_ban'] > 0 else 100,
            'manual_op_ban': metrics['manual_op_ban'] / total * 100 if metrics['manual_op_ban'] > 0 else 100
        }
    
    def calculate_overall_score(self) -> float:
        """Calculate weighted overall score"""
        weights = {
            'tool_use': 0.30,
            'pdca_structure': 0.30,
            'style_compliance': 0.30,
            'guardrails': 0.10
        }
        
        overall = 0.0
        for category, weight in weights.items():
            category_avg = sum(self.results[category].values()) / len(self.results[category])
            overall += category_avg * weight
        
        return overall
    
    def generate(self, instruction: str, input_text: str) -> str:
        """Generate output from model"""
        prompt = f"{instruction}\n\nInput: {input_text}\n\nOutput:"
        
        result = subprocess.run([
            'ollama', 'run', 'web4-agent:latest', prompt
        ], capture_output=True, text=True)
        
        return result.stdout.strip()
    
    def load_samples(self, file_path: Path) -> List[Dict]:
        """Load evaluation samples"""
        samples = []
        with open(file_path, 'r') as f:
            for line in f:
                samples.append(json.loads(line))
        return samples
    
    def check_template_compliance(self, output: str) -> bool:
        """Check PDCA template compliance"""
        required_sections = ['PLAN', 'DO', 'CHECK', 'ACT', 'SUMMARY']
        return all(section in output for section in required_sections)
    
    def check_tron_format(self, output: str) -> bool:
        """Check TRON format"""
        tron_keywords = ['Trigger', 'Response', 'Outcome', 'Next']
        return all(keyword in output for keyword in tron_keywords)
    
    def check_dual_links(self, output: str) -> bool:
        """Check dual link format"""
        pattern = r'\[GitHub\]\([^)]+\)\s*\|\s*\[§/[^]]+\]\([^)]+\)'
        return bool(re.search(pattern, output))
    
    def check_empty_constructor(self, output: str) -> bool:
        """Check empty constructor pattern"""
        pattern = r'constructor\(\)\s*\{\s*this\.model\s*=\s*\{[^}]+\};\s*\}'
        return bool(re.search(pattern, output))
    
    def check_layer_separation(self, output: str) -> bool:
        """Check layer separation"""
        # Check if interface and implementation are separate
        has_interface = 'export interface' in output
        has_implementation = 'export class' in output
        return has_interface and has_implementation
    
    def check_lint(self, code: str) -> bool:
        """Check if code passes lint"""
        # Save to temp file
        temp_file = Path('/tmp/temp_code.ts')
        temp_file.write_text(code)
        
        # Run eslint
        result = subprocess.run([
            'npx', 'eslint', str(temp_file)
        ], capture_output=True)
        
        return result.returncode == 0
    
    def check_tool_selection(self, output: Dict, sample: Dict) -> bool:
        """Check if correct tool was selected"""
        # Implementation depends on expected tool
        return True  # Placeholder
    
    def check_arguments(self, output: Dict, sample: Dict) -> bool:
        """Check if arguments are correct"""
        # Implementation depends on expected arguments
        return True  # Placeholder
    
    def print_report(self):
        """Print evaluation report"""
        print('=' * 80)
        print('Web4 Model Evaluation Report')
        print('=' * 80)
        
        print('\n📊 Tool Use Evaluation:')
        for metric, value in self.results['tool_use'].items():
            status = '✅' if value >= 92 else '⚠️'
            print(f'  {status} {metric}: {value:.2f}%')
        
        print('\n📋 PDCA Structure Evaluation:')
        for metric, value in self.results['pdca_structure'].items():
            status = '✅' if value >= 90 else '⚠️'
            print(f'  {status} {metric}: {value:.2f}%')
        
        print('\n🎨 Style Compliance Evaluation:')
        for metric, value in self.results['style_compliance'].items():
            status = '✅' if value >= 90 else '⚠️'
            print(f'  {status} {metric}: {value:.2f}%')
        
        print('\n🛡️ Guardrails Evaluation:')
        for metric, value in self.results['guardrails'].items():
            status = '✅' if value >= 98 else '⚠️'
            print(f'  {status} {metric}: {value:.2f}%')
        
        overall = self.results['overall']
        status = '✅ PASS' if overall >= 90 else '❌ FAIL'
        print(f'\n📈 Overall Score: {overall:.2f}% {status}')
        print('=' * 80)

if __name__ == '__main__':
    evaluator = Web4ModelEvaluator(
        model_path='outputs/web4_complete_lora/latest/',
        eval_data_path='data/eval/'
    )
    
    results = evaluator.evaluate_all()
    evaluator.print_report()
    
    # Save results
    with open('outputs/evaluation_results.json', 'w') as f:
        json.dumps(results, f, indent=2)
```

---

## RL Add-On (Optional Stage)

### Stage Overview

After SFT (Supervised Fine-Tuning), you can optionally add Reinforcement Learning stages for further refinement:

**Stage 1: Preference Optimization (ORPO/DPO)**
- Human annotators compare model outputs
- Train model to prefer higher-quality responses
- Time: 4-8 hours on M1 Mac
- Dataset: 500-1,500 preference pairs

**Stage 2: Offline RL (RS-SFT/AWR)**
- AI-scored samples (automated quality assessment)
- Reward shaping based on evaluation metrics
- Time: 6-12 hours on M1 Mac
- Dataset: 5,000-20,000 scored samples

**Stage 3: Online RL (PPO/GRPO)** [Cloud Recommended]
- Interactive environment simulation
- Real-time feedback loop
- Time: 4-8 hours on cloud (1-2 days on M1)
- Dataset: 10,000-50,000 episodes

**Recommendation**: Start with SFT only. Add RL stages if specific behaviors need refinement.

See: [Web4_LoRA_RL_AddOn_Plan.md](../RL/Web4_LoRA_RL_AddOn_Plan.md) for details.

---

## Deployment Architecture

### Final System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER REQUEST                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OLLAMA SERVER                                  │
│                                                                   │
│  Model: web4-agent:latest                                       │
│  Base: Qwen2.5-Coder-7B-Instruct                               │
│  Adapter: web4_complete_lora (nightly_2025-10-27)              │
│  Format: Q4_K_M GGUF (~4.5 GB)                                  │
│                                                                   │
│  Knowledge (Trained into adapter):                              │
│  • All PDCA patterns and structures                             │
│  • All CMM framework knowledge                                  │
│  • All Web4 architectural patterns                              │
│  • All historical PDCAs (up to last night)                      │
│  • All component implementations                                │
│  • All key lessons and checklists                               │
│  • All compliance rules and violations                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              RAG QUERY (Optional, Rare)                          │
│                                                                   │
│  Query RAG only for:                                            │
│  1. Today's PDCAs (not yet in training)                         │
│  2. Current session context                                     │
│  3. Draft/uncommitted work                                      │
│                                                                   │
│  RAG Hit Rate: ~5% of requests                                  │
│  (Most knowledge already in adapter)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSE GENERATION                           │
│                                                                   │
│  Sources:                                                        │
│  • Trained knowledge (95%)                                      │
│  • RAG context (5%)                                             │
│                                                                   │
│  Quality:                                                        │
│  • Template compliance: >95%                                    │
│  • Pattern adherence: >90%                                      │
│  • Refusal accuracy: >98%                                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    USER RESPONSE                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ollama Modelfile

```modelfile
# Modelfile for web4-agent
FROM ./outputs/web4_complete_lora/latest/model.Q4_K_M.gguf

PARAMETER temperature 0.0
PARAMETER top_p 0.95
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1

TEMPLATE """{{ .System }}

User: {{ .Prompt }}
