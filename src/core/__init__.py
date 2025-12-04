"""
Structon Core Module

Contains the fundamental components:
- Schema: Structon data structures
- Atomics: Primitive operations
- Interpreter: Execution engine
- Tension: Drive force management
- Memory: Living memory system
- Factory: Structon creation helpers
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
    registry,
    set_interpreter
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

from .factory import (
    # Validation
    validate_structon,
    is_valid_structon,
    
    # Blueprint loading
    load_blueprint,
    list_blueprints,
    
    # Creation helpers
    generate_id,
    create_node,
    create_structon,
    create_from_blueprint,
    
    # LLM generation (template-based)
    generate_customization_prompt,
    generate_structon_via_llm,
    
    # Saving
    save_structon,
    
    # Quick builders
    quick_llm_structon,
    quick_memory_structon,
    
    # Pool composition
    load_from_pool,
    list_pool,
    compose_from_pools,
    compose_custom
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
    "set_interpreter",
    
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
    
    # Factory
    "validate_structon",
    "is_valid_structon",
    "load_blueprint",
    "list_blueprints",
    "generate_id",
    "create_node",
    "create_structon",
    "create_from_blueprint",
    "generate_customization_prompt",
    "generate_structon_via_llm",
    "save_structon",
    "quick_llm_structon",
    "quick_memory_structon",
    
    # Pool composition
    "load_from_pool",
    "list_pool",
    "compose_from_pools",
    "compose_custom",
]
# Evolution
from .evolution import (
    auto_select,
    auto_compose,
    track_success,
    get_success_rate,
    update_tension,
    evolve_structon,
    generate_missing,
    prune_pool,
    evaluate_result,
    evolution_step,
    evolution_loop
)
