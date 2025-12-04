# Structon System — Comprehensive Checkpoint

> **Last Updated:** December 4, 2024

---

## 1. Core Philosophy

### The Big Idea
> **"Program intentions, not instructions — the system figures out and improves how to achieve them."**

### Key Principles

| Principle | Meaning |
|-----------|---------|
| **Code is Data** | Everything is JSON. Agents, memory, logic — all data that can be generated, modified, inspected |
| **Self-Similarity** | One pattern everywhere: sense-act-feedback. Memories, tasks, agents all follow same structure |
| **Tension-Driven** | Unresolved states create drive. High tension = needs attention. Resolving tension = progress |
| **Living Memory** | Memory is activity, not storage. Memories sense relevance, activate when needed, evolve through feedback |
| **Self-Improvement** | Agents evaluate their own output, improve if needed, learn from experience |

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      STRUCTON SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    PYTHON LAYER                       │  │
│  │              (Minimal Bootstrap Only)                 │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Interpreter    Atomics (32)    Factory    Memory    │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   STRUCTON LAYER                      │  │
│  │                (Everything is JSON)                   │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Agents    Tasks    Memories    Blueprints    Meta   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Core Modules

### File Structure

```
src/core/
├── schema.py       # What structons ARE (data structures)
├── atomics.py      # What structons DO (32 primitive operations)
├── interpreter.py  # How structons RUN (execution engine)
├── tension.py      # What DRIVES structons (motivation system)
├── memory.py       # How structons REMEMBER (living memory)
├── factory.py      # How to CREATE structons (helpers)
└── __init__.py     # Exports all
```

### Module Responsibilities

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `schema.py` | Define structon data structures | `Structon`, `Node`, `Edge`, `Phase` |
| `atomics.py` | 32 primitive operations | `call_llm`, `load_memories`, `run_structon`, etc. |
| `interpreter.py` | Execute structons | `Interpreter.run()`, topological sort |
| `tension.py` | Calculate and propagate tension | `calculate_tension`, `propagate_tension_up` |
| `memory.py` | Living memory system | `LivingMemory`, `MemoryStructon` |
| `factory.py` | Create valid structons | `quick_llm_structon`, `create_from_blueprint` |

---

## 4. Structon Schema

### Basic Structure

```json
{
  "structure_id": "unique_id",
  "structure_type": "composite",
  "intent": "What this structon does",
  "description": "Detailed description",
  "phases": ["sense", "act", "feedback"],
  "tension": 0.5,
  "importance": 0.5,
  "nodes": [...],
  "edges": [...]
}
```

### Node Structure

```json
{
  "id": "a1",
  "type": "process",
  "phase": "act",
  "description": "What this node does",
  "atomic": "call_llm",
  "input": "$previous_output",
  "args": {"prompt": "Do something: {input}"},
  "output": "$result"
}
```

### Phases (Sense-Act-Feedback)

| Phase | Purpose | Typical Atomics |
|-------|---------|-----------------|
| **Sense** | Gather input, detect context | `get`, `load_memories`, `sense_memories` |
| **Act** | Process, transform, generate | `call_llm`, `run_structon`, `activate_memories` |
| **Feedback** | Output, learn, update state | `emit`, `learn_from_experience`, `update_memory` |

---

## 5. Atomics (32 Operations)

### Categories

```
Data:       get, set, merge, filter, map, first, sort, diff
Control:    if, loop, branch
Structon:   load_structon, save_structon, query_structons, 
            create_structon, update_structon
Memory:     load_memories, sense_memories, activate_memories,
            create_memory, update_memory, learn_from_experience
Meta:       run_structon
LLM:        call_llm, parse_response, validate_json
I/O:        emit, log, read_input
Tension:    calculate_tension, propagate_tension, get_highest_tension
```

### Key Atomics

| Atomic | Purpose |
|--------|---------|
| `call_llm` | Call LLM with prompt |
| `run_structon` | Run another structon (enables composition) |
| `load_memories` | Load all memories from disk |
| `sense_memories` | Calculate relevance to context |
| `activate_memories` | Get top-k relevant memories |
| `learn_from_experience` | Extract and save lesson from task |

---

## 6. Memory System

### Memory as Activity (Not Storage)

```
Traditional: Store → Query → Retrieve (passive)
Structon:    Sense → Activate → Participate → Evolve (active)
```

### MemoryStructon

```json
{
  "id": "mem_20251204...",
  "intent": "How to explain concepts",
  "content": {"lesson": "Use analogies and examples"},
  "sense_patterns": ["explain", "what is", "how does"],
  "tension": 0.72,
  "success_rate": 0.85,
  "times_used": 5,
  "last_activated": "2024-12-04T14:20:00"
}
```

### Memory Lifecycle

```
Experience → Learn (extract lesson) → Store (JSON file)
    ↓
Context → Sense (calculate relevance) → Activate (participate)
    ↓
Outcome → Feedback (update tension/success) → Evolve
    ↓
Low value → Prune (remove)
```

### Feedback Effects

| Outcome | Tension | Success Rate | Meaning |
|---------|---------|--------------|---------|
| Success | ↓ 0.9× | ↑ increases | "This works, confident" |
| Failure | ↑ 1.15× | ↓ decreases | "Needs attention" |

---

## 7. Factory System

### Quick Creation

```python
from src.core import quick_llm_structon, save_structon

# Create agent in one line
agent = quick_llm_structon(
    intent="Summarize text",
    prompt="Summarize this: {input}",
    learn=True  # Adds learning node
)

# Save it
save_structon(agent, "summarizer.json")
```

### From Blueprint

```python
from src.core import create_from_blueprint

agent = create_from_blueprint(
    blueprint_name="agent",
    intent="Research quantum computing",
    customizations={"prompt": "Research: {input}"}
)
```

### Full Control

```python
from src.core import create_structon, create_node

nodes = [
    create_node("s1", "get", "sense", "input", "Get topic", 
                args={"key": "topic"}, output_var="$topic"),
    create_node("a1", "call_llm", "act", "process", "Research",
                "$topic", {"prompt": "Research: {input}"}, "$result"),
    create_node("f1", "emit", "feedback", "output", "Return",
                "$result", {}, "$output")
]

agent = create_structon(
    intent="Research agent",
    nodes=nodes,
    edges=[{"from": "s1", "to": "a1"}, {"from": "a1", "to": "f1"}]
)
```

---

## 8. Execution Flow

### Running a Structon

```python
from src.core import Interpreter, Structon, set_interpreter

# Setup
interpreter = Interpreter()
set_interpreter(interpreter)  # Enable run_structon atomic

# Load and run
agent = Structon.from_dict(agent_data)
result = interpreter.run(agent, {"topic": "quantum computing"})

# Result contains
result["result"]   # Final output
result["success"]  # True/False
result["errors"]   # Any errors
result["context"]  # Full execution context
```

### Execution Order

1. Topological sort of nodes based on edges
2. Execute nodes in order
3. Each node: get input → call atomic → store output
4. Variable substitution: `$var` → actual value
5. Return final result

---

## 9. Directory Structure

```
structon/
├── src/core/              # Core modules (6 files)
│   ├── schema.py
│   ├── atomics.py
│   ├── interpreter.py
│   ├── tension.py
│   ├── memory.py
│   ├── factory.py
│   └── __init__.py
│
├── structons/             # Your agents (JSON)
│   ├── research_agent.json
│   ├── memory_sense.json
│   └── ...
│
├── blueprints/            # Templates (JSON)
│   ├── composite_blueprint.json
│   ├── memory_blueprint.json
│   └── agent_blueprint.json
│
├── memory/                # Persisted memories (JSON)
│   ├── mem_20251204....json
│   └── ...
│
├── examples/              # Example scripts
│   ├── research_agent.py
│   ├── test_structon_agent.py
│   └── ...
│
└── tests/                 # Unit tests
    └── test_core.py
```

---

## 10. Proven Capabilities

| Capability | Status | Evidence |
|------------|--------|----------|
| Structon execution | ✅ | All tests pass |
| LLM integration | ✅ | OpenAI/Anthropic working |
| Code is data | ✅ | Agents defined entirely in JSON |
| Self-improvement | ✅ | Score improved 5→10 in tests |
| Living memory | ✅ | Memories persist, activate, evolve |
| Memory improves output | ✅ | 8/10 → 9/10 with memory |
| Learning from experience | ✅ | New memories created automatically |
| Structons calling structons | ✅ | `run_structon` atomic works |
| Factory creation | ✅ | One-line agent creation |

---

## 11. Key Insights

### Memory as Activity
> "Memory isn't WHERE things are stored. Memory is things COMING ALIVE again."

### Self-Similarity
> "One pattern (sense-act-feedback) at every level. Memories, tasks, agents — all same shape."

### Code is Data
> "LLM generates JSON → JSON executes → AI writes its own programs"

### Tension as Drive
> "Unresolved states create tension. High tension demands attention. Resolving tension = progress."

### Living System
> "LLM is the frozen brain. Structon is the living body. Together, they might be the first thing meaningfully 'alive' in silicon."

---

## 12. Usage Patterns

### Pattern 1: Simple Agent

```python
agent = quick_llm_structon("Explain", "Explain: {input}")
result = interpreter.run(Structon.from_dict(agent), {"input": "gravity"})
```

### Pattern 2: Agent with Memory

```python
# Load memories
memories = LivingMemory()
memories.sense("quantum computing")
active = memories.activate(top_k=3)

# Use in prompt
context = "\n".join([m.content["lesson"] for m in active])
# ... include in LLM prompt
```

### Pattern 3: Agent with Learning

```python
agent = quick_llm_structon("Research", "Research: {input}", learn=True)
# Agent automatically learns from each execution
```

### Pattern 4: Composable Agents

```python
# research_agent calls memory_sense via run_structon
{
  "atomic": "run_structon",
  "args": {"structon_id": "memory_sense"}
}
```

---

## 13. Configuration

### Environment Variables

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o"  # Optional, default: gpt-4o

# Or Anthropic
export ANTHROPIC_API_KEY="sk-..."
```

### Default Paths

```python
STRUCTON_STORAGE_PATH = "./structons"
MEMORY_DIR = "./memory"
BLUEPRINT_DIR = "./blueprints"
```

---

## 14. Future Directions

| Direction | Description |
|-----------|-------------|
| **Pure Structon Loop** | Evolution loop as structon, not Python |
| **Multi-Agent** | Agents coordinating with each other |
| **Real Web Search** | Web search atomic with real API |
| **Error Recovery** | Graceful handling of failures |
| **Production API** | REST API for running structons |
| **Visual Editor** | GUI for building structons |
| **Marketplace** | Share and discover structons |

---

## 15. Quick Start

```python
import sys
import os
sys.path.insert(0, os.getcwd())

from src.core import (
    quick_llm_structon,
    Structon,
    Interpreter,
    set_interpreter,
    LivingMemory
)

# Setup
interpreter = Interpreter()
set_interpreter(interpreter)

# Create and run agent
agent = quick_llm_structon("My Agent", "Do: {input}", learn=True)
result = interpreter.run(Structon.from_dict(agent), {"input": "hello"})
print(result["result"])
```

---

## 16. One-Sentence Summary

> **Structon is a self-improving, memory-aware AI agent framework where code is data — agents are JSON that can be generated, modified, and evolved by LLMs.**

---

**This checkpoint captures the complete system state as of December 4, 2024.** 🚀
