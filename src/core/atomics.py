"""
Atomic Functions Module

The ~25 primitive operations that bridge structons to real computation.
These are the ONLY real code in the system. Everything else is data.
"""

from typing import Any, Dict, List, Callable, Optional
import json
import os


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
    
    # Simple condition evaluation
    if condition == "success < 0.5":
        success = input_data.get("success", 1.0) if isinstance(input_data, dict) else 1.0
        return then_value if success < 0.5 else else_value
    elif condition == "result != null":
        return then_value if input_data is not None else else_value
    
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
    
    filepath = os.path.join(STRUCTON_STORAGE_PATH, f"{structon_id}.json")
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    return {"error": f"Structon not found: {structon_id}"}


def atomic_save_structon(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> Dict:
    """Save a structon to storage."""
    os.makedirs(STRUCTON_STORAGE_PATH, exist_ok=True)
    
    if isinstance(input_data, dict) and "structure_id" in input_data:
        filepath = os.path.join(STRUCTON_STORAGE_PATH, f"{input_data['structure_id']}.json")
        with open(filepath, 'w') as f:
            json.dump(input_data, f, indent=2)
        return {"saved": True, "path": filepath}
    
    return {"saved": False, "error": "Invalid structon data"}


def atomic_query_structons(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> List[Dict]:
    """Query structons from storage."""
    results = []
    
    if not os.path.exists(STRUCTON_STORAGE_PATH):
        return results
    
    status = args.get("status")
    structon_type = args.get("type")
    get_all = args.get("all", False)
    limit = args.get("limit", 100)
    
    for filename in os.listdir(STRUCTON_STORAGE_PATH):
        if filename.endswith(".json"):
            filepath = os.path.join(STRUCTON_STORAGE_PATH, filename)
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
# LLM Operations
# =============================================================================

# LLM Provider - initialized on first use
_LLM_PROVIDER = None
_LLM_PROVIDER_INITIALIZED = False


def _get_llm_provider():
    """Get or create LLM provider based on environment."""
    global _LLM_PROVIDER, _LLM_PROVIDER_INITIALIZED
    
    if _LLM_PROVIDER_INITIALIZED:
        return _LLM_PROVIDER
    
    _LLM_PROVIDER_INITIALIZED = True
    
    # Try OpenAI first
    if os.environ.get("OPENAI_API_KEY"):
        try:
            import openai
            _LLM_PROVIDER = OpenAILLM()
            print("[LLM] Using OpenAI provider")
            return _LLM_PROVIDER
        except ImportError:
            print("[LLM] OpenAI key found but 'openai' package not installed")
    
    # Try Anthropic
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            import anthropic
            _LLM_PROVIDER = AnthropicLLM()
            print("[LLM] Using Anthropic provider")
            return _LLM_PROVIDER
        except ImportError:
            print("[LLM] Anthropic key found but 'anthropic' package not installed")
    
    print("[LLM] No API key found. Using mock provider.")
    return None


class OpenAILLM:
    """OpenAI LLM wrapper."""
    
    def __init__(self, model: str = None):
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o")
        self.api_key = os.environ.get("OPENAI_API_KEY")
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"[OpenAI Error: {str(e)}]"


class AnthropicLLM:
    """Anthropic LLM wrapper."""
    
    def __init__(self, model: str = None):
        self.model = model or os.environ.get("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        except Exception as e:
            return f"[Anthropic Error: {str(e)}]"


def atomic_call_llm(input_data: Any, args: Dict[str, Any], context: Dict[str, Any]) -> str:
    """Call the language model."""
    provider = _get_llm_provider()
    
    prompt_template = args.get("prompt", "{input}")
    
    # Format prompt with input
    if isinstance(input_data, str):
        prompt = prompt_template.replace("{input}", input_data)
    elif isinstance(input_data, dict):
        prompt = prompt_template
        for key, value in input_data.items():
            prompt = prompt.replace(f"{{${key}}}", str(value))
            prompt = prompt.replace(f"{{{key}}}", str(value))
    elif input_data is None:
        prompt = prompt_template.replace("{input}", "")
    else:
        prompt = prompt_template.replace("{input}", str(input_data))
    
    # Clean up any remaining template variables
    prompt = prompt.replace("{input}", "").replace("{$input}", "")
    
    # If LLM provider is configured, use it
    if provider:
        return provider.generate(prompt)
    
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