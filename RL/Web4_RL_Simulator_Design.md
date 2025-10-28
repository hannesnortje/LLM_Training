# 🎮 Web4 RL Simulator Design

> Environment architecture for Stage 3 (PPO/GRPO online reinforcement learning)

**Version:** 1.0  
**Last Updated:** 2025-10-27  
**Status:** Planning / Pre-Implementation

---

## 📋 Table of Contents

1. [Overview](#1️⃣-overview)
2. [Architecture](#2️⃣-architecture)
3. [Environment API](#3️⃣-environment-api)
4. [Tool Implementations](#4️⃣-tool-implementations)
5. [Reward Function](#5️⃣-reward-function)
6. [Episode Management](#6️⃣-episode-management)
7. [Task Generation](#7️⃣-task-generation)
8. [Validation & Testing](#8️⃣-validation--testing)

---

## 1️⃣ Overview

### Purpose

The simulator provides a **deterministic, controllable environment** where the RL agent can:
- Execute tool calls safely (no real file system changes)
- Receive immediate feedback on correctness
- Learn multi-step planning through trial-and-reward
- Practice without risk of damaging real systems

### Key Requirements

1. **Deterministic:** Same action sequence → same results (for reproducibility)
2. **Fast:** Episodes complete in <1 second (for training throughput)
3. **Realistic:** Mimics real tool behavior closely enough to transfer
4. **Safe:** No actual file system or command execution
5. **Observable:** Full logging for debugging and analysis
6. **Extensible:** Easy to add new tools and tasks

### Scope

**Included:**
- File system operations (read, write, search, list)
- Code search (pattern matching, semantic mock)
- Basic terminal commands (safe subset)
- Multi-step task scenarios

**Excluded (for now):**
- Network operations (API calls, web requests)
- Database operations
- Long-running processes
- Interactive commands

---

## 2️⃣ Architecture

### Component Overview

```
┌──────────────────────────────────────────────────┐
│              RL Training Loop                    │
│  (PPO/GRPO orchestrates episodes)                │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│          Environment Manager                      │
│  - Task selection & initialization                │
│  - Episode lifecycle management                   │
│  - Reward calculation & aggregation               │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│          Simulator Core                           │
│  ┌────────────────┐  ┌────────────────┐          │
│  │ Mock File Sys  │  │  Tool Registry │          │
│  │ (in-memory)    │  │  (dispatchers) │          │
│  └────────────────┘  └────────────────┘          │
│  ┌────────────────┐  ┌────────────────┐          │
│  │ State Tracker  │  │ Reward Computer│          │
│  └────────────────┘  └────────────────┘          │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│        Tool Implementations                       │
│  read_file, write, grep, codebase_search, ...    │
└──────────────────────────────────────────────────┘
```

### Data Flow

```
1. Task Selected → Environment Reset
   ├─> Mock file system initialized
   ├─> Task description provided to agent
   └─> Episode state initialized

2. Agent Generates Action → Tool Call
   ├─> JSON parsed and validated
   ├─> Tool dispatcher finds implementation
   └─> Tool executes in mock environment

3. Tool Returns Result
   ├─> State updated (files, observations)
   ├─> Reward computed (immediate)
   └─> Result formatted and returned to agent

4. Episode Continues or Terminates
   ├─> Success: task completed correctly
   ├─> Failure: wrong action or max steps
   └─> Violation: guardrail or safety issue

5. Episode End → Reward Aggregation
   ├─> Immediate rewards summed
   ├─> Completion bonus added
   └─> KL penalty applied
```

---

## 3️⃣ Environment API

### Core Interface

```python
class Web4Simulator:
    """
    OpenAI Gym-style environment for Web4 tool learning
    """
    
    def __init__(self, config: SimulatorConfig):
        """
        Args:
            config: Simulator configuration (tools, rewards, limits)
        """
        self.fs = MockFileSystem()
        self.tool_registry = ToolRegistry()
        self.reward_computer = RewardComputer(config.rewards)
        self.max_steps = config.max_steps
        
    def reset(self, task: Task) -> Observation:
        """
        Reset environment for new episode
        
        Args:
            task: Task specification (goal, initial files, etc.)
            
        Returns:
            Initial observation (task description, available context)
        """
        self.fs.reset(task.initial_files)
        self.state = EpisodeState(task=task, step=0)
        return self._make_observation()
    
    def step(self, action: str) -> Tuple[Observation, float, bool, dict]:
        """
        Execute one action in the environment
        
        Args:
            action: Model output (JSON tool call)
            
        Returns:
            observation: Next state observation
            reward: Immediate reward for this action
            done: Whether episode is complete
            info: Debug information
        """
        # Parse action
        try:
            tool_call = self._parse_action(action)
        except JSONError as e:
            reward = self.reward_computer.json_error()
            return self._make_observation(), reward, True, {"error": str(e)}
        
        # Validate schema
        if not self._validate_schema(tool_call):
            reward = self.reward_computer.schema_error()
            return self._make_observation(), reward, True, {"error": "schema"}
        
        # Execute tool
        try:
            result = self.tool_registry.execute(tool_call, self.fs)
            self.state.history.append((tool_call, result))
            self.state.step += 1
        except Exception as e:
            reward = self.reward_computer.execution_error()
            return self._make_observation(), reward, True, {"error": str(e)}
        
        # Check guardrails
        if self._check_guardrail_violation(tool_call):
            reward = self.reward_computer.guardrail_violation()
            return self._make_observation(), reward, True, {"error": "guardrail"}
        
        # Compute reward
        reward = self._compute_step_reward(tool_call, result)
        
        # Check if done
        done, completion_reason = self._check_completion()
        if done and completion_reason == "success":
            reward += self.reward_computer.task_complete()
        
        # Check max steps
        if self.state.step >= self.max_steps:
            done = True
            completion_reason = "max_steps"
        
        info = {
            "step": self.state.step,
            "reason": completion_reason,
            "tool": tool_call["tool"],
        }
        
        return self._make_observation(), reward, done, info
```

### Task Specification

```python
@dataclass
class Task:
    """Specification for a single episode task"""
    
    id: str                          # Unique task ID
    description: str                 # Natural language goal
    category: TaskCategory           # tool_use, multi_step, code_gen, etc.
    difficulty: Difficulty           # simple, medium, hard
    
    initial_files: Dict[str, str]    # Path → content
    expected_actions: List[str]      # Gold action sequence (for validation)
    success_criteria: Callable       # Function: State → bool
    
    max_steps: int = 20              # Override global max
    metadata: Dict[str, Any] = None  # Additional info

TaskCategory = Enum("TaskCategory", [
    "TOOL_USE",          # Single correct tool call
    "MULTI_STEP",        # 2-5 step sequence
    "CODE_GENERATION",   # Generate and write code
    "SEARCH_AND_EDIT",   # Find then modify
    "REFACTOR",          # Transform existing code
])

Difficulty = Enum("Difficulty", ["SIMPLE", "MEDIUM", "HARD", "EXPERT"])
```

### Observation Format

```python
@dataclass
class Observation:
    """What the agent sees at each step"""
    
    task_description: str            # Original goal
    current_step: int                # Step number
    max_steps: int                   # Step limit
    
    available_tools: List[str]       # Tool names
    previous_action: Optional[str]   # Last action taken
    previous_result: Optional[str]   # Last result received
    
    context: Dict[str, Any]          # Additional context (varies by task)
    # e.g., {"visible_files": ["a.ts", "b.ts"], "cwd": "/workspace"}
```

---

## 4️⃣ Tool Implementations

### Mock File System

```python
class MockFileSystem:
    """In-memory file system with path operations"""
    
    def __init__(self):
        self.files: Dict[str, str] = {}          # path → content
        self.metadata: Dict[str, FileMetadata] = {}  # path → metadata
        self.cwd: str = "/workspace"
        
    def reset(self, initial_files: Dict[str, str]):
        """Initialize file system state"""
        self.files = initial_files.copy()
        self.metadata = {
            path: FileMetadata(size=len(content), mtime=0)
            for path, content in initial_files.items()
        }
        
    def read(self, path: str) -> str:
        """Read file contents"""
        abs_path = self._resolve_path(path)
        if abs_path not in self.files:
            raise FileNotFoundError(f"File not found: {path}")
        return self.files[abs_path]
    
    def write(self, path: str, content: str):
        """Write file contents"""
        abs_path = self._resolve_path(path)
        self.files[abs_path] = content
        self.metadata[abs_path] = FileMetadata(
            size=len(content),
            mtime=self._current_time()
        )
    
    def exists(self, path: str) -> bool:
        """Check if file exists"""
        return self._resolve_path(path) in self.files
    
    def list_dir(self, path: str) -> List[str]:
        """List directory contents"""
        abs_path = self._resolve_path(path)
        if not abs_path.endswith("/"):
            abs_path += "/"
        
        return [
            p for p in self.files.keys()
            if p.startswith(abs_path) and "/" not in p[len(abs_path):]
        ]
    
    def glob(self, pattern: str) -> List[str]:
        """Find files matching glob pattern"""
        import fnmatch
        return [
            path for path in self.files.keys()
            if fnmatch.fnmatch(path, pattern)
        ]
    
    def _resolve_path(self, path: str) -> str:
        """Resolve relative paths"""
        if path.startswith("/"):
            return path
        return os.path.normpath(os.path.join(self.cwd, path))
```

### Tool: read_file

```python
class ReadFileTool:
    name = "read_file"
    
    schema = {
        "target_file": {"type": "string", "required": True},
        "offset": {"type": "integer", "required": False},
        "limit": {"type": "integer", "required": False},
    }
    
    def execute(self, args: dict, fs: MockFileSystem) -> str:
        """Execute read_file tool"""
        path = args["target_file"]
        
        try:
            content = fs.read(path)
        except FileNotFoundError:
            return f"Error: File not found: {path}"
        
        # Handle offset/limit
        lines = content.split("\n")
        offset = args.get("offset", 0)
        limit = args.get("limit", len(lines))
        
        selected_lines = lines[offset:offset + limit]
        
        # Format with line numbers
        formatted = "\n".join(
            f"{i+offset+1:6d}|{line}"
            for i, line in enumerate(selected_lines)
        )
        
        return formatted
```

### Tool: grep

```python
class GrepTool:
    name = "grep"
    
    schema = {
        "pattern": {"type": "string", "required": True},
        "path": {"type": "string", "required": False},
        "type": {"type": "string", "required": False},
        "output_mode": {"type": "string", "enum": ["content", "files_with_matches", "count"]},
        "-i": {"type": "boolean", "required": False},
    }
    
    def execute(self, args: dict, fs: MockFileSystem) -> str:
        """Execute grep tool"""
        pattern = args["pattern"]
        path = args.get("path", "/workspace")
        file_type = args.get("type")
        case_insensitive = args.get("-i", False)
        output_mode = args.get("output_mode", "content")
        
        # Build regex
        import re
        flags = re.IGNORECASE if case_insensitive else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            return f"Error: Invalid regex: {e}"
        
        # Find matching files
        candidates = self._get_candidates(fs, path, file_type)
        
        matches = []
        for file_path in candidates:
            content = fs.read(file_path)
            file_matches = self._search_file(file_path, content, regex)
            if file_matches:
                matches.extend(file_matches)
        
        # Format output
        if output_mode == "files_with_matches":
            return "\n".join(set(m["file"] for m in matches))
        elif output_mode == "count":
            counts = {}
            for m in matches:
                counts[m["file"]] = counts.get(m["file"], 0) + 1
            return "\n".join(f"{count}:{file}" for file, count in counts.items())
        else:  # content
            return self._format_content_output(matches)
    
    def _get_candidates(self, fs: MockFileSystem, path: str, file_type: Optional[str]) -> List[str]:
        """Get list of files to search"""
        if fs.exists(path) and not path.endswith("/"):
            return [path]
        
        # Directory search
        all_files = [f for f in fs.files.keys() if f.startswith(path)]
        
        # Filter by type
        if file_type:
            extension = f".{file_type}"
            all_files = [f for f in all_files if f.endswith(extension)]
        
        return all_files
```

### Tool: codebase_search (Mock Semantic Search)

```python
class CodebaseSearchTool:
    name = "codebase_search"
    
    schema = {
        "query": {"type": "string", "required": True},
        "target_directories": {"type": "array", "items": {"type": "string"}},
    }
    
    def execute(self, args: dict, fs: MockFileSystem) -> str:
        """
        Mock semantic search
        
        For simulation, we use keyword matching + heuristics
        to approximate semantic search behavior
        """
        query = args["query"]
        target_dirs = args.get("target_directories", ["/workspace"])
        
        # Extract key terms from query
        keywords = self._extract_keywords(query)
        
        # Score files by relevance
        candidates = []
        for target_dir in target_dirs:
            files = fs.list_dir(target_dir) if target_dir else fs.files.keys()
            
            for file_path in files:
                content = fs.read(file_path)
                score = self._relevance_score(content, keywords)
                if score > 0.3:  # Threshold
                    candidates.append((file_path, score, content))
        
        # Sort by score
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Format top results
        results = []
        for file_path, score, content in candidates[:5]:
            snippet = self._extract_snippet(content, keywords)
            results.append(f"File: {file_path}\nScore: {score:.2f}\n{snippet}\n")
        
        return "\n---\n".join(results) if results else "No results found."
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query"""
        # Simple heuristic: split and filter stop words
        stop_words = {"the", "a", "an", "is", "are", "how", "what", "where", "when"}
        words = query.lower().split()
        return [w for w in words if w not in stop_words and len(w) > 2]
    
    def _relevance_score(self, content: str, keywords: List[str]) -> float:
        """Score content relevance to keywords"""
        content_lower = content.lower()
        matches = sum(1 for kw in keywords if kw in content_lower)
        return matches / len(keywords) if keywords else 0.0
```

### Safe Command Subset

```python
class RunTerminalCmdTool:
    name = "run_terminal_cmd"
    
    # Whitelist of safe commands for simulation
    SAFE_COMMANDS = {
        "ls", "pwd", "echo", "cat", "grep", "find",
        "wc", "head", "tail", "sort", "uniq"
    }
    
    schema = {
        "command": {"type": "string", "required": True},
        "is_background": {"type": "boolean", "required": False},
    }
    
    def execute(self, args: dict, fs: MockFileSystem) -> str:
        """Execute safe terminal command (mock)"""
        command = args["command"]
        
        # Parse command
        cmd_parts = command.split()
        if not cmd_parts:
            return "Error: Empty command"
        
        base_cmd = cmd_parts[0]
        
        # Check whitelist
        if base_cmd not in self.SAFE_COMMANDS:
            return f"Error: Command '{base_cmd}' not available in simulator"
        
        # Mock implementations
        if base_cmd == "ls":
            path = cmd_parts[1] if len(cmd_parts) > 1 else fs.cwd
            return "\n".join(fs.list_dir(path))
        
        elif base_cmd == "pwd":
            return fs.cwd
        
        elif base_cmd == "echo":
            return " ".join(cmd_parts[1:])
        
        # ... more mock implementations ...
        
        return f"Mock execution of: {command}"
```

---

## 5️⃣ Reward Function

### Reward Components

```python
class RewardComputer:
    def __init__(self, config: RewardConfig):
        self.config = config
        
    def json_error(self) -> float:
        """Invalid JSON in action"""
        return self.config.schema_fail  # -5.0
    
    def schema_error(self) -> float:
        """JSON valid but schema invalid"""
        return self.config.schema_fail  # -5.0
    
    def execution_error(self) -> float:
        """Tool execution failed"""
        return self.config.wrong_tool  # -3.0
    
    def guardrail_violation(self) -> float:
        """Safety violation"""
        return self.config.guardrail_violation  # -10.0 (episode ends)
    
    def task_complete(self) -> float:
        """Task successfully completed"""
        return self.config.task_complete  # +10.0
    
    def step_reward(
        self,
        tool_call: dict,
        result: str,
        state: EpisodeState
    ) -> float:
        """Compute reward for a successful step"""
        reward = 0.0
        
        # Correct tool used
        if self._is_correct_tool(tool_call, state):
            reward += self.config.correct_tool  # +5.0
        else:
            reward += self.config.wrong_tool  # -3.0
        
        # Schema compliance
        if self._schema_valid(tool_call):
            reward += self.config.schema_pass  # +2.0
        
        # Style check (if code generation)
        if self._has_code_output(tool_call) and self._style_valid(result):
            reward += self.config.style_pass  # +1.0
        
        # Redundancy penalty
        if self._is_redundant(tool_call, state):
            reward += self.config.redundant_action  # -2.0
        
        # Step penalty (encourage efficiency)
        reward += self.config.step_penalty  # -0.5
        
        return reward
    
    def _is_correct_tool(self, tool_call: dict, state: EpisodeState) -> bool:
        """Check if tool choice is appropriate for current state"""
        # Compare against expected action sequence (gold standard)
        expected_tools = [a["tool"] for a in state.task.expected_actions]
        current_step = state.step
        
        if current_step < len(expected_tools):
            return tool_call["tool"] == expected_tools[current_step]
        
        # If beyond expected sequence, check if it's reasonable
        return tool_call["tool"] in self._reasonable_tools_for_state(state)
    
    def _is_redundant(self, tool_call: dict, state: EpisodeState) -> bool:
        """Check if action repeats previous action unnecessarily"""
        if not state.history:
            return False
        
        last_action, last_result = state.history[-1]
        
        # Same tool with same args
        if (tool_call["tool"] == last_action["tool"] and
            tool_call.get("args") == last_action.get("args")):
            return True
        
        # Reading same file twice without modification in between
        if (tool_call["tool"] == "read_file" and
            last_action["tool"] == "read_file" and
            tool_call["args"]["target_file"] == last_action["args"]["target_file"]):
            return True
        
        return False
```

### Reward Configuration

```python
@dataclass
class RewardConfig:
    """Reward values for different outcomes"""
    
    # Task-level
    task_complete: float = 10.0
    task_failed: float = -5.0
    
    # Per-step rewards
    correct_tool: float = 5.0
    wrong_tool: float = -3.0
    schema_pass: float = 2.0
    schema_fail: float = -5.0
    style_pass: float = 1.0
    
    # Penalties
    step_penalty: float = -0.5
    redundant_action: float = -2.0
    guardrail_violation: float = -10.0
    
    # KL penalty
    kl_weight: float = 0.05
```

### Example Reward Trace

```python
# Task: "Read main.ts and count lines"

# Step 1: {"tool": "read_file", "args": {"target_file": "main.ts"}}
# Reward: +5 (correct) +2 (schema) -0.5 (step) = +6.5

# Step 2: {"tool": "run_terminal_cmd", "args": {"command": "wc -l main.ts"}}
# Reward: +5 (correct) +2 (schema) -0.5 (step) = +6.5

# Task complete
# Reward: +10.0

# Total episode reward: 6.5 + 6.5 + 10.0 = 23.0
```

---

## 6️⃣ Episode Management

### Episode Lifecycle

```python
class EpisodeManager:
    def __init__(self, task_generator: TaskGenerator, simulator: Web4Simulator):
        self.task_generator = task_generator
        self.simulator = simulator
        
    def run_episode(self, policy: PolicyModel) -> EpisodeResult:
        """Run one complete episode"""
        # Select task
        task = self.task_generator.sample_task()
        
        # Reset environment
        obs = self.simulator.reset(task)
        
        # Episode loop
        done = False
        total_reward = 0.0
        steps = []
        
        while not done:
            # Policy generates action
            action = policy.generate_action(obs)
            
            # Execute in simulator
            next_obs, reward, done, info = self.simulator.step(action)
            
            # Record
            steps.append({
                "observation": obs,
                "action": action,
                "reward": reward,
                "info": info,
            })
            
            total_reward += reward
            obs = next_obs
        
        return EpisodeResult(
            task=task,
            steps=steps,
            total_reward=total_reward,
            success=info["reason"] == "success",
            num_steps=len(steps),
        )
```

### Curriculum Learning

```python
class CurriculumScheduler:
    """Gradually increase task difficulty during training"""
    
    def __init__(self):
        self.episode_count = 0
        
    def get_task_distribution(self) -> Dict[Difficulty, float]:
        """Return probability distribution over task difficulties"""
        if self.episode_count < 2000:
            # Phase 1: Mostly simple tasks
            return {
                Difficulty.SIMPLE: 0.7,
                Difficulty.MEDIUM: 0.25,
                Difficulty.HARD: 0.05,
                Difficulty.EXPERT: 0.0,
            }
        elif self.episode_count < 10000:
            # Phase 2: More medium tasks
            return {
                Difficulty.SIMPLE: 0.3,
                Difficulty.MEDIUM: 0.5,
                Difficulty.HARD: 0.15,
                Difficulty.EXPERT: 0.05,
            }
        else:
            # Phase 3: Full distribution
            return {
                Difficulty.SIMPLE: 0.2,
                Difficulty.MEDIUM: 0.4,
                Difficulty.HARD: 0.3,
                Difficulty.EXPERT: 0.1,
            }
    
    def on_episode_end(self, result: EpisodeResult):
        """Update curriculum based on performance"""
        self.episode_count += 1
        # Could adjust distribution based on success rates per difficulty
```

---

## 7️⃣ Task Generation

### Task Categories & Examples

```python
# Category: TOOL_USE (single tool call)
task_tool_use_1 = Task(
    id="tool_use_001",
    description="Read the file src/main.ts",
    category=TaskCategory.TOOL_USE,
    difficulty=Difficulty.SIMPLE,
    initial_files={
        "/workspace/src/main.ts": "console.log('Hello');",
    },
    expected_actions=[
        {"tool": "read_file", "args": {"target_file": "src/main.ts"}},
    ],
    success_criteria=lambda state: any(
        "read_file" in str(action) for action, _ in state.history
    ),
)

# Category: MULTI_STEP (2-3 steps)
task_multi_step_1 = Task(
    id="multi_step_001",
    description="Find all TypeScript files, then read main.ts",
    category=TaskCategory.MULTI_STEP,
    difficulty=Difficulty.MEDIUM,
    initial_files={
        "/workspace/main.ts": "export const x = 1;",
        "/workspace/utils.ts": "export const y = 2;",
    },
    expected_actions=[
        {"tool": "glob_file_search", "args": {"glob_pattern": "*.ts"}},
        {"tool": "read_file", "args": {"target_file": "/workspace/main.ts"}},
    ],
    success_criteria=lambda state: (
        len(state.history) >= 2 and
        "glob_file_search" in str(state.history[0][0]) and
        "read_file" in str(state.history[1][0])
    ),
)

# Category: SEARCH_AND_EDIT
task_search_edit_1 = Task(
    id="search_edit_001",
    description="Find all TODO comments in main.ts and replace them with DONE",
    category=TaskCategory.SEARCH_AND_EDIT,
    difficulty=Difficulty.HARD,
    initial_files={
        "/workspace/main.ts": "// TODO: implement\nfunction foo() {}",
    },
    expected_actions=[
        {"tool": "grep", "args": {"pattern": "TODO", "path": "/workspace/main.ts"}},
        {"tool": "search_replace", "args": {
            "file_path": "/workspace/main.ts",
            "old_string": "// TODO: implement",
            "new_string": "// DONE",
        }},
    ],
    success_criteria=lambda state: (
        state.fs.read("/workspace/main.ts") == "// DONE\nfunction foo() {}"
    ),
)
```

### Task Generator

```python
class TaskGenerator:
    def __init__(self, task_pool: List[Task], curriculum: CurriculumScheduler):
        self.task_pool = task_pool
        self.curriculum = curriculum
        
        # Group by difficulty
        self.by_difficulty = {
            diff: [t for t in task_pool if t.difficulty == diff]
            for diff in Difficulty
        }
    
    def sample_task(self) -> Task:
        """Sample a task according to curriculum"""
        dist = self.curriculum.get_task_distribution()
        
        # Sample difficulty
        difficulty = random.choices(
            list(dist.keys()),
            weights=list(dist.values())
        )[0]
        
        # Sample task from that difficulty
        return random.choice(self.by_difficulty[difficulty])
    
    def add_task(self, task: Task):
        """Dynamically add new task to pool"""
        self.task_pool.append(task)
        self.by_difficulty[task.difficulty].append(task)
```

### Procedural Task Generation

```python
def generate_read_file_task() -> Task:
    """Procedurally generate a read_file task"""
    # Random file structure
    num_files = random.randint(3, 10)
    files = {}
    target_file = None
    
    for i in range(num_files):
        ext = random.choice([".ts", ".js", ".py", ".md"])
        path = f"/workspace/file_{i}{ext}"
        content = f"// Content of file {i}\n" + "\n".join(
            f"line {j}" for j in range(random.randint(10, 100))
        )
        files[path] = content
        
        if i == random.randint(0, num_files - 1):
            target_file = path
    
    return Task(
        id=f"generated_read_{random.randint(1000, 9999)}",
        description=f"Read the file {target_file}",
        category=TaskCategory.TOOL_USE,
        difficulty=Difficulty.SIMPLE,
        initial_files=files,
        expected_actions=[
            {"tool": "read_file", "args": {"target_file": target_file}},
        ],
        success_criteria=lambda state: any(
            action.get("tool") == "read_file" and
            action.get("args", {}).get("target_file") == target_file
            for action, _ in state.history
        ),
    )
```

---

## 8️⃣ Validation & Testing

### Unit Tests

```python
def test_mock_file_system():
    """Test basic file system operations"""
    fs = MockFileSystem()
    fs.reset({"/workspace/test.txt": "hello"})
    
    assert fs.read("/workspace/test.txt") == "hello"
    assert fs.exists("/workspace/test.txt")
    assert not fs.exists("/workspace/missing.txt")
    
    fs.write("/workspace/new.txt", "world")
    assert fs.read("/workspace/new.txt") == "world"

def test_read_file_tool():
    """Test read_file tool execution"""
    fs = MockFileSystem()
    fs.reset({"/workspace/test.ts": "line1\nline2\nline3"})
    
    tool = ReadFileTool()
    result = tool.execute({"target_file": "/workspace/test.ts"}, fs)
    
    assert "line1" in result
    assert "line2" in result
    assert "line3" in result

def test_reward_computation():
    """Test reward calculation"""
    config = RewardConfig()
    computer = RewardComputer(config)
    
    # Correct tool
    assert computer.correct_tool() == 5.0
    
    # JSON error
    assert computer.json_error() < 0
    
    # Guardrail violation
    assert computer.guardrail_violation() < -5.0
```

### Integration Tests

```python
def test_full_episode():
    """Test complete episode execution"""
    task = Task(
        id="test_001",
        description="Read main.ts",
        category=TaskCategory.TOOL_USE,
        difficulty=Difficulty.SIMPLE,
        initial_files={"/workspace/main.ts": "content"},
        expected_actions=[
            {"tool": "read_file", "args": {"target_file": "/workspace/main.ts"}},
        ],
        success_criteria=lambda state: len(state.history) > 0,
    )
    
    simulator = Web4Simulator(SimulatorConfig())
    obs = simulator.reset(task)
    
    # Execute correct action
    action = '{"tool": "read_file", "args": {"target_file": "/workspace/main.ts"}}'
    obs, reward, done, info = simulator.step(action)
    
    assert reward > 0  # Positive reward for correct action
    assert done  # Task should complete
    assert info["reason"] == "success"
```

### Determinism Validation

```python
def test_determinism():
    """Ensure same actions produce same results"""
    task = load_task("test_task_001")
    simulator1 = Web4Simulator(SimulatorConfig(seed=42))
    simulator2 = Web4Simulator(SimulatorConfig(seed=42))
    
    actions = [
        '{"tool": "read_file", "args": {"target_file": "/workspace/main.ts"}}',
        '{"tool": "grep", "args": {"pattern": "TODO"}}',
    ]
    
    # Run both simulators
    results1 = run_episode(simulator1, task, actions)
    results2 = run_episode(simulator2, task, actions)
    
    # Should be identical
    assert results1.total_reward == results2.total_reward
    assert results1.success == results2.success
    assert len(results1.steps) == len(results2.steps)
```

### Performance Benchmarks

```python
def benchmark_episode_speed():
    """Measure episode execution speed"""
    simulator = Web4Simulator(SimulatorConfig())
    task = load_task("benchmark_task")
    
    num_episodes = 100
    start = time.time()
    
    for _ in range(num_episodes):
        obs = simulator.reset(task)
        done = False
        while not done:
            action = sample_random_action()  # Random policy
            obs, reward, done, info = simulator.step(action)
    
    elapsed = time.time() - start
    episodes_per_sec = num_episodes / elapsed
    
    print(f"Episodes/sec: {episodes_per_sec:.2f}")
    assert episodes_per_sec > 10  # Target: >10 episodes/sec
```

---

## 🔧 Implementation Checklist

### Core Components
- [ ] Implement `MockFileSystem` class
- [ ] Implement `Web4Simulator` environment
- [ ] Implement `RewardComputer` with all components
- [ ] Implement `EpisodeManager` for lifecycle

### Tools
- [ ] `read_file` tool
- [ ] `write` tool
- [ ] `search_replace` tool
- [ ] `grep` tool
- [ ] `glob_file_search` tool
- [ ] `codebase_search` tool (mock)
- [ ] `list_dir` tool
- [ ] `run_terminal_cmd` tool (safe subset)

### Task Generation
- [ ] Create 50+ handcrafted tasks (10 per difficulty)
- [ ] Implement procedural task generation
- [ ] Implement `TaskGenerator` with sampling
- [ ] Implement `CurriculumScheduler`

### Validation
- [ ] Unit tests for all tools
- [ ] Integration tests for episodes
- [ ] Determinism validation
- [ ] Performance benchmarks

### Integration with RL
- [ ] OpenAI Gym API compatibility
- [ ] TRL library integration
- [ ] Logging and monitoring hooks
- [ ] Checkpoint save/load for reproducibility

---

## 📚 References

- **OpenAI Gym:** Environment API standard
- **Stable Baselines3:** RL algorithm implementations
- **TRL (Transformer RL):** HuggingFace RL library
- **SimPy:** Discrete event simulation (if needed for async tools)

---

**End of Simulator Design**  
**Version:** 1.0  
**Date:** 2025-10-27

