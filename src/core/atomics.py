"""
Atomic Functions Module

The ~35 primitive operations that bridge structons to real computation.
These are the ONLY real code in the system. Everything else is data.

Categories:
- Data Operations
- Control Flow
- Structon Operations
- Memory Operations (NEW)
- Meta Operations (NEW)
- LLM Operations
- I/O Operations
- Tension Operations
"""

from typing import Any, Dict, List, Callable, Optional
import json
import os
from datetime import datetime


class AtomicRegistry:
    """Registry of all atomic functions."""
    
    def __init__(self):
        self._functions: Dict[str, Callable] = {}
        self._register_builtins()
    
    def register(self, name: str, func: Callable) -> None:
        """Register an atomic function."""
        self._functions[name] = func
    
    def get(self, name: str) -> Callable:
        """Get an atomic function by name."""
        if name not in self._functions:
            raise ValueError(f"Unknown atomic function: {name}")
        return self._functions[name]
    
    def list_all(self) -> List[str]:
        """List all registered atomic functions."""
        return list(self._functions.keys())
    
    def _register_builtins(self) -> None:
        """Register built-in atomic functions."""
        
        # Data Operations
        self.register("get", atomic_get)
        self.register("set", atomic_set)
        self.register("merge", atomic_merge)
        self.register("filter", atomic_filter)
        self.register("map", atomic_map)
        self.register("first", atomic_first)
        self.register("sort", atomic_sort)
        self.register("diff", atomic_diff)
        
        # Control Flow
        self.register("if", atomic_if)
        self.register("loop", atomic_loop)
        self.register("branch", atomic_branch)
        
        # Structon Operations
        self.register("load_structon", atomic_load_structon)
        self.register("save_structon", atomic_save_structon)
        self.register("query_structons", atomic_query_structons)
        self.register("create_structon", atomic_create_structon)
        self.register("update_structon", atomic_update_structon)
        
        # Memory Operations (NEW)
        self.register("load_memories", atomic_load_memories)
        self.register("sense_memories", atomic_sense_memories)
        self.register("activate_memories", atomic_activate_memories)
        self.register("create_memory", atomic_create_memory)
        self.register("update_memory", atomic_update_memory)
        self.register("learn_from_experience", atomic_learn_from_experience)
        
        # Meta Operations (NEW)
        self.register("run_structon", atomic_run_structon)
        
        # LLM Operations
        self.register("call_llm", atomic_call_llm)
        self.register("parse_response", atomic_parse_response)
        self.register("validate_json", atomic_validate_json)
        
        # I/O Operations
        self.register("emit", atomic_emit)
        self.register("log", atomic_log)
        self.register("read_input", atomic_read_input)
        
        # Tension Operations
        self.register("calculate_tension", atomic_calculate_tension)
        self.register("propagate_tension", atomic_propagate_tension)
        self.register("get_highest_tension", atomic_get_highest_tension)


# =============================================================================
# Data Operations
# =============================================================================

def atomic_get(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Get a value from context or input."""
    key = args.get("key")
    if key:
        return context.get(key, input_data)
    return input_data


def atomic_set(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Set a value in context."""
    key = args.get("key")
    if key:
        context[key] = input_data
    return input_data


def atomic_merge(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Merge multiple objects into one."""
    if isinstance(input_data, list):
        result = {}
        for item in input_data:
            if isinstance(item, dict):
                result.update(item)
        return result
    elif isinstance(input_data, dict):
        return input_data
    return {"value": input_data}


def atomic_filter(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List:
    """Filter a list based on condition."""
    if not isinstance(input_data, list):
        return [input_data] if input_data else []
    
    threshold = args.get("threshold")
    key = args.get("key")
    value = args.get("value")
    
    if threshold is not None and key:
        return [item for item in input_data if item.get(key, 0) >= threshold]
    elif value is not None and key:
        return [item for item in input_data if item.get(key) == value]
    
    return [item for item in input_data if item]


def atomic_map(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List:
    """Apply a function to each item in a list."""
    if not isinstance(input_data, list):
        input_data = [input_data]
    
    func_name = args.get("function")
    key = args.get("key")
    
    if key:
        return [item.get(key) if isinstance(item, dict) else item for item in input_data]
    
    # If function specified, would need to look it up
    return input_data


def atomic_first(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Get the first element of a list."""
    if isinstance(input_data, list) and len(input_data) > 0:
        return input_data[0]
    return input_data


def atomic_sort(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List:
    """Sort a list."""
    if not isinstance(input_data, list):
        return [input_data]
    
    key = args.get("by")
    order = args.get("order", "asc")
    reverse = order == "desc"
    
    if key:
        return sorted(input_data, key=lambda x: x.get(key, 0) if isinstance(x, dict) else x, reverse=reverse)
    return sorted(input_data, reverse=reverse)


def atomic_diff(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Calculate difference between two states."""
    if isinstance(input_data, list) and len(input_data) >= 2:
        old_state, new_state = input_data[0], input_data[1]
    else:
        return {"changes": [], "added": [], "removed": []}
    
    changes = []
    added = []
    removed = []
    
    if isinstance(old_state, dict) and isinstance(new_state, dict):
        for key in new_state:
            if key not in old_state:
                added.append(key)
            elif new_state[key] != old_state[key]:
                changes.append({"key": key, "old": old_state[key], "new": new_state[key]})
        
        for key in old_state:
            if key not in new_state:
                removed.append(key)
    
    return {"changes": changes, "added": added, "removed": removed}


# =============================================================================
# Control Flow
# =============================================================================

def atomic_if(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Conditional execution."""
    condition = args.get("condition", "")
    then_value = args.get("then", True)
    else_value = args.get("else", False)
    
    # Evaluate various condition types
    if condition == "success < 0.5":
        success = input_data.get("success", 1.0) if isinstance(input_data, dict) else 1.0
        return then_value if success < 0.5 else else_value
    elif condition == "result != null":
        return then_value if input_data is not None else else_value
    elif condition == "score >= target":
        score = input_data.get("score", 0) if isinstance(input_data, dict) else 0
        target = args.get("target", 8)
        return then_value if score >= target else else_value
    elif condition == "has_memories":
        return then_value if input_data and len(input_data) > 0 else else_value
    
    # Default: truthy check
    return then_value if input_data else else_value


def atomic_loop(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List:
    """Loop over items."""
    if not isinstance(input_data, list):
        return [input_data]
    
    max_iterations = args.get("max", 100)
    return input_data[:max_iterations]


def atomic_branch(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> str:
    """Choose a branch based on input."""
    branches = args.get("branches", {})
    default = args.get("default", "main")
    
    if isinstance(input_data, str) and input_data in branches:
        return branches[input_data]
    
    return default


# =============================================================================
# Structon Operations
# =============================================================================

STRUCTON_STORAGE_PATH = "./structons"


def atomic_load_structon(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Load a structon from storage."""
    structon_id = args.get("id") or input_data
    storage_path = args.get("storage_path", STRUCTON_STORAGE_PATH)
    
    filepath = os.path.join(storage_path, f"{structon_id}.json")
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    return {"error": f"Structon not found: {structon_id}"}


def atomic_save_structon(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Save a structon to storage."""
    storage_path = args.get("storage_path", STRUCTON_STORAGE_PATH)
    os.makedirs(storage_path, exist_ok=True)
    
    if isinstance(input_data, dict) and "structure_id" in input_data:
        filepath = os.path.join(storage_path, f"{input_data['structure_id']}.json")
        with open(filepath, 'w') as f:
            json.dump(input_data, f, indent=2)
        return {"saved": True, "path": filepath}
    
    return {"saved": False, "error": "Invalid structon data"}


def atomic_query_structons(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List[Dict]:
    """Query structons from storage."""
    storage_path = args.get("storage_path", STRUCTON_STORAGE_PATH)
    results = []
    
    if not os.path.exists(storage_path):
        return results
    
    status = args.get("status")
    structon_type = args.get("type")
    get_all = args.get("all", False)
    limit = args.get("limit", 100)
    
    for filename in os.listdir(storage_path):
        if filename.endswith(".json"):
            filepath = os.path.join(storage_path, filename)
            with open(filepath, 'r') as f:
                structon = json.load(f)
            
            # Apply filters
            if status and structon.get("status") != status:
                continue
            if structon_type and structon.get("structure_type") != structon_type:
                continue
            
            results.append(structon)
            
            if len(results) >= limit:
                break
    
    return results


def atomic_create_structon(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Create a new structon."""
    import uuid
    
    blueprint = args.get("blueprint", "composite")
    intent = args.get("intent") or input_data or "new_structon"
    
    return {
        "structure_id": str(uuid.uuid4()),
        "structure_type": blueprint,
        "intent": intent,
        "phases": ["sense", "act", "feedback"],
        "tension": 0.8,
        "importance": 0.5,
        "nodes": [],
        "edges": []
    }


def atomic_update_structon(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Update an existing structon."""
    target_id = args.get("target")
    updates = args.get("updates", {})
    
    if isinstance(input_data, dict):
        input_data.update(updates)
        return input_data
    
    return {"error": "Invalid input for update"}


# =============================================================================
# Memory Operations (NEW - for code-is-data)
# =============================================================================

MEMORY_DIR = "./memory"


def atomic_load_memories(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List[Dict]:
    """Load all memories from disk."""
    memory_dir = args.get("memory_dir", MEMORY_DIR)
    os.makedirs(memory_dir, exist_ok=True)
    
    memories = []
    for filename in os.listdir(memory_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(memory_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    memories.append(json.load(f))
            except Exception as e:
                print(f"[Memory] Failed to load {filename}: {e}")
    
    return memories


def atomic_sense_memories(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List[Dict]:
    """
    Calculate relevance of memories to context.
    
    This is the SENSE phase for memories.
    """
    memories = args.get("memories", [])
    if not memories and isinstance(input_data, list):
        memories = input_data
        ctx = args.get("context", "")
    else:
        ctx = str(input_data)
    
    if not memories:
        return []
    
    # First try pattern matching (fast path)
    for memory in memories:
        memory["activation"] = 0.0
        patterns = memory.get("sense_patterns", [])
        ctx_lower = ctx.lower()
        
        for pattern in patterns:
            if pattern.lower() in ctx_lower:
                memory["activation"] = memory.get("tension", 0.5) * 0.9
                break
    
    # For memories without pattern match, use LLM
    unmatched = [m for m in memories if m.get("activation", 0) == 0]
    
    if unmatched:
        memory_intents = {str(i): m.get("intent", "") for i, m in enumerate(unmatched)}
        
        prompt = f"""Rate each memory's relevance (0.0-1.0) to this context.
Return JSON only: {{"0": 0.5, "1": 0.8, ...}}

Context: {ctx}

Memories:
{json.dumps(memory_intents, indent=2)}"""
        
        response = atomic_call_llm(prompt, {"prompt": "{input}"}, context)
        
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            relevances = json.loads(response[start:end])
            
            for i, memory in enumerate(unmatched):
                relevance = float(relevances.get(str(i), 0.1))
                relevance = max(0.0, min(1.0, relevance))
                memory["activation"] = memory.get("tension", 0.5) * relevance
        except:
            for memory in unmatched:
                memory["activation"] = memory.get("tension", 0.5) * 0.1
    
    return memories


def atomic_activate_memories(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List[Dict]:
    """
    Get top-k activated memories.
    
    This is the ACT phase for memories.
    """
    memories = input_data if isinstance(input_data, list) else []
    top_k = args.get("top_k", 3)
    threshold = args.get("threshold", 0.0)
    
    # Filter and sort by activation
    qualified = [m for m in memories if m.get("activation", 0) > threshold]
    sorted_memories = sorted(qualified, key=lambda m: m.get("activation", 0), reverse=True)
    
    # Activate top-k
    activated = sorted_memories[:top_k]
    for memory in activated:
        memory["times_used"] = memory.get("times_used", 0) + 1
        memory["last_activated"] = datetime.now().isoformat()
    
    return activated


def atomic_create_memory(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """
    Create a new memory.
    
    This is part of the FEEDBACK phase.
    """
    memory_dir = args.get("memory_dir", MEMORY_DIR)
    
    memory = {
        "id": f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "intent": args.get("intent", str(input_data)[:50] if input_data else "new_memory"),
        "content": args.get("content", {"data": input_data}),
        "sense_patterns": args.get("patterns", []),
        "tension": args.get("tension", 0.8),
        "success_rate": 0.5,
        "times_used": 0,
        "created_at": datetime.now().isoformat(),
        "last_activated": None
    }
    
    # Save to disk
    os.makedirs(memory_dir, exist_ok=True)
    filepath = os.path.join(memory_dir, f"{memory['id']}.json")
    with open(filepath, 'w') as f:
        json.dump(memory, f, indent=2)
    
    return memory


def atomic_update_memory(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """
    Update memory based on feedback.
    
    This is the FEEDBACK phase for memories.
    """
    memory = input_data if isinstance(input_data, dict) else {}
    success = args.get("success", True)
    memory_dir = args.get("memory_dir", MEMORY_DIR)
    
    if not memory.get("id"):
        return memory
    
    # Update stats based on feedback
    if success:
        memory["tension"] = max(0.05, memory.get("tension", 0.5) * 0.9)
        memory["success_rate"] = memory.get("success_rate", 0.5) * 0.8 + 0.2
    else:
        memory["tension"] = min(1.0, memory.get("tension", 0.5) * 1.15)
        memory["success_rate"] = memory.get("success_rate", 0.5) * 0.8
    
    # Save updated memory
    filepath = os.path.join(memory_dir, f"{memory['id']}.json")
    with open(filepath, 'w') as f:
        json.dump(memory, f, indent=2)
    
    return memory


def atomic_learn_from_experience(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Optional[Dict]:
    """
    Extract and save learning from experience.
    
    This is the meta-FEEDBACK: learning new knowledge from tasks.
    """
    task = args.get("task", "")
    result = args.get("result", str(input_data))
    success = args.get("success", True)
    memory_dir = args.get("memory_dir", MEMORY_DIR)
    
    success_str = "succeeded" if success else "failed"
    
    prompt = f"""You completed a task. Extract a reusable lesson for future similar tasks.

TASK: {task}
RESULT: {result}
OUTCOME: {success_str}

Think about:
- What approach was used?
- What made it work (or fail)?
- When would this lesson apply again?

Return a JSON object with these exact fields:
{{
  "intent": "A brief description of what this lesson is about",
  "lesson": "The key insight to remember",
  "patterns": ["trigger", "words", "for", "this", "memory"]
}}

Return ONLY the JSON object, no other text."""

    response = atomic_call_llm(prompt, {"prompt": "{input}"}, context)
    
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        
        if start == -1 or end == 0:
            return None
        
        learning = json.loads(response[start:end])
        
        # Validate and create memory
        intent = learning.get("intent", "").strip()
        lesson = learning.get("lesson", "").strip()
        patterns = learning.get("patterns", [])
        
        if not intent:
            intent = f"Lesson from: {task[:50]}"
        
        if not lesson:
            lesson = f"Task {success_str}: {result[:100]}"
        
        if isinstance(patterns, str):
            patterns = [p.strip() for p in patterns.split(",")]
        
        memory = atomic_create_memory(None, {
            "intent": intent,
            "content": {
                "lesson": lesson,
                "source_task": task,
                "source_result": result[:200],
                "was_successful": success
            },
            "patterns": patterns,
            "memory_dir": memory_dir
        }, context)
        
        return memory
        
    except Exception as e:
        print(f"[Memory] Learning failed: {e}")
        return None


# =============================================================================
# Meta Operations (NEW - structons running structons)
# =============================================================================

# Reference to interpreter - will be set by interpreter module
_interpreter = None


def set_interpreter(interpreter):
    """Set the interpreter reference for meta operations."""
    global _interpreter
    _interpreter = interpreter


def atomic_run_structon(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """
    Run another structon from within a structon.
    
    This enables:
    - Composition: Structons calling structons
    - Recursion: Structons calling themselves
    - Meta-cognition: Structons about structons
    
    TRUE CODE-IS-DATA: A structon can load and run any other structon.
    """
    global _interpreter
    
    structon_id = args.get("structon_id")
    structon_data = args.get("structon")  # Can pass structon directly
    storage_path = args.get("storage_path", STRUCTON_STORAGE_PATH)
    
    # Get the structon to run
    if structon_data:
        structon = structon_data
    elif structon_id:
        structon = atomic_load_structon(None, {"id": structon_id, "storage_path": storage_path}, context)
        if "error" in structon:
            return {"error": f"Could not load structon: {structon_id}"}
    else:
        return {"error": "No structon specified"}
    
    # Prepare input for child structon
    child_context = dict(context)  # Copy parent context
    if input_data:
        child_context["input"] = input_data
    
    # Run the structon
    if _interpreter:
        # Use the real interpreter
        from .schema import Structon
        if isinstance(structon, dict):
            structon_obj = Structon.from_dict(structon)
        else:
            structon_obj = structon
        return _interpreter.run(structon_obj, child_context)
    else:
        # Fallback: return the structon data
        return {"warning": "No interpreter set", "structon": structon}


# =============================================================================
# LLM Operations
# =============================================================================

# LLM Provider classes
class OpenAILLM:
    """OpenAI LLM provider."""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o")
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        return self._client
    
    def generate(self, prompt: str) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096
        )
        return response.choices[0].message.content


class AnthropicLLM:
    """Anthropic LLM provider."""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from anthropic import Anthropic
                self._client = Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
        return self._client
    
    def generate(self, prompt: str) -> str:
        client = self._get_client()
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


# Global LLM provider
LLM_PROVIDER = None


def _init_llm_provider():
    """Initialize LLM provider based on environment."""
    global LLM_PROVIDER
    
    if LLM_PROVIDER is not None:
        return
    
    if os.environ.get("OPENAI_API_KEY"):
        LLM_PROVIDER = OpenAILLM()
        print("[LLM] Using OpenAI provider")
    elif os.environ.get("ANTHROPIC_API_KEY"):
        LLM_PROVIDER = AnthropicLLM()
        print("[LLM] Using Anthropic provider")


def atomic_call_llm(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> str:
    """Call the language model."""
    global LLM_PROVIDER
    
    # Initialize provider if needed
    _init_llm_provider()
    
    prompt_template = args.get("prompt", "{input}")
    
    # Format prompt with input
    if isinstance(input_data, str):
        prompt = prompt_template.replace("{input}", input_data)
    elif isinstance(input_data, dict):
        prompt = prompt_template
        for key, value in input_data.items():
            prompt = prompt.replace(f"{{${key}}}", str(value))
            prompt = prompt.replace(f"{{{key}}}", str(value))
        prompt = prompt.replace("{input}", json.dumps(input_data))
    else:
        prompt = prompt_template.replace("{input}", str(input_data))
    
    # Call LLM
    if LLM_PROVIDER:
        return LLM_PROVIDER.generate(prompt)
    
    # Placeholder response
    return f"[LLM Response to: {prompt[:100]}...]"


def atomic_parse_response(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Parse LLM response into structured data."""
    format_type = args.get("format", "text")
    
    if format_type == "json":
        try:
            if isinstance(input_data, str):
                # Try to extract JSON from response
                start = input_data.find("{")
                end = input_data.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(input_data[start:end])
            return input_data
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": input_data}
    
    return input_data


def atomic_validate_json(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Validate JSON structure."""
    schema = args.get("schema", {})
    
    if isinstance(input_data, dict):
        # Basic validation
        required = schema.get("required", [])
        missing = [r for r in required if r not in input_data]
        
        return {
            "valid": len(missing) == 0,
            "data": input_data,
            "missing": missing
        }
    
    return {"valid": False, "error": "Not a valid object"}


# =============================================================================
# I/O Operations
# =============================================================================

def atomic_emit(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Emit/output a value."""
    return input_data


def atomic_log(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Log for debugging."""
    level = args.get("level", "INFO")
    message = args.get("message", "")
    
    print(f"[{level}] {message}: {input_data}")
    
    return input_data


def atomic_read_input(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Read external input."""
    source = args.get("source", "stdin")
    
    if source == "stdin":
        return input("Input: ")
    elif source == "context":
        key = args.get("key")
        return context.get(key)
    
    return input_data


# =============================================================================
# Tension Operations
# =============================================================================

def atomic_calculate_tension(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> float:
    """Calculate tension for a structon."""
    if isinstance(input_data, dict):
        importance = input_data.get("importance", 0.5)
        urgency = input_data.get("urgency", 0.5)
        unresolved = input_data.get("unresolved", 0.5)
        blocking = input_data.get("blocking", 0.0)
        
        tension = (
            importance * 0.3 +
            urgency * 0.3 +
            unresolved * 0.2 +
            blocking * 0.2
        )
        
        return max(0.0, min(1.0, tension))
    
    return 0.5


def atomic_propagate_tension(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Propagate tension through structon tree."""
    if isinstance(input_data, list):
        if len(input_data) == 0:
            return {"tension": 0.5}
        
        tensions = [item.get("tension", 0.5) if isinstance(item, dict) else 0.5 for item in input_data]
        
        max_tension = max(tensions)
        avg_tension = sum(tensions) / len(tensions)
        
        # Hybrid: weighted toward max but considers average
        propagated = max_tension * 0.7 + avg_tension * 0.3
        
        return {"tension": propagated, "max": max_tension, "avg": avg_tension}
    
    return {"tension": input_data.get("tension", 0.5) if isinstance(input_data, dict) else 0.5}


def atomic_get_highest_tension(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Get the item with highest tension."""
    if not isinstance(input_data, list):
        return input_data
    
    if len(input_data) == 0:
        return None
    
    return max(input_data, key=lambda x: x.get("tension", 0) if isinstance(x, dict) else 0)


# =============================================================================
# Global Registry Instance
# =============================================================================

registry = AtomicRegistry()


def get_atomic(name: str) -> Callable:
    """Get an atomic function by name."""
    return registry.get(name)


def list_atomics() -> List[str]:
    """List all available atomic functions."""
    return registry.list_all()