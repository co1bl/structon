# Structon: A Self-Improving Cognitive Architecture for LLMs

**Author:** ImagineTask  
**Date:** December 2024  
**Version:** 1.0  
**Repository:** [github.com/co1bl/structon](https://github.com/co1bl/structon)

---

## Abstract

This document presents Structon, a cognitive architecture that transforms Large Language Models (LLMs) from passive responders into autonomous, goal-directed agents. Through a series of experiments, we demonstrate three key findings:

1. **Code is Data**: LLMs can generate executable cognitive structures (structons) that control their own behavior
2. **Self-Similar Architecture**: A single pattern (sense → act → feedback) scales to arbitrary complexity
3. **Autonomous Self-Improvement**: Systems can evaluate their own output and iteratively improve without human intervention

In our experiments, a self-improving loop evolved from a 5/10 score to 10/10 in just 3 iterations, proving that autonomous cognitive improvement is achievable with current technology.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [The Problem](#2-the-problem)
3. [Core Concepts](#3-core-concepts)
4. [Architecture](#4-architecture)
5. [Experiments & Results](#5-experiments--results)
6. [Implications](#6-implications)
7. [Limitations & Future Work](#7-limitations--future-work)
8. [Conclusion](#8-conclusion)

---

## 1. Introduction

Large Language Models represent a breakthrough in artificial intelligence—they can reason, write, code, and analyze with remarkable capability. Yet they remain fundamentally passive: they respond when prompted, but they don't pursue goals, maintain memory across sessions, or improve themselves.

**Structon bridges this gap.**

Structon is a minimal cognitive architecture that provides the "missing layer" between raw intelligence (LLM) and functional agency. By combining:

- **Structure** (JSON-based cognitive units)
- **Drive** (tension as motivating force)  
- **Recursion** (self-similar patterns at every scale)

...we create systems that can generate their own code, evaluate their own output, and improve their own performance—autonomously.

---

## 2. The Problem

### 2.1 The Intelligence-Agency Gap

Current LLMs are powerful but limited:

| LLM Alone | What's Missing |
|-----------|----------------|
| Responds to prompts | No persistent goals |
| Stateless | No memory across sessions |
| Passive | No intrinsic motivation |
| Fixed behavior | No self-improvement |

An LLM is like a brilliant consultant who forgets everything between meetings and only speaks when spoken to.

### 2.2 Why This Matters

To build truly useful AI systems, we need agents that can:

- Maintain goals over time
- Remember and learn from experience
- Improve their own performance
- Operate with minimal human intervention

Structon provides the architectural foundation for all of these capabilities.

---

## 3. Core Concepts

### 3.1 What is a Structon?

A structon is a **self-contained unit of cognition** represented as JSON data. Every structon has three phases:

```
┌─────────────────────────────────────────┐
│            STRUCTON                     │
├─────────────────────────────────────────┤
│  SENSE    →  Perceive current state     │
│  ACT      →  Do something about it      │
│  FEEDBACK →  Learn from the result      │
└─────────────────────────────────────────┘
```

### 3.2 Self-Similarity

The same pattern applies at every scale:

```
SYSTEM level:   sense → act → feedback
STRUCTON level: sense → act → feedback
NODE level:     input → process → output
```

This is analogous to fractals in mathematics or DNA in biology—simple rules that generate unlimited complexity.

### 3.3 Tension as Drive

Every structon has a **tension** value (0.0 to 1.0):

- High tension = unresolved, needs attention
- Low tension = resolved, complete

The system always works on the highest-tension item, providing intrinsic motivation without explicit programming.

```python
tension = (
    importance × 0.3 +
    urgency × 0.3 +
    unresolved × 0.2 +
    blocking × 0.2
)
```

### 3.4 Code is Data

In Structon, there is no distinction between code and data. A structon is:

- **Data**: JSON that can be stored, transmitted, inspected
- **Code**: Instructions that the interpreter executes

This means LLMs can generate structons, and those structons can run as programs.

---

## 4. Architecture

### 4.1 System Components

```
┌─────────────────────────────────────────────────────────┐
│                      STRUCTON SYSTEM                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌──────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │  Schema  │    │  Interpreter │    │  LLM Layer   │  │
│   │  (JSON)  │───▶│  (Executor)  │◀──▶│  (OpenAI/    │  │
│   │          │    │              │    │   Anthropic) │  │
│   └──────────┘    └──────────────┘    └──────────────┘  │
│         │                │                    │          │
│         ▼                ▼                    ▼          │
│   ┌──────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │ Atomics  │    │   Tension    │    │  Generator   │  │
│   │ (25 ops) │    │   Manager    │    │  & Evolver   │  │
│   └──────────┘    └──────────────┘    └──────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Structon Schema

```json
{
  "structure_id": "example_001",
  "structure_type": "composite",
  "intent": "answer_question",
  "phases": ["sense", "act", "feedback"],
  "tension": 0.8,
  "importance": 0.7,
  "nodes": [
    {
      "id": "s1",
      "type": "input",
      "phase": "sense",
      "atomic": "get",
      "args": {"key": "question"},
      "output": "$question"
    },
    {
      "id": "a1", 
      "type": "process",
      "phase": "act",
      "atomic": "call_llm",
      "input": "$question",
      "args": {"prompt": "Answer: {input}"},
      "output": "$answer"
    },
    {
      "id": "f1",
      "type": "output",
      "phase": "feedback",
      "atomic": "emit",
      "input": "$answer"
    }
  ],
  "edges": [
    {"from": "s1", "to": "a1"},
    {"from": "a1", "to": "f1"}
  ]
}
```

### 4.3 Atomic Functions

The system includes ~25 primitive operations:

| Category | Functions |
|----------|-----------|
| Data | get, set, merge, filter, map, sort, diff |
| Control | if, loop, branch |
| Structon | load, save, query, create, update |
| LLM | call_llm, parse_response, validate_json |
| I/O | emit, log, read_input |
| Tension | calculate, propagate, get_highest |

These are the **only** real code. Everything else is data.

---

## 5. Experiments & Results

### 5.1 Experiment 1: Basic Execution

**Goal:** Verify the sense-act-feedback loop works.

**Method:** Create a simple Q&A structon, execute with interpreter.

**Result:**
```
✅ Success!
Execution History:
  ✓ s1: completed (SENSE - got question)
  ✓ a1: completed (ACT - called LLM)  
  ✓ f1: completed (FEEDBACK - emitted result)
```

**Finding:** The core architecture functions correctly.

---

### 5.2 Experiment 2: Code is Data

**Goal:** Prove that LLMs can generate executable structons.

**Method:** 
1. Ask LLM to generate a structon for "fun facts about a topic"
2. Parse the JSON into a Structon object
3. Execute it with the interpreter

**Result:**
```
[1] LLM Generating Structon...
    Created: fun_fact_generator

[2] Converting Data to Executable...
    ✅ Valid structon created

[3] Executing Generated Structon...
    ✅ CODE IS DATA - PROVEN!
    
Result: [Comprehensive facts about honey bees...]
```

**Finding:** LLMs can write their own programs as data structures.

---

### 5.3 Experiment 3: Evolution

**Goal:** Prove that structons can improve through feedback.

**Method:**
1. Create v1 structon (brief explanation)
2. Evaluate result (score 1-10)
3. Evolve based on feedback
4. Create v2 structon (comprehensive)
5. Compare scores

**Result:**
```
v1 (brief):         111 chars, Score: 6/10
v2 (comprehensive): 3,216 chars, Score: 9/10

✅ EVOLUTION WORKS - v2 is more comprehensive
```

**Finding:** Feedback-driven improvement produces measurably better results.

---

### 5.4 Experiment 4: Autonomous Self-Improvement

**Goal:** Prove fully autonomous improvement loop.

**Method:**
1. Start with weak prompt (score ~5)
2. Run → Evaluate → Evolve → Repeat
3. Stop when score ≥ 9
4. No human intervention

**Result:**
```
🔄 ITERATION 1
   Score: 5/10
   Missing: EPR paradox, Bell's theorem...
   📈 Evolving...

🔄 ITERATION 2
   Score: 8/10
   Missing: Applications...
   📈 Evolving...

🔄 ITERATION 3
   Score: 10/10
   ✅ TARGET REACHED!

Progression:
  v1: [█████░░░░░]  5/10 |  478 chars
  v2: [████████░░]  8/10 |  759 chars
  v3: [██████████] 10/10 |  858 chars

🎉 SELF-IMPROVEMENT SUCCESSFUL!
   System evolved from 5/10 to 10/10
```

**Finding:** Autonomous self-improvement is achievable with current technology.

---

### 5.5 Summary of Results

| Experiment | Hypothesis | Result |
|------------|------------|--------|
| Basic Execution | Sense-act-feedback works | ✅ Proven |
| Code is Data | LLM can generate executable structons | ✅ Proven |
| Evolution | Feedback improves performance | ✅ Proven (6→9) |
| Autonomous Loop | Self-improvement without humans | ✅ Proven (5→10) |

---

## 6. Implications

### 6.1 For AI Development

Structon demonstrates that **agency is architectural, not emergent**. We don't need to wait for more powerful models—we can build agentic systems today by adding the right structure.

### 6.2 For Software Engineering

The "code is data" principle enables:
- Programs that modify themselves
- Runtime code generation
- Inspectable, debuggable AI behavior
- Version-controlled cognition

### 6.3 For AGI Research

Structon may represent one of the missing pieces in the AGI puzzle:

```
Intelligence (LLM)     = 50% of AGI
Agency (Structon)      = 25% of AGI
Embodiment + Grounding = 25% of AGI (still missing)
```

The architecture provides the "operating system" for artificial general intelligence.

### 6.4 Comparison to Existing Approaches

| Approach | Strengths | Limitations |
|----------|-----------|-------------|
| LangChain | Easy chaining | No self-improvement |
| AutoGPT | Autonomous | No structured memory |
| Semantic Kernel | Enterprise-ready | Complex, not self-similar |
| **Structon** | Self-similar, self-improving | Early stage |

---

## 7. Limitations & Future Work

### 7.1 Current Limitations

1. **Hybrid Implementation**: The evolution loop currently uses Python control flow, not pure structons
2. **No Persistence**: Structons don't persist across sessions yet
3. **Limited Testing**: Only tested on explanation tasks
4. **No Nesting**: Haven't validated deep structon recursion

### 7.2 Future Work

| Priority | Task | Impact |
|----------|------|--------|
| High | Pure structon evolution loop | Architectural completeness |
| High | Persistence layer | Long-term memory |
| Medium | Research agent demo | Practical validation |
| Medium | Multi-agent coordination | Scalability |
| Low | Embodiment integration | AGI pathway |

### 7.3 Open Questions

1. How deep can structon nesting go before coherence degrades?
2. Can structons develop emergent behaviors not explicitly programmed?
3. What's the optimal tension propagation formula?
4. How do we prevent infinite self-modification loops?

---

## 8. Conclusion

Structon represents a minimal but complete cognitive architecture that bridges the gap between LLM intelligence and functional agency. Through four experiments, we demonstrated:

1. **The core loop works**: Sense-act-feedback executes correctly
2. **Code is data**: LLMs can generate executable cognitive structures
3. **Evolution works**: Feedback produces measurable improvement (6→9)
4. **Autonomy is possible**: Self-improvement from 5/10 to 10/10 without human intervention

The key insight is that **agency emerges from structure, not just intelligence**. By providing LLMs with the right architectural scaffolding—persistent goals, tension-driven selection, and self-similar patterns—we can create systems that pursue goals, learn from experience, and improve themselves.

This is not AGI. But it may be one of the essential pieces.

---

## Appendix A: Quick Start

```bash
# Clone repository
git clone https://github.com/co1bl/structon.git
cd structon

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="your-key-here"

# Run examples
python examples/hello_world.py
python examples/reasoning_loop.py --simple
python examples/code_is_data.py
python examples/evolution_experiment.py
```

---

## Appendix B: Key Files

| File | Purpose |
|------|---------|
| `src/core/schema.py` | Structon data classes |
| `src/core/atomics.py` | 25 primitive operations |
| `src/core/interpreter.py` | Execution engine |
| `src/core/tension.py` | Tension calculation |
| `src/llm/generator.py` | LLM integration |
| `examples/` | Working examples |
| `tests/` | Unit tests |

---

## Appendix C: The Four Rules

1. **Everything is a structon** — Tasks, knowledge, feedback, even the system's self-model
2. **Structons contain structons** — Infinite nesting, same rules at every level
3. **Tension drives action** — Always work on highest-tension item
4. **Feedback evolves structure** — Results improve the structon itself

---

## References

- Hofstadter, D. (1979). *Gödel, Escher, Bach: An Eternal Golden Braid*
- Minsky, M. (1986). *The Society of Mind*
- Brooks, R. (1991). Intelligence Without Representation
- Vaswani et al. (2017). Attention Is All You Need
- OpenAI (2023). GPT-4 Technical Report

---

## Citation

```bibtex
@software{structon2024,
  title = {Structon: A Self-Improving Cognitive Architecture for LLMs},
  author = {ImagineTask},
  year = {2024},
  url = {https://github.com/co1bl/structon}
}
```

---

## License

MIT License — See [LICENSE](../LICENSE) for details.

---

*"The atom of cognition. Sense. Act. Feedback. Repeat."*
