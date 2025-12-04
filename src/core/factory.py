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
            elif key == "prompt" and "nodes" in structon:
                # Shortcut: update first call_llm node's prompt
                for node in structon["nodes"]:
                    if node.get("atomic") == "call_llm":
                        node["args"]["prompt"] = value
                        break
            else:
                structon[key] = value
    
    return structon


# =============================================================================
# LLM Generation
# =============================================================================

def generate_structon_prompt(intent: str, available_atomics: List[str] = None) -> str:
    """Generate prompt for LLM to create a structon."""
    
    atomics = available_atomics or [
        "get", "set", "emit", "call_llm", "parse_response",
        "load_memories", "sense_memories", "activate_memories",
        "create_memory", "update_memory", "learn_from_experience",
        "run_structon", "if", "loop"
    ]
    
    return f"""Create a JSON structon for this intent: "{intent}"

Requirements:
1. Must have structure_id, structure_type, intent, description, phases, tension, importance, nodes, edges
2. Each node must have: id, type, phase, description, atomic, args, output
3. Node types: input, process, output
4. Phases: sense, act, feedback
5. Use $variable_name for data flow between nodes

Available atomics: {', '.join(atomics)}

Common patterns:
- Sense phase: get input from context
- Act phase: process with call_llm
- Feedback phase: emit result, optionally learn_from_experience

Example node:
{{
  "id": "a1",
  "type": "process", 
  "phase": "act",
  "description": "Process with LLM",
  "atomic": "call_llm",
  "input": "$input",
  "args": {{"prompt": "Do something with: {{input}}"}},
  "output": "$result"
}}

Return ONLY valid JSON, no explanation."""


def generate_structon_via_llm(
    intent: str,
    llm_func = None
) -> Dict[str, Any]:
    """
    Use LLM to generate a complete structon.
    
    Args:
        intent: What the structon should do
        llm_func: Function to call LLM (default: uses atomic_call_llm)
        
    Returns:
        Generated structon dict
    """
    from .atomics import atomic_call_llm
    
    prompt = generate_structon_prompt(intent)
    
    if llm_func:
        response = llm_func(prompt)
    else:
        response = atomic_call_llm(prompt, {"prompt": "{input}"}, {})
    
    # Parse JSON from response
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            structon = json.loads(response[start:end])
            
            # Ensure it has an ID
            if not structon.get("structure_id"):
                structon["structure_id"] = generate_id()
            
            # Validate
            validation = validate_structon(structon)
            if not validation["valid"]:
                print(f"[Factory] Generated structon has errors: {validation['errors']}")
            
            return structon
    except json.JSONDecodeError as e:
        print(f"[Factory] Failed to parse LLM response: {e}")
    
    return None


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
        prompt: LLM prompt (use {input} for variable)
        input_key: Context key to get input from
        learn: Whether to add learning node
    """
    nodes = [
        create_node("s1", "get", "sense", "input", "Get input", args={"key": input_key}, output_var="$input"),
        create_node("a1", "call_llm", "act", "process", "Process with LLM", "$input", {"prompt": prompt}, "$result"),
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
