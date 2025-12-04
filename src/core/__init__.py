"""
Structon Core Module

Contains the fundamental components:
- Schema: Structon data structures
- Atomics: Primitive operations
- Interpreter: Execution engine
- Tension: Drive force management
- Memory: Living memory system
"""

from .schema import (
    Structon,
    Node,
    Edge,
    TensionProfile,
    Metadata,
    StructonType,
    NodeType,
    Phase,
    NodeState
)

from .atomics import (
    get_atomic,
    list_atomics,
    registry
)

from .interpreter import (
    Interpreter,
    ExecutionContext,
    MainLoop
)

from .tension import (
    calculate_tension,
    calculate_structon_tension,
    propagate_tension_up,
    inherit_importance,
    update_all_tensions,
    TensionConfig,
    TensionManager
)

from .memory import (
    MemoryStructon,
    LivingMemory
)

__all__ = [
    # Schema
    "Structon",
    "Node",
    "Edge",
    "TensionProfile",
    "Metadata",
    "StructonType",
    "NodeType",
    "Phase",
    "NodeState",
    
    # Atomics
    "get_atomic",
    "list_atomics",
    "registry",
    
    # Interpreter
    "Interpreter",
    "ExecutionContext",
    "MainLoop",
    
    # Tension
    "calculate_tension",
    "calculate_structon_tension",
    "propagate_tension_up",
    "inherit_importance",
    "update_all_tensions",
    "TensionConfig",
    "TensionManager",
    
    # Memory
    "MemoryStructon",
    "LivingMemory",
]