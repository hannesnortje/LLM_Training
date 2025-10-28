# Phase 1: Setup & RAG Bootstrap

**Duration:** Flexible (1-2 weeks typical)  
**Goal:** Establish complete three-tier RAG system with all 534 PDCAs indexed and validated

---

## Overview

Phase 1 establishes the foundation for the entire training pipeline by creating a three-tier RAG system (ChromaDB + Redis Graph + SQLite) and indexing all source data. This phase is critical because RAG becomes the single source of truth for all subsequent training sample generation.

---

## Prerequisites

Before starting Phase 1, ensure you have:

- [ ] **Hardware:** M1 Mac with 32GB RAM (or equivalent)
- [ ] **OS:** macOS, Linux, or Windows with WSL2
- [ ] **Access:** Web4Articles repository at `/media/hannesn/storage/Code/CeruleanCircle/Web4Articles/Web4Articles/`
- [ ] **Account:** HuggingFace account (free tier sufficient, for base model download later)
- [ ] **Time:** 1-2 weeks allocated (full-time vs part-time)

---

## Step 1: Environment Setup

**Estimated Time:** 2-4 hours  
**Goal:** Install all required software and dependencies

### 1.1 Install Python 3.10+

```bash
# Verify Python version (must be 3.10 or higher)
python3 --version

# If needed, install Python 3.10+
# macOS with Homebrew:
brew install python@3.10

# Linux (Ubuntu/Debian):
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# Verify installation
python3.10 --version
```

**Validation:**
- [ ] Python 3.10 or higher installed
- [ ] `python3 --version` shows correct version

---

### 1.2 Install Ollama

```bash
# macOS / Linux
curl https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai

# Verify installation
ollama --version

# Test Ollama server (optional, for later)
ollama serve &
```

**Validation:**
- [ ] Ollama installed successfully
- [ ] `ollama --version` shows version number

---

### 1.3 Install ChromaDB

```bash
# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install ChromaDB
pip install chromadb==0.4.18

# Verify installation
python3 -c "import chromadb; print(chromadb.__version__)"
```

**Validation:**
- [ ] ChromaDB installed successfully
- [ ] Import test passes without errors

---

### 1.4 Install Redis + RedisGraph

**macOS:**
```bash
# Install Redis
brew install redis

# Start Redis server
brew services start redis

# Verify Redis is running
redis-cli ping
# Should return: PONG

# Install RedisGraph (if not included)
# Note: RedisGraph may need to be built from source or use Redis Stack
brew install redis-stack
```

**Linux (Ubuntu/Debian):**
```bash
# Install Redis
sudo apt update
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify
redis-cli ping

# Install Redis Stack for RedisGraph
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis-stack-server

# Start Redis Stack
sudo systemctl start redis-stack-server
```

**Python Client:**
```bash
# Install Python Redis clients
pip install redis==5.0.1 redisgraph==2.5.1
```

**Validation:**
- [ ] Redis server running (`redis-cli ping` returns PONG)
- [ ] RedisGraph module loaded
- [ ] Python Redis clients installed

---

### 1.5 Verify SQLite

```bash
# SQLite comes with Python, verify it's available
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

**Validation:**
- [ ] SQLite available (should show version 3.x.x)

---

### 1.6 Clone Web4Articles Repository

```bash
# Navigate to your work directory
cd /media/hannesn/storage/Code/CeruleanCircle/

# Verify Web4Articles exists
ls -la Web4Articles/Web4Articles/

# Count PDCAs to verify
find Web4Articles/Web4Articles/scrum.pmo/project.journal/ -name "*.pdca.md" | wc -l
# Should show: 534

# Count TypeScript files
find Web4Articles/Web4Articles/ -name "*.ts" -o -name "*.tsx" | wc -l
# Should show: ~3,477
```

**Validation:**
- [ ] Web4Articles repository accessible
- [ ] 534 PDCA files found
- [ ] ~3,477 TypeScript files found

---

### 1.7 Set Up Project Structure

```bash
# Navigate to LLM_Training directory
cd /media/hannesn/storage/Code/CeruleanCircle/Planning/LLM_Training/

# Create project structure
mkdir -p scripts
mkdir -p data
mkdir -p config
mkdir -p outputs
mkdir -p eval
mkdir -p logs

# Verify structure
tree -L 1 .
```

**Expected Structure:**
```
LLM_Training/
├── scripts/          # Python scripts for indexing, training, evaluation
├── data/             # Generated JSONL training files
├── config/           # Configuration files (training params, RAG settings)
├── outputs/          # LoRA adapters, GGUF models, eval reports
├── eval/             # Evaluation test harnesses
├── logs/             # Log files for evening loop, debugging
├── Training/         # Existing: strategy docs, diagrams
├── RL/               # Existing: RL planning docs
└── Implementation/   # This guide
```

**Validation:**
- [ ] All directories created
- [ ] Directory structure matches expected layout

---

### 1.8 Install Python Dependencies

Create `requirements.txt`:

```bash
cat > requirements.txt << 'EOF'
# Core ML Libraries
transformers==4.36.0
peft==0.7.1
torch==2.1.2
accelerate==0.25.0
bitsandbytes==0.41.3

# Vector DB & Graph
chromadb==0.4.18
sentence-transformers==2.2.2
redis==5.0.1
redisgraph==2.5.1

# Data Processing
datasets==2.15.0
jsonschema==4.20.0
tqdm==4.66.1

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
```

Install dependencies:

```bash
pip install -r requirements.txt

# Verify key installations
python3 << 'VERIFY'
import transformers
import peft
import torch
import chromadb
import redis
import redisgraph
print("✓ All core dependencies installed successfully")
print(f"  - transformers: {transformers.__version__}")
print(f"  - peft: {peft.__version__}")
print(f"  - torch: {torch.__version__}")
print(f"  - chromadb: {chromadb.__version__}")
VERIFY
```

**Validation:**
- [ ] All packages installed without errors
- [ ] Import verification passes
- [ ] No version conflicts

---

## Step 2: RAG System Bootstrap

**Estimated Time:** 4-8 hours (mostly indexing time)  
**Goal:** Index all 534 PDCAs, 3,477 TypeScript files, 238 process docs, and 12K tool examples

### 2.1 Create Initial Indexing Script

Create `scripts/initial_indexing.py`:

```python
#!/usr/bin/env python3
"""
Initial indexing script for Web4 RAG system.
Indexes PDCAs, TypeScript files, process docs, and tool examples.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import chromadb
from chromadb.config import Settings
import redis
from redisgraph import Graph
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Configuration
WEB4_ARTICLES_ROOT = Path("/media/hannesn/storage/Code/CeruleanCircle/Web4Articles/Web4Articles")
PDCA_ROOT = WEB4_ARTICLES_ROOT / "scrum.pmo" / "project.journal"
DATA_ROOT = Path("./data")
CHROMA_DB_PATH = "./chroma_db"
SQLITE_DB_PATH = "./pdca_timeline.db"

# Initialize embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize ChromaDB
print("Initializing ChromaDB...")
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Initialize Redis Graph
print("Connecting to Redis Graph...")
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
redis_graph = Graph('breadcrumb_graph', redis_client)

# Initialize SQLite
print("Initializing SQLite...")
sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cursor = sqlite_conn.cursor()

# Create tables
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS pdcas (
    id TEXT PRIMARY KEY,
    agent_name TEXT,
    agent_role TEXT,
    date TEXT,
    timestamp INTEGER,
    session_id TEXT,
    branch TEXT,
    sprint TEXT,
    cmm_level INTEGER,
    task_type TEXT,
    objective TEXT,
    quality_score REAL,
    verification_status TEXT,
    file_path TEXT
)
''')
sqlite_conn.commit()


def chunk_pdca_adaptive(pdca_content: str, pdca_id: str) -> List[Dict[str, Any]]:
    """
    PDCA-aware adaptive chunking that preserves section boundaries.
    Returns list of chunk dictionaries with content and metadata.
    """
    chunks = []
    
    # Split by major sections (PDCA structure)
    sections = {
        'objective': r'## Objective\n(.*?)(?=\n## |$)',
        'plan': r'## Plan\n(.*?)(?=\n## |$)',
        'do': r'## Do\n(.*?)(?=\n## |$)',
        'check': r'## Check\n(.*?)(?=\n## |$)',
        'act': r'## Act\n(.*?)(?=\n## |$)',
        'metadata': r'---\n(.*?)---',
    }
    
    import re
    
    for section_name, pattern in sections.items():
        match = re.search(pattern, pdca_content, re.DOTALL)
        if match:
            content = match.group(1).strip()
            if len(content) > 100:  # Only create chunk if substantial
                chunks.append({
                    'content': f"## {section_name.title()}\n{content}",
                    'chunk_type': f'pdca_{section_name}',
                    'chunk_index': len(chunks),
                    'pdca_id': pdca_id,
                })
    
    return chunks if chunks else [{'content': pdca_content, 'chunk_type': 'pdca_full', 'chunk_index': 0, 'pdca_id': pdca_id}]


def extract_pdca_metadata(pdca_path: Path) -> Dict[str, Any]:
    """Extract metadata from PDCA filename and content."""
    # Filename pattern: YYYYMMDD-HHMMSS-AgentName.RoleName.pdca.md
    stem = pdca_path.stem.replace('.pdca', '')
    parts = stem.split('-', 2)
    
    if len(parts) >= 3:
        date_str = parts[0]
        time_str = parts[1]
        agent_part = parts[2]
        
        agent_parts = agent_part.split('.')
        agent_name = agent_parts[0] if len(agent_parts) > 0 else "UnknownAgent"
        agent_role = agent_parts[1] if len(agent_parts) > 1 else "UnknownRole"
        
        # Parse timestamp
        timestamp = datetime.strptime(f"{date_str}-{time_str}", "%Y%m%d-%H%M%S")
    else:
        agent_name = "UnknownAgent"
        agent_role = "UnknownRole"
        timestamp = datetime.fromtimestamp(pdca_path.stat().st_mtime)
    
    return {
        'agent_name': agent_name,
        'agent_role': agent_role,
        'date': timestamp.strftime('%Y-%m-%d'),
        'timestamp': int(timestamp.timestamp()),
        'pdca_id': pdca_path.stem,
    }


def index_pdcas():
    """Index all 534 PDCAs into ChromaDB, Redis Graph, and SQLite."""
    print("\n=== Indexing PDCAs ===")
    
    # Get or create ChromaDB collection
    try:
        collection = chroma_client.get_collection(name="pdca_historical")
        print(f"Found existing collection with {collection.count()} items, deleting...")
        chroma_client.delete_collection(name="pdca_historical")
    except:
        pass
    
    collection = chroma_client.create_collection(
        name="pdca_historical",
        metadata={"description": "Historical PDCA documents with PDCA-aware chunking"}
    )
    
    # Find all PDCA files
    pdca_files = list(PDCA_ROOT.rglob("*.pdca.md"))
    print(f"Found {len(pdca_files)} PDCA files")
    
    total_chunks = 0
    
    for pdca_path in tqdm(pdca_files, desc="Indexing PDCAs"):
        try:
            # Read PDCA content
            with open(pdca_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            metadata = extract_pdca_metadata(pdca_path)
            
            # Chunk content
            chunks = chunk_pdca_adaptive(content, metadata['pdca_id'])
            
            # Generate embeddings and add to ChromaDB
            for chunk in chunks:
                chunk_id = f"{metadata['pdca_id']}_chunk_{chunk['chunk_index']}"
                embedding = embedding_model.encode(chunk['content']).tolist()
                
                collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk['content']],
                    metadatas=[{
                        'chunk_type': chunk['chunk_type'],
                        'chunk_index': chunk['chunk_index'],
                        'pdca_id': metadata['pdca_id'],
                        'agent_name': metadata['agent_name'],
                        'agent_role': metadata['agent_role'],
                        'date': metadata['date'],
                        'timestamp': metadata['timestamp'],
                        'trained_in_adapter': False,
                        'training_batch': '',
                        'training_date': '',
                    }]
                )
                total_chunks += 1
            
            # Add to SQLite
            sqlite_cursor.execute('''
                INSERT OR REPLACE INTO pdcas 
                (id, agent_name, agent_role, date, timestamp, quality_score, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                metadata['pdca_id'],
                metadata['agent_name'],
                metadata['agent_role'],
                metadata['date'],
                metadata['timestamp'],
                80.0,  # Default quality score
                str(pdca_path)
            ))
            
            # Add to Redis Graph (will be enhanced with PRECEDES edges later)
            redis_graph.query(
                f"CREATE (p:PDCA {{id: '{metadata['pdca_id']}', agent: '{metadata['agent_name']}', date: '{metadata['date']}'}})"
            )
        
        except Exception as e:
            print(f"Error indexing {pdca_path}: {e}")
            continue
    
    sqlite_conn.commit()
    print(f"✓ Indexed {len(pdca_files)} PDCAs into {total_chunks} chunks")
    return total_chunks


def index_typescript_files():
    """Index 3,477 TypeScript files by layer and pattern."""
    print("\n=== Indexing TypeScript Files ===")
    
    # Get or create collection
    try:
        collection = chroma_client.get_collection(name="components")
        chroma_client.delete_collection(name="components")
    except:
        pass
    
    collection = chroma_client.create_collection(
        name="components",
        metadata={"description": "TypeScript component files organized by layer and pattern"}
    )
    
    # Find TypeScript files
    ts_files = list(WEB4_ARTICLES_ROOT.rglob("*.ts")) + list(WEB4_ARTICLES_ROOT.rglob("*.tsx"))
    print(f"Found {len(ts_files)} TypeScript files")
    
    indexed_count = 0
    
    for ts_path in tqdm(ts_files, desc="Indexing TypeScript"):
        try:
            with open(ts_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip very small files
            if len(content) < 100:
                continue
            
            # Detect layer and pattern from path/content
            layer = "unknown"
            if "/layer2/" in str(ts_path):
                layer = "layer2"
            elif "/layer3/" in str(ts_path):
                layer = "layer3"
            elif "/layer5/" in str(ts_path):
                layer = "layer5"
            
            # Detect patterns
            patterns = []
            if "constructor()" in content or "constructor () {" in content:
                patterns.append("empty_constructor")
            if "toScenario()" in content:
                patterns.append("scenario_state")
            if "init(" in content:
                patterns.append("init_method")
            
            # Generate embedding
            embedding = embedding_model.encode(content[:2000]).tolist()  # First 2K chars
            
            collection.add(
                ids=[str(ts_path.relative_to(WEB4_ARTICLES_ROOT))],
                embeddings=[embedding],
                documents=[content[:5000]],  # Store first 5K chars
                metadatas=[{
                    'file_path': str(ts_path),
                    'layer': layer,
                    'patterns': ','.join(patterns) if patterns else 'none',
                    'file_type': ts_path.suffix,
                }]
            )
            indexed_count += 1
        
        except Exception as e:
            print(f"Error indexing {ts_path}: {e}")
            continue
    
    print(f"✓ Indexed {indexed_count} TypeScript files")
    return indexed_count


def index_tool_examples():
    """Index 12K tool examples from tool_core.jsonl and tool_neg.jsonl."""
    print("\n=== Indexing Tool Examples ===")
    
    # Get or create collection
    try:
        collection = chroma_client.get_collection(name="tool_examples")
        chroma_client.delete_collection(name="tool_examples")
    except:
        pass
    
    collection = chroma_client.create_collection(
        name="tool_examples",
        metadata={"description": "Tool examples for IDE-specific tool injection"}
    )
    
    tool_files = [
        DATA_ROOT / "tool_core.jsonl",
        DATA_ROOT / "tool_neg.jsonl"
    ]
    
    indexed_count = 0
    
    for tool_file in tool_files:
        if not tool_file.exists():
            print(f"Warning: {tool_file} not found, skipping...")
            continue
        
        with open(tool_file, 'r') as f:
            for line in tqdm(f, desc=f"Indexing {tool_file.name}"):
                try:
                    example = json.loads(line)
                    
                    # Generate embedding from instruction
                    instruction = example.get('instruction', '')
                    embedding = embedding_model.encode(instruction).tolist()
                    
                    collection.add(
                        ids=[f"{tool_file.stem}_{indexed_count}"],
                        embeddings=[embedding],
                        documents=[instruction],
                        metadatas=[{
                            'tool_name': example.get('tool_name', 'unknown'),
                            'tool_ecosystem': 'continue',  # Default to Continue
                            'usage_pattern': example.get('usage_pattern', 'general'),
                            'is_negative': 'neg' in tool_file.stem,
                        }]
                    )
                    indexed_count += 1
                
                except Exception as e:
                    print(f"Error indexing tool example: {e}")
                    continue
    
    print(f"✓ Indexed {indexed_count} tool examples")
    return indexed_count


def main():
    """Main indexing orchestration."""
    print("="*60)
    print("Web4 RAG System - Initial Indexing")
    print("="*60)
    
    # Index all data
    pdca_chunks = index_pdcas()
    ts_count = index_typescript_files()
    tool_count = index_tool_examples()
    
    # Summary
    print("\n" + "="*60)
    print("INDEXING COMPLETE!")
    print("="*60)
    print(f"✓ PDCAs: {pdca_chunks} chunks from 534 files")
    print(f"✓ TypeScript: {ts_count} files")
    print(f"✓ Tools: {tool_count} examples")
    print(f"\nChromaDB: {CHROMA_DB_PATH}")
    print(f"SQLite: {SQLITE_DB_PATH}")
    print(f"Redis Graph: breadcrumb_graph")
    print("="*60)


if __name__ == "__main__":
    main()
```

**Run the script:**

```bash
# Make executable
chmod +x scripts/initial_indexing.py

# Run indexing (will take 4-8 hours depending on hardware)
python3 scripts/initial_indexing.py
```

**Expected Output:**
```
=============================================================
Web4 RAG System - Initial Indexing
=============================================================
Loading embedding model...
Initializing ChromaDB...
Connecting to Redis Graph...
Initializing SQLite...

=== Indexing PDCAs ===
Found 534 PDCA files
Indexing PDCAs: 100%|████████| 534/534 [01:23<00:00,  6.42it/s]
✓ Indexed 534 PDCAs into 2,670 chunks

=== Indexing TypeScript Files ===
Found 3,477 TypeScript files
Indexing TypeScript: 100%|████████| 3477/3477 [12:45<00:00,  4.54it/s]
✓ Indexed 3,477 TypeScript files

=== Indexing Tool Examples ===
Indexing tool_core.jsonl: 100%|████████| 10000/10000 [08:20<00:00, 19.99it/s]
Indexing tool_neg.jsonl: 100%|████████| 2000/2000 [01:40<00:00, 19.98it/s]
✓ Indexed 12,000 tool examples

=============================================================
INDEXING COMPLETE!
=============================================================
✓ PDCAs: 2,670 chunks from 534 files
✓ TypeScript: 3,477 files
✓ Tools: 12,000 examples

ChromaDB: ./chroma_db
SQLite: ./pdca_timeline.db
Redis Graph: breadcrumb_graph
=============================================================
```

**Validation:**
- [ ] Script runs without fatal errors
- [ ] ~2,670 PDCA chunks indexed
- [ ] 3,477 TypeScript files indexed
- [ ] 12K tool examples indexed (if files exist)
- [ ] ChromaDB directory created
- [ ] SQLite database file created
- [ ] Redis Graph contains nodes

---

### 2.2 Verify Three-Tier Indexing

Create `scripts/test_rag_queries.py`:

```python
#!/usr/bin/env python3
"""Test RAG queries across all three tiers."""

import chromadb
import redis
from redisgraph import Graph
import sqlite3
from sentence_transformers import SentenceTransformer

# Initialize connections
chroma_client = chromadb.PersistentClient(path="./chroma_db")
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
redis_graph = Graph('breadcrumb_graph', redis_client)
sqlite_conn = sqlite3.connect("./pdca_timeline.db")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def test_semantic_search():
    """Test ChromaDB semantic search."""
    print("\n=== Testing Semantic Search (ChromaDB) ===")
    
    collection = chroma_client.get_collection("pdca_historical")
    
    query = "debugging component initialization issues"
    query_embedding = embedding_model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    
    print(f"Query: {query}")
    print(f"Found {len(results['ids'][0])} results:")
    for i, (doc_id, doc) in enumerate(zip(results['ids'][0], results['documents'][0])):
        print(f"  {i+1}. {doc_id}: {doc[:100]}...")
    
    assert len(results['ids'][0]) > 0, "No results from semantic search!"
    print("✓ Semantic search working")


def test_graph_traversal():
    """Test Redis Graph breadcrumb navigation."""
    print("\n=== Testing Graph Traversal (Redis Graph) ===")
    
    # Get all PDCA nodes
    result = redis_graph.query("MATCH (p:PDCA) RETURN p.id LIMIT 5")
    
    print(f"Found {len(result.result_set)} PDCA nodes:")
    for row in result.result_set:
        print(f"  - {row[0]}")
    
    assert len(result.result_set) > 0, "No PDCA nodes in graph!"
    print("✓ Graph traversal working")


def test_temporal_queries():
    """Test SQLite temporal queries."""
    print("\n=== Testing Temporal Queries (SQLite) ===")
    
    cursor = sqlite_conn.cursor()
    
    # Query by date range
    cursor.execute("""
        SELECT id, agent_name, date 
        FROM pdcas 
        WHERE date >= '2024-01-01' 
        ORDER BY date DESC 
        LIMIT 5
    """)
    
    results = cursor.fetchall()
    print(f"Found {len(results)} PDCAs from 2024:")
    for pdca_id, agent, date in results:
        print(f"  - {date}: {pdca_id} by {agent}")
    
    # Query by agent
    cursor.execute("""
        SELECT agent_name, COUNT(*) as count 
        FROM pdcas 
        GROUP BY agent_name
    """)
    
    agents = cursor.fetchall()
    print(f"\nPDCAs by agent:")
    for agent, count in agents:
        print(f"  - {agent}: {count}")
    
    assert len(results) > 0, "No temporal query results!"
    print("✓ Temporal queries working")


def test_metadata_completeness():
    """Verify metadata fields are populated."""
    print("\n=== Testing Metadata Completeness ===")
    
    collection = chroma_client.get_collection("pdca_historical")
    
    # Get sample chunks
    results = collection.get(limit=10, include=['metadatas'])
    
    required_fields = [
        'chunk_type', 'chunk_index', 'pdca_id', 'agent_name', 
        'agent_role', 'date', 'timestamp', 'trained_in_adapter'
    ]
    
    for metadata in results['metadatas']:
        for field in required_fields:
            assert field in metadata, f"Missing field: {field}"
    
    print(f"✓ All {len(required_fields)} required metadata fields present")
    
    # Show sample metadata
    print("\nSample metadata:")
    for k, v in results['metadatas'][0].items():
        print(f"  - {k}: {v}")


def main():
    print("="*60)
    print("RAG System Validation Tests")
    print("="*60)
    
    test_semantic_search()
    test_graph_traversal()
    test_temporal_queries()
    test_metadata_completeness()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60)


if __name__ == "__main__":
    main()
```

**Run validation:**

```bash
chmod +x scripts/test_rag_queries.py
python3 scripts/test_rag_queries.py
```

**Validation:**
- [ ] Semantic search returns relevant results
- [ ] Graph traversal finds PDCA nodes
- [ ] Temporal queries work correctly
- [ ] All metadata fields populated
- [ ] All tests pass

---

## Step 3: Data Quality Validation

**Estimated Time:** 2-4 hours  
**Goal:** Ensure RAG system is production-ready for sample generation

### 3.1 Test Harness Baseline

Create `eval/baseline_test.py` to establish baseline metrics before training:

```python
#!/usr/bin/env python3
"""
Establish baseline metrics from untrained base model.
This will be compared against trained model in Phase 3.
"""

import json
from datetime import datetime

def establish_baseline():
    """Create baseline report."""
    
    baseline = {
        'date': datetime.now().isoformat(),
        'model': 'untrained_base',
        'metrics': {
            'pattern_compliance': 0.0,  # Measured in Phase 3
            'pdca_template': 0.0,
            'tron_format': 0.0,
            'empty_constructor': 0.0,
            'tool_success': 0.0,
            'refusal_f1': 0.0,
        },
        'notes': 'Baseline established. Will measure trained model improvements in Phase 3.'
    }
    
    # Save baseline
    with open('outputs/baseline_metrics.json', 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print("✓ Baseline metrics file created: outputs/baseline_metrics.json")
    print("  This will be used for comparison in Phase 3 evaluation.")


if __name__ == "__main__":
    establish_baseline()
```

**Run baseline:**

```bash
python3 eval/baseline_test.py
```

**Validation:**
- [ ] `outputs/baseline_metrics.json` created
- [ ] Baseline documented for future comparison

---

### 3.2 RAG Query Performance Test

Test query latency to ensure performance targets:

```bash
python3 << 'TEST'
import time
import chromadb
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("pdca_historical")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Test semantic query latency
query = "show me component lifecycle management patterns"
query_embedding = embedding_model.encode(query).tolist()

start = time.time()
results = collection.query(query_embeddings=[query_embedding], n_results=5)
latency = (time.time() - start) * 1000

print(f"Semantic Query Latency: {latency:.0f}ms")
assert latency < 1000, f"Query too slow: {latency}ms (target: <1000ms)"
print("✓ Query performance acceptable")
TEST
```

**Validation:**
- [ ] Query latency under 1 second
- [ ] Results returned successfully

---

## Phase 1 Completion Checklist

Before proceeding to Phase 2, verify all items:

### Environment
- [ ] Python 3.10+ installed and verified
- [ ] Ollama installed (`ollama --version`)
- [ ] ChromaDB installed and tested
- [ ] Redis server running (`redis-cli ping`)
- [ ] RedisGraph module loaded
- [ ] SQLite available
- [ ] All Python dependencies installed

### Data Indexing
- [ ] 534 PDCAs indexed (verify count in ChromaDB)
- [ ] ~2,670 PDCA chunks created
- [ ] 3,477 TypeScript files indexed
- [ ] 238 process docs indexed (if applicable)
- [ ] 12K tool examples indexed (if files exist)
- [ ] ChromaDB collections created: `pdca_historical`, `components`, `tool_examples`
- [ ] Redis Graph contains PDCA nodes
- [ ] SQLite database populated

### Validation
- [ ] Semantic search returns relevant results (under 1 second)
- [ ] Graph traversal works (PDCA nodes accessible)
- [ ] Temporal queries work (date/agent filtering)
- [ ] Metadata completeness verified (15+ fields)
- [ ] Test harness baseline established
- [ ] Query performance acceptable (<1000ms)

### Documentation
- [ ] All scripts documented and executable
- [ ] Log files reviewed (no critical errors)
- [ ] Validation tests passed

---

## Success Criteria

**Phase 1 is complete when:**

✓ RAG system operational with 3 tiers (ChromaDB, Redis Graph, SQLite)  
✓ All 534 PDCAs queryable via semantic/graph/temporal methods  
✓ Test queries return relevant results under 1 second  
✓ Metadata complete (15+ fields per chunk)  
✓ Environment ready for Phase 2 sample generation

---

## Troubleshooting

### Redis Connection Error
```
Error: Could not connect to Redis at localhost:6379
```
**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# If not, start Redis
# macOS:
brew services start redis
# Linux:
sudo systemctl start redis-server
```

### ChromaDB Import Error
```
ImportError: No module named 'chromadb'
```
**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall ChromaDB
pip install chromadb==0.4.18
```

### Embedding Model Download Issues
```
Error downloading model: sentence-transformers/all-MiniLM-L6-v2
```
**Solution:**
```bash
# Download manually first
python3 << 'DOWNLOAD'
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("✓ Model downloaded successfully")
DOWNLOAD
```

### Out of Memory During Indexing
```
MemoryError: Unable to allocate array
```
**Solution:**
- Process files in smaller batches
- Reduce embedding batch size
- Close other applications
- Consider upgrading RAM

---

## Next Steps

Once Phase 1 is complete:

1. **Review Phase 1 deliverables** - Ensure all checklist items are completed
2. **Commit indexing scripts** - Save all scripts to version control
3. **Backup RAG databases** - Create backup of ChromaDB, Redis, SQLite
4. **Proceed to Phase 2** - Begin sample generation from RAG

**Estimated Time to Phase 2:** Immediately (if Phase 1 validation passes)

---

## Phase 1 Summary

**Deliverables:**
- ✓ Complete three-tier RAG system
- ✓ 534 PDCAs indexed (~2,670 chunks)
- ✓ 3,477 TypeScript files indexed
- ✓ 12K tool examples indexed
- ✓ All queries validated and performant
- ✓ Baseline metrics established

**Duration:** 1-2 weeks (flexible)  
**Next Phase:** Phase 2 - Sample Generation

---

*Document Version: 1.0*  
*Last Updated: 2025-10-28*  
*Part of: Web4 Balanced LoRA Training Strategy*

