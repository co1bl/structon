"""
Structon Factory

Helpers for creating valid structons from blueprints or LLM generation.
This ensures all structons have required fields and proper structure.
"""

import os
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime


# Default paths
BLUEPRINT_DIR = "./blueprints"
STRUCTON_DIR = "./structons"


# =============================================================================
# Default Values
# =============================================================================

DEFAULT_NODE = {
    "id": "node_1",
    "type": "process",
    "phase": "act",
    "description": "Default node",
    "atomic": "emit",
    "args": {},
    "input": None,
    "output": "$output"
}

DEFAULT_STRUCTON = {
    "structure_id": None,  # Will be generated
    "structure_type": "composite",
    "intent": "Default structon",
    "description": "A structon created from factory",
    "phases": ["sense", "act", "feedback"],
    "tension": 0.5,
    "importance": 0.5,
    "nodes": [],
    "edges": []
}


# =============================================================================
# Validation
# =============================================================================

REQUIRED_STRUCTON_FIELDS = [
    "structure_id", "structure_type", "intent", "phases", 
    "tension", "importance", "nodes", "edges"
]

REQUIRED_NODE_FIELDS = [
    "id", "type", "phase", "description", "atomic"
]

VALID_PHASES = ["sense", "act", "feedback"]
VALID_NODE_TYPES = ["input", "process", "output"]
VALID_STRUCTURE_TYPES = ["sense", "act", "feedback", "composite", "blueprint"]


def validate_structon(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate structon data and return validation result.
    
    Returns:
        {"valid": True/False, "errors": [...], "warnings": [...]}
    """
    errors = []
    warnings = []
    
    # Check required fields
    for field in REQUIRED_STRUCTON_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate structure_type
    if data.get("structure_type") not in VALID_STRUCTURE_TYPES:
        errors.append(f"Invalid structure_type: {data.get('structure_type')}")
    
    # Validate phases
    phases = data.get("phases", [])
    for phase in phases:
        if phase not in VALID_PHASES:
            errors.append(f"Invalid phase: {phase}")
    
    # Validate tension and importance
    tension = data.get("tension", 0)
    importance = data.get("importance", 0)
    if not (0 <= tension <= 1):
        warnings.append(f"Tension {tension} outside 0-1 range")
    if not (0 <= importance <= 1):
        warnings.append(f"Importance {importance} outside 0-1 range")
    
    # Validate nodes
    nodes = data.get("nodes", [])
    node_ids = set()
    for i, node in enumerate(nodes):
        for field in REQUIRED_NODE_FIELDS:
            if field not in node:
                errors.append(f"Node {i} missing field: {field}")
        
        node_id = node.get("id")
        if node_id in node_ids:
            errors.append(f"Duplicate node id: {node_id}")
        node_ids.add(node_id)
        
        if node.get("type") not in VALID_NODE_TYPES:
            warnings.append(f"Node {node_id} has unusual type: {node.get('type')}")
        
        if node.get("phase") not in VALID_PHASES:
            errors.append(f"Node {node_id} has invalid phase: {node.get('phase')}")
    
    # Validate edges reference valid nodes
    edges = data.get("edges", [])
    for edge in edges:
        if edge.get("from") not in node_ids:
            errors.append(f"Edge references unknown node: {edge.get('from')}")
        if edge.get("to") not in node_ids:
            errors.append(f"Edge references unknown node: {edge.get('to')}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def is_valid_structon(data: Dict[str, Any]) -> bool:
    """Quick check if structon is valid."""
    return validate_structon(data)["valid"]


# =============================================================================
# Blueprint Loading
# =============================================================================

def load_blueprint(name: str, blueprint_dir: str = None) -> Dict[str, Any]:
    """
    Load a blueprint template by name.
    
    Args:
        name: Blueprint name (without .json extension)
        blueprint_dir: Directory containing blueprints
        
    Returns:
        Blueprint data as dict
    """
    directory = blueprint_dir or BLUEPRINT_DIR
    
    # Try different filename patterns
    patterns = [
        f"{name}.json",
        f"{name}_blueprint.json",
        f"blueprint_{name}.json"
    ]
    
    for pattern in patterns:
        filepath = os.path.join(directory, pattern)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    
    raise FileNotFoundError(f"Blueprint not found: {name} in {directory}")


def list_blueprints(blueprint_dir: str = None) -> List[str]:
    """List all available blueprints."""
    directory = blueprint_dir or BLUEPRINT_DIR
    
    if not os.path.exists(directory):
        return []
    
    blueprints = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            name = filename.replace('.json', '').replace('_blueprint', '').replace('blueprint_', '')
            blueprints.append(name)
    
    return blueprints


# =============================================================================
# Structon Creation
# =============================================================================

def generate_id() -> str:
    """Generate unique structon ID."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    short_uuid = str(uuid.uuid4())[:8]
    return f"structon_{timestamp}_{short_uuid}"


def create_node(
    node_id: str,
    atomic: str,
    phase: str = "act",
    node_type: str = "process",
    description: str = None,
    input_var: str = None,
    args: Dict = None,
    output_var: str = None
) -> Dict[str, Any]:
    """
    Create a valid node with all required fields.
    
    Args:
        node_id: Unique node identifier
        atomic: Atomic function name
        phase: sense, act, or feedback
        node_type: input, process, or output
        description: Human-readable description
        input_var: Input variable (e.g., "$topic")
        args: Arguments for atomic function
        output_var: Output variable (e.g., "$result")
    """
    return {
        "id": node_id,
        "type": node_type,
        "phase": phase,
        "description": description or f"{atomic} node",
        "atomic": atomic,
        "input": input_var,
        "args": args or {},
        "output": output_var or f"${node_id}_output"
    }


def create_structon(
    intent: str,
    nodes: List[Dict] = None,
    edges: List[Dict] = None,
    structure_id: str = None,
    structure_type: str = "composite",
    description: str = None,
    tension: float = 0.5,
    importance: float = 0.5,
    phases: List[str] = None
) -> Dict[str, Any]:
    """
    Create a valid structon with all required fields.
    
    Args:
        intent: What this structon does
        nodes: List of nodes (use create_node helper)
        edges: List of edges {"from": "s1", "to": "a1"}
        structure_id: Unique ID (auto-generated if None)
        structure_type: composite, sense, act, feedback, blueprint
        description: Human-readable description
        tension: Initial tension 0-1
        importance: Importance 0-1
        phases: List of phases (default: all three)
    """
    return {
        "structure_id": structure_id or generate_id(),
        "structure_type": structure_type,
        "intent": intent,
        "description": description or intent,
        "phases": phases or ["sense", "act", "feedback"],
        "tension": tension,
        "importance": importance,
        "nodes": nodes or [],
        "edges": edges or []
    }


def create_from_blueprint(
    blueprint_name: str,
    intent: str = None,
    structure_id: str = None,
    customizations: Dict[str, Any] = None,
    blueprint_dir: str = None
) -> Dict[str, Any]:
    """
    Create a structon from a blueprint template.
    
    Args:
        blueprint_name: Name of blueprint to use
        intent: Override intent (optional)
        structure_id: Override ID (optional, auto-generated if None)
        customizations: Dict of field overrides
        blueprint_dir: Directory containing blueprints
        
    Returns:
        New structon based on blueprint
    """
    # Load blueprint
    blueprint = load_blueprint(blueprint_name, blueprint_dir)
    
    # Create new structon from blueprint
    structon = json.loads(json.dumps(blueprint))  # Deep copy
    
    # Set unique ID
    structon["structure_id"] = structure_id or generate_id()
    
    # Override intent if provided
    if intent:
        structon["intent"] = intent
        structon["description"] = intent
    
    # Track input_key for syncing
    input_key = customizations.get("input_key", "input") if customizations else "input"
    
    # Apply customizations
    if customizations:
        for key, value in customizations.items():
            if key == "nodes":
                # Merge node customizations
                for node_update in value:
                    node_id = node_update.get("id")
                    for node in structon["nodes"]:
                        if node["id"] == node_id:
                            node.update(node_update)
            elif key == "input_key" and "nodes" in structon:
                # Update get node's key AND output variable
                for node in structon["nodes"]:
                    if node.get("atomic") == "get":
                        node["args"]["key"] = value
                        node["output"] = f"${value}"
                        break
            elif key == "prompt" and "nodes" in structon:
                # Update first call_llm node's prompt
                for node in structon["nodes"]:
                    if node.get("atomic") == "call_llm":
                        node["args"]["prompt"] = value
                        break
            elif key not in ("input_key", "prompt", "learn"):
                structon[key] = value
    
    # CRITICAL: Sync all variable names and prompt placeholders
    structon = _sync_variables(structon, input_key)
    
    return structon


def _sync_variables(structon: Dict[str, Any], input_key: str) -> Dict[str, Any]:
    """
    Ensure all variable names are consistent throughout the structon.
    
    This fixes the mismatch where:
    - get node outputs $text
    - call_llm expects $input
    - prompt uses {input} but should use {text}
    """
    nodes = structon.get("nodes", [])
    
    # Find the get node's output variable
    get_output_var = None
    for node in nodes:
        if node.get("atomic") == "get":
            # Ensure get node uses input_key
            node["args"]["key"] = input_key
            node["output"] = f"${input_key}"
            get_output_var = f"${input_key}"
            break
    
    if not get_output_var:
        return structon
    
    # Update all downstream nodes that use this variable
    for node in nodes:
        # Update call_llm nodes
        if node.get("atomic") == "call_llm":
            # Set input to match get node's output
            node["input"] = get_output_var
            
            # Fix prompt placeholder to match variable name
            if "args" in node and "prompt" in node["args"]:
                prompt = node["args"]["prompt"]
                # Replace {input} with {actual_variable_name}
                # Handle common placeholders
                for placeholder in ["{input}", "{text}", "{task}", "{query}", "{content}"]:
                    if placeholder in prompt:
                        prompt = prompt.replace(placeholder, f"{{{input_key}}}")
                node["args"]["prompt"] = prompt
    
    return structon


# =============================================================================
# LLM Generation (Template-Based)
# =============================================================================

def generate_customization_prompt(intent: str, blueprint: Dict[str, Any]) -> str:
    """
    Generate prompt for LLM to customize a blueprint.
    
    LLM only decides WHAT (prompt, input_key, etc.)
    Template provides HOW (structure, required fields)
    """
    return f"""I need to create an AI agent for this intent: "{intent}"

I have a template with these customizable parts:
1. prompt: The instruction for the LLM (use {{input}} as placeholder for input data)
2. input_key: What to call the input variable (e.g., "text", "topic", "query")
3. learn: Whether the agent should learn from experience (true/false)
4. parallel_tasks: Optional list of additional LLM calls to run in parallel

Based on the intent "{intent}", provide customizations as JSON:

{{
  "prompt": "The LLM prompt to accomplish the intent. Use {{input}} for the input.",
  "input_key": "descriptive_name_for_input",
  "learn": true or false,
  "parallel_tasks": [
    {{"name": "task_name", "prompt": "additional prompt if needed"}}
  ] or []
}}

RULES:
- prompt must clearly instruct the LLM what to do
- input_key should describe what kind of input (e.g., "text", "code", "question")
- learn=true if the task benefits from remembering past experiences
- parallel_tasks only if the intent requires multiple distinct outputs

Return ONLY valid JSON, no explanation."""


def generate_structon_via_llm(
    intent: str,
    blueprint_name: str = "agent",
    llm_func = None,
    blueprint_dir: str = None
) -> Dict[str, Any]:
    """
    Use LLM to customize a blueprint template.
    
    This is SAFE because:
    - Blueprint provides valid structure (all required fields)
    - LLM only customizes content (prompt, input_key, etc.)
    - Result is always valid
    
    Args:
        intent: What the structon should do
        blueprint_name: Which blueprint to use as template
        llm_func: Function to call LLM (default: uses atomic_call_llm)
        blueprint_dir: Directory containing blueprints
        
    Returns:
        Valid structon dict (guaranteed)
    """
    from .atomics import atomic_call_llm
    
    # 1. Load blueprint template
    try:
        blueprint = load_blueprint(blueprint_name, blueprint_dir)
    except FileNotFoundError:
        # Fallback to quick builder if no blueprint
        print(f"[Factory] Blueprint '{blueprint_name}' not found, using quick builder")
        return _generate_without_blueprint(intent, llm_func)
    
    # 2. Ask LLM for customizations only
    prompt = generate_customization_prompt(intent, blueprint)
    
    if llm_func:
        response = llm_func(prompt)
    else:
        response = atomic_call_llm(prompt, {"prompt": "{input}"}, {})
    
    # 3. Parse customizations
    customizations = _parse_customizations(response)
    
    # 4. Apply customizations to blueprint
    structon = create_from_blueprint(
        blueprint_name=blueprint_name,
        intent=intent,
        customizations=customizations,
        blueprint_dir=blueprint_dir
    )
    
    # 5. Handle parallel tasks if requested
    if customizations.get("parallel_tasks"):
        structon = _add_parallel_tasks(structon, customizations["parallel_tasks"])
    
    return structon


def _parse_customizations(response: str) -> Dict[str, Any]:
    """Parse LLM response into customizations dict."""
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(response[start:end])
            return {
                "prompt": data.get("prompt", "Process this: {input}"),
                "input_key": data.get("input_key", "input"),
                "learn": data.get("learn", False),
                "parallel_tasks": data.get("parallel_tasks", [])
            }
    except json.JSONDecodeError:
        pass
    
    # Default if parsing fails
    return {
        "prompt": "Process this: {input}",
        "input_key": "input",
        "learn": False,
        "parallel_tasks": []
    }


def _add_parallel_tasks(structon: Dict[str, Any], tasks: List[Dict]) -> Dict[str, Any]:
    """Add parallel LLM tasks to structon."""
    if not tasks:
        return structon
    
    nodes = structon["nodes"]
    edges = structon["edges"]
    
    # Find the input node (s1) and output node
    input_node_id = "s1"
    output_node_id = None
    for node in nodes:
        if node.get("atomic") == "emit":
            output_node_id = node["id"]
            break
    
    # Add parallel task nodes
    for i, task in enumerate(tasks):
        task_id = f"a_parallel_{i+1}"
        task_node = create_node(
            node_id=task_id,
            atomic="call_llm",
            phase="act",
            node_type="process",
            description=task.get("name", f"Parallel task {i+1}"),
            input_var="$input",
            args={"prompt": task.get("prompt", "Process: {input}")},
            output_var=f"$parallel_result_{i+1}"
        )
        nodes.append(task_node)
        
        # Connect from input
        edges.append({"from": input_node_id, "to": task_id})
        
        # Connect to output
        if output_node_id:
            edges.append({"from": task_id, "to": output_node_id})
    
    structon["nodes"] = nodes
    structon["edges"] = edges
    
    return structon


def _generate_without_blueprint(intent: str, llm_func = None) -> Dict[str, Any]:
    """Fallback: generate using quick builder when no blueprint available."""
    from .atomics import atomic_call_llm
    
    # Ask LLM just for the prompt
    prompt = f"""For this intent: "{intent}"
    
What LLM prompt would accomplish this? Use {{input}} as placeholder.
Return ONLY the prompt text, nothing else."""
    
    if llm_func:
        response = llm_func(prompt)
    else:
        response = atomic_call_llm(prompt, {"prompt": "{input}"}, {})
    
    # Clean up response
    llm_prompt = response.strip().strip('"').strip("'")
    if not "{input}" in llm_prompt:
        llm_prompt = llm_prompt + "\n\nInput: {input}"
    
    return quick_llm_structon(intent, llm_prompt, learn=True)


# =============================================================================
# Saving
# =============================================================================

def save_structon(
    structon: Dict[str, Any],
    filename: str = None,
    structon_dir: str = None,
    validate: bool = True
) -> str:
    """
    Save structon to file.
    
    Args:
        structon: Structon data
        filename: Filename (default: structure_id.json)
        structon_dir: Directory to save in
        validate: Whether to validate before saving
        
    Returns:
        Filepath where saved
    """
    directory = structon_dir or STRUCTON_DIR
    os.makedirs(directory, exist_ok=True)
    
    # Validate
    if validate:
        validation = validate_structon(structon)
        if not validation["valid"]:
            raise ValueError(f"Invalid structon: {validation['errors']}")
    
    # Generate filename
    if not filename:
        filename = f"{structon['structure_id']}.json"
    if not filename.endswith('.json'):
        filename += '.json'
    
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as f:
        json.dump(structon, f, indent=2)
    
    return filepath


# =============================================================================
# Quick Builders
# =============================================================================

def quick_llm_structon(
    intent: str,
    prompt: str,
    input_key: str = "input",
    learn: bool = False
) -> Dict[str, Any]:
    """
    Quickly create a simple LLM-based structon.
    
    Args:
        intent: What it does
        prompt: LLM prompt (use {input_key} for variable, e.g., {text})
        input_key: Context key to get input from
        learn: Whether to add learning node
    """
    # Ensure prompt uses the correct placeholder
    # Replace common placeholders with the actual input_key
    for placeholder in ["{input}", "{text}", "{task}", "{query}", "{content}"]:
        if placeholder in prompt and placeholder != f"{{{input_key}}}":
            prompt = prompt.replace(placeholder, f"{{{input_key}}}")
    
    # If no placeholder found, add one
    if f"{{{input_key}}}" not in prompt:
        prompt = prompt + f"\n\nInput: {{{input_key}}}"
    
    # Use consistent variable naming: $input_key throughout
    var_name = f"${input_key}"
    
    nodes = [
        create_node("s1", "get", "sense", "input", "Get input", args={"key": input_key}, output_var=var_name),
        create_node("a1", "call_llm", "act", "process", "Process with LLM", var_name, {"prompt": prompt}, "$result"),
    ]
    
    edges = [
        {"from": "s1", "to": "a1"}
    ]
    
    if learn:
        nodes.append(create_node("f1", "learn_from_experience", "feedback", "process", "Learn", "$result", {"task": intent, "success": True}, "$memory"))
        nodes.append(create_node("f2", "emit", "feedback", "output", "Return result", "$result", {}, "$output"))
        edges.extend([
            {"from": "a1", "to": "f1"},
            {"from": "a1", "to": "f2"}
        ])
    else:
        nodes.append(create_node("f1", "emit", "feedback", "output", "Return result", "$result", {}, "$output"))
        edges.append({"from": "a1", "to": "f1"})
    
    return create_structon(intent, nodes, edges)


def quick_memory_structon(
    intent: str = "Sense relevant memories",
    top_k: int = 3
) -> Dict[str, Any]:
    """Quickly create a memory sensing structon."""
    nodes = [
        create_node("s1", "get", "sense", "input", "Get context", args={"key": "context"}, output_var="$context"),
        create_node("s2", "load_memories", "sense", "process", "Load memories", args={}, output_var="$memories"),
        create_node("a1", "sense_memories", "act", "process", "Sense relevance", "$context", {"memories": "$memories"}, "$sensed"),
        create_node("a2", "activate_memories", "act", "process", "Activate top memories", "$sensed", {"top_k": top_k}, "$active"),
        create_node("f1", "emit", "feedback", "output", "Return memories", "$active", {}, "$output")
    ]
    
    edges = [
        {"from": "s1", "to": "a1"},
        {"from": "s2", "to": "a1"},
        {"from": "a1", "to": "a2"},
        {"from": "a2", "to": "f1"}
    ]
    
    return create_structon(intent, nodes, edges)