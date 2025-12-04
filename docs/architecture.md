# Structon: Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        BLUEPRINT                            │
│              (template for valid structons)                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                          LLM                                │
│         (generates and evolves structons)                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       STRUCTONS                             │
│    (self-similar, nested, sense-act-feedback units)         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   ATOMIC FUNCTIONS                          │
│           (~20-30 primitives, only real code)               │
└─────────────────────────────────────────────────────────────┘
```

---

## Structon Schema

```json
{
  "structure_id": "string (UUID)",
  "structure_type": "string (sense|act|feedback|composite)",
  "intent": "string (what this structon does)",
  
  "phases": ["sense", "act", "feedback"],
  
  "tension": 0.0-1.0,
  "importance": 0.0-1.0,
  
  "nodes": [
    {
      "id": "string",
      "type": "string (input|process|output|sub_structon)",
      "phase": "string (sense|act|feedback)",
      "description": "string",
      "atomic": "string (atomic function name)",
      "structon_ref": "string (for nested structons)",
      "input": "string or array (variable references)",
      "output": "string (variable name)",
      "args": {}
    }
  ],
  
  "edges": [
    {"from": "node_id", "to": "node_id"}
  ],
  
  "tension_profile": {
    "max_tension": 0.0-1.0,
    "node_conflicts": [],
    "barriers": [],
    "unresolved_desires": []
  },
  
  "metadata": {
    "created_at": "ISO timestamp",
    "updated_at": "ISO timestamp",
    "version": "integer",
    "parent_id": "string (parent structon)"
  }
}
```

---

## The Main Loop

```python
def main_loop(root_structon):
    while get_max_tension(root_structon) > THRESHOLD:
        # 1. SENSE
        perception = sense(root_structon)
        
        # 2. SELECT by tension
        target = select_highest_tension(perception)
        
        # 3. ACT
        result = act(target)
        
        # 4. FEEDBACK
        feedback = create_feedback(target, result)
        
        # 5. EVOLVE
        evolved = llm_evolve(target, feedback)
        
        # 6. UPDATE
        update_structon(root_structon, evolved)
        
        # 7. PROPAGATE tension
        propagate_tension(root_structon)
```

---

## Tension System

### Calculation

```python
def calculate_tension(structon):
    importance = structon.importance
    urgency = calculate_urgency(structon)
    unresolved = calculate_unresolved_ratio(structon)
    blocking = calculate_blocking_factor(structon)
    
    tension = (
        importance * 0.3 +
        urgency * 0.3 +
        unresolved * 0.2 +
        blocking * 0.2
    )
    
    return clamp(tension, 0.0, 1.0)
```

### Propagation

```
IMPORTANCE flows DOWN (inheritance):
  Parent important → Children important

TENSION flows UP (aggregation):
  Child tensions → Parent tension

Formula:
  parent.tension = max(child_tensions) * 0.7 + avg(child_tensions) * 0.3
```

---

## Atomic Functions

Minimum set (~25 functions):

### Data Operations
```python
"get"           # Get value from context
"set"           # Set value in context
"merge"         # Combine objects
"filter"        # Filter array
"map"           # Transform array
"first"         # Get first element
"sort"          # Sort array
```

### Control Flow
```python
"if"            # Conditional
"loop"          # Iteration
"branch"        # Multiple paths
```

### Structon Operations
```python
"load_structon"     # Load from storage
"save_structon"     # Save to storage
"query_structons"   # Query by criteria
"create_structon"   # Create new structon
"update_structon"   # Update existing
```

### LLM Operations
```python
"call_llm"          # Call language model
"parse_response"    # Parse LLM output
"validate_json"     # Validate structure
```

### I/O Operations
```python
"emit"              # Output result
"log"               # Log for debugging
"read_input"        # Read external input
```

### Tension Operations
```python
"calculate_tension"     # Calculate tension
"propagate_tension"     # Propagate through tree
"get_highest_tension"   # Find priority
```

---

## Interpreter

```python
class Interpreter:
    def __init__(self):
        self.atomics = load_atomic_functions()
        self.context = {}
    
    def run(self, structon):
        # Execute nodes in order
        for node in topological_sort(structon.nodes, structon.edges):
            result = self.execute_node(node)
            if node.output:
                self.context[node.output] = result
        
        return self.context
    
    def execute_node(self, node):
        if node.type == "sub_structon":
            # Recursive execution
            sub = load_structon(node.structon_ref)
            return self.run(sub)
        else:
            # Atomic execution
            func = self.atomics[node.atomic]
            inputs = self.resolve_inputs(node.input)
            return func(inputs, node.args)
    
    def resolve_inputs(self, input_spec):
        if isinstance(input_spec, str) and input_spec.startswith("$"):
            return self.context[input_spec[1:]]
        elif isinstance(input_spec, list):
            return [self.resolve_inputs(i) for i in input_spec]
        return input_spec
```

---

## LLM Integration

### Generation Prompt

```python
GENERATE_PROMPT = """
You are generating a structon following this blueprint:

{blueprint}

Task: {task}

Requirements:
1. Follow the blueprint schema exactly
2. Include sense, act, and feedback phases
3. Set appropriate tension values
4. Use available atomic functions: {atomics}

Output valid JSON only.
"""
```

### Evolution Prompt

```python
EVOLVE_PROMPT = """
You are evolving a structon based on feedback.

Original Structon:
{structon}

Execution Feedback:
{feedback}

What went wrong (if anything): {error}

Generate an improved structon that:
1. Addresses the feedback
2. Improves on previous version
3. Maintains valid structure

Output valid JSON only.
"""
```

---

## Storage

### File-based (Simple)

```
structons/
├── active/
│   ├── {id}.json
│   └── ...
├── archive/
│   └── {id}_v{version}.json
└── index.json
```

### Database (Production)

```sql
CREATE TABLE structons (
    id UUID PRIMARY KEY,
    type VARCHAR(50),
    intent TEXT,
    tension FLOAT,
    importance FLOAT,
    data JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    version INTEGER,
    parent_id UUID REFERENCES structons(id)
);

CREATE INDEX idx_tension ON structons(tension DESC);
CREATE INDEX idx_type ON structons(type);
```

---

## Pools (Views)

Not separate storage, but views/queries:

```python
def get_sense_structons():
    return query_structons(phases__contains="sense")

def get_act_structons():
    return query_structons(phases__contains="act")

def get_feedback_structons():
    return query_structons(phases__contains="feedback")
```

---

## Self-Similarity

The pattern repeats at every level:

```
SYSTEM LEVEL:
┌─────────────────────────────────────────────────────────────┐
│ Sense: Load all structons, assess tensions                  │
│ Act: Execute pipeline                                       │
│ Feedback: Evolve system based on results                    │
└─────────────────────────────────────────────────────────────┘

STRUCTON LEVEL:
┌─────────────────────────────────────────────────────────────┐
│ Sense: Check state, read inputs                             │
│ Act: Execute nodes                                          │
│ Feedback: Update tension, create feedback structon          │
└─────────────────────────────────────────────────────────────┘

NODE LEVEL:
┌─────────────────────────────────────────────────────────────┐
│ Sense: Read inputs to node                                  │
│ Act: Call atomic function                                   │
│ Feedback: Return result                                     │
└─────────────────────────────────────────────────────────────┘

ATOMIC LEVEL:
┌─────────────────────────────────────────────────────────────┐
│ Sense: Receive arguments                                    │
│ Act: Compute                                                │
│ Feedback: Return value                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Handling

```python
def safe_execute(structon):
    try:
        result = interpreter.run(structon)
        return Success(result)
    except ValidationError as e:
        return Failure("invalid_structon", str(e))
    except AtomicError as e:
        return Failure("atomic_failed", str(e))
    except LLMError as e:
        return Failure("llm_failed", str(e))
    except Exception as e:
        return Failure("unknown", str(e))
```

---

## Configuration

```yaml
# config.yaml
structon:
  tension_threshold: 0.1
  max_iterations: 1000
  
llm:
  provider: "anthropic"  # or "openai"
  model: "claude-3-sonnet"
  max_tokens: 4096
  
storage:
  type: "file"  # or "postgres"
  path: "./structons"
  
logging:
  level: "INFO"
  file: "./logs/structon.log"
```
