# Structon: Getting Started Tutorial

## Introduction

This tutorial will guide you through building your first structon-based system.

---

## Prerequisites

- Python 3.10+
- An LLM API key (Anthropic or OpenAI)

## Installation

```bash
git clone https://github.com/ImagineTask/structon.git
cd structon
pip install -r requirements.txt
```

Set your API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
# or
export OPENAI_API_KEY="your-key-here"
```

---

## Step 1: Understanding Structons

A structon is a cognitive unit with three phases:

```
SENSE → ACT → FEEDBACK
```

Here's the simplest possible structon:

```json
{
  "structure_id": "hello_001",
  "structure_type": "simple",
  "intent": "say_hello",
  "phases": ["sense", "act", "feedback"],
  "tension": 0.8,
  "importance": 0.5,
  "nodes": [
    {
      "id": "s1",
      "phase": "sense",
      "type": "input",
      "description": "Get name to greet",
      "atomic": "get",
      "args": {"key": "name"},
      "output": "$name"
    },
    {
      "id": "a1",
      "phase": "act",
      "type": "process",
      "description": "Create greeting",
      "atomic": "call_llm",
      "input": "$name",
      "args": {"prompt": "Say hello to {$name}"},
      "output": "$greeting"
    },
    {
      "id": "f1",
      "phase": "feedback",
      "type": "output",
      "description": "Output result",
      "atomic": "emit",
      "input": "$greeting",
      "output": "$result"
    }
  ],
  "edges": [
    {"from": "s1", "to": "a1"},
    {"from": "a1", "to": "f1"}
  ]
}
```

---

## Step 2: Running Your First Structon

```python
from structon import Structon, Interpreter

# Create interpreter
interpreter = Interpreter()

# Load structon
structon = Structon.from_file("hello.json")

# Provide input
context = {"name": "World"}

# Run
result = interpreter.run(structon, context)

print(result)  # "Hello, World!"
```

---

## Step 3: Understanding Tension

Tension drives what gets processed. Higher tension = higher priority.

```python
from structon import calculate_tension

structon.importance = 0.8  # How important is this?
structon.urgency = 0.9     # How soon must it be done?

tension = calculate_tension(structon)
print(f"Tension: {tension}")  # ~0.85
```

When tension is resolved (task complete), it drops:

```python
structon.resolve()
print(f"Tension: {structon.tension}")  # ~0.1
```

---

## Step 4: Nesting Structons

Structons can contain other structons:

```json
{
  "structure_id": "composite_001",
  "intent": "research_topic",
  "nodes": [
    {
      "id": "n1",
      "phase": "sense",
      "type": "sub_structon",
      "structon_ref": "gather_sources",
      "output": "$sources"
    },
    {
      "id": "n2",
      "phase": "act",
      "type": "sub_structon",
      "structon_ref": "analyze_sources",
      "input": "$sources",
      "output": "$analysis"
    },
    {
      "id": "n3",
      "phase": "feedback",
      "type": "sub_structon",
      "structon_ref": "synthesize_findings",
      "input": "$analysis",
      "output": "$report"
    }
  ]
}
```

Each sub-structon is itself sense-act-feedback. **Same pattern at every scale.**

---

## Step 5: The Main Loop

The main loop runs until tension is resolved:

```python
from structon import MainLoop

loop = MainLoop(root_structon)

# Run until tension < 0.1
result = loop.run(threshold=0.1, max_iterations=100)

print(f"Final result: {result}")
print(f"Iterations: {loop.iterations}")
```

What happens each iteration:

1. **Sense** — Load state, find highest tension
2. **Select** — Pick structon with highest tension
3. **Act** — Execute the structon
4. **Feedback** — Capture result
5. **Evolve** — LLM improves structon if needed
6. **Propagate** — Update tensions throughout tree

---

## Step 6: LLM-Generated Structons

Let the LLM generate structons for you:

```python
from structon import Generator

generator = Generator()

# Generate from task description
structon = generator.generate(
    task="Analyze the sentiment of customer reviews",
    blueprint="analysis_blueprint"
)

# Run it
result = interpreter.run(structon, {"reviews": reviews})
```

---

## Step 7: Evolution Through Feedback

Structons improve over time:

```python
from structon import Evolver

evolver = Evolver()

# Run and get feedback
result = interpreter.run(structon, context)
feedback = {
    "success": result.success,
    "error": result.error,
    "duration": result.duration
}

# Evolve based on feedback
evolved = evolver.evolve(structon, feedback)

# Save the improved version
evolved.save()
```

---

## Step 8: Building a Complete Agent

Putting it all together:

```python
from structon import Agent

# Create agent with root goal
agent = Agent(
    goal="Help user with research tasks",
    blueprints=["research", "analysis", "synthesis"]
)

# Run continuously
while True:
    user_input = input("You: ")
    
    if user_input == "quit":
        break
    
    # Agent processes input through structon system
    response = agent.process(user_input)
    
    print(f"Agent: {response}")
    print(f"Active structons: {agent.active_count}")
    print(f"Total tension: {agent.total_tension}")
```

---

## Example: Research Agent

Complete example of a research agent:

```python
from structon import Agent, Structon

# Define the research structon
research_structon = Structon({
    "structure_id": "research_agent",
    "intent": "research_and_synthesize",
    "phases": ["sense", "act", "feedback"],
    "tension": 0.9,
    "nodes": [
        # SENSE: Understand the question
        {
            "id": "understand",
            "phase": "sense",
            "atomic": "call_llm",
            "args": {"prompt": "What is the user asking about? {$question}"},
            "output": "$understanding"
        },
        # SENSE: Break into sub-questions
        {
            "id": "decompose",
            "phase": "sense",
            "atomic": "call_llm",
            "input": "$understanding",
            "args": {"prompt": "Break this into 3 sub-questions"},
            "output": "$sub_questions"
        },
        # ACT: Research each sub-question
        {
            "id": "research",
            "phase": "act",
            "atomic": "map",
            "input": "$sub_questions",
            "args": {"function": "research_sub_question"},
            "output": "$findings"
        },
        # ACT: Synthesize findings
        {
            "id": "synthesize",
            "phase": "act",
            "atomic": "call_llm",
            "input": "$findings",
            "args": {"prompt": "Synthesize these findings into a coherent answer"},
            "output": "$synthesis"
        },
        # FEEDBACK: Evaluate quality
        {
            "id": "evaluate",
            "phase": "feedback",
            "atomic": "call_llm",
            "input": "$synthesis",
            "args": {"prompt": "Rate this answer 1-10 and explain why"},
            "output": "$evaluation"
        },
        # FEEDBACK: Output result
        {
            "id": "output",
            "phase": "feedback",
            "atomic": "emit",
            "input": ["$synthesis", "$evaluation"],
            "output": "$result"
        }
    ],
    "edges": [
        {"from": "understand", "to": "decompose"},
        {"from": "decompose", "to": "research"},
        {"from": "research", "to": "synthesize"},
        {"from": "synthesize", "to": "evaluate"},
        {"from": "evaluate", "to": "output"}
    ]
})

# Run the agent
from structon import Interpreter

interpreter = Interpreter()
result = interpreter.run(research_structon, {
    "question": "What are the implications of quantum computing for cryptography?"
})

print(result)
```

---

## Next Steps

1. **Explore blueprints** — See `blueprints/` for templates
2. **Add custom atomics** — Extend `src/core/atomics.py`
3. **Build complex agents** — Nest structons for complex reasoning
4. **Contribute** — See `CONTRIBUTING.md`

---

## Key Concepts to Remember

1. **sense → act → feedback** — The fundamental loop
2. **Tension drives action** — High tension = high priority
3. **Everything is structon** — Nest infinitely
4. **LLM generates and evolves** — Intelligence from LLM, structure from structon
5. **Same pattern at all scales** — Self-similar, fractal
