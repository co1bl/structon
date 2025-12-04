"""
Tension Module

Handles tension calculation and propagation throughout the structon tree.

Tension is the drive force:
- High tension = unresolved, urgent, needs attention
- Low tension = resolved, complete, can wait
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class TensionConfig:
    """Configuration for tension calculation."""
    
    importance_weight: float = 0.3
    urgency_weight: float = 0.3
    unresolved_weight: float = 0.2
    blocking_weight: float = 0.2
    
    # Propagation weights
    max_weight: float = 0.7
    avg_weight: float = 0.3
    
    # Inheritance decay
    importance_decay: float = 0.9


# Default configuration
DEFAULT_CONFIG = TensionConfig()


def calculate_tension(
    importance: float = 0.5,
    urgency: float = 0.5,
    unresolved: float = 0.5,
    blocking: float = 0.0,
    config: TensionConfig = None
) -> float:
    """
    Calculate tension based on multiple factors.
    
    Args:
        importance: How important is this (0.0 to 1.0)
        urgency: How urgent is this (0.0 to 1.0)
        unresolved: How incomplete is this (0.0 to 1.0)
        blocking: Is this blocking others (0.0 to 1.0)
        config: Optional tension configuration
    
    Returns:
        Tension value between 0.0 and 1.0
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    tension = (
        importance * config.importance_weight +
        urgency * config.urgency_weight +
        unresolved * config.unresolved_weight +
        blocking * config.blocking_weight
    )
    
    return max(0.0, min(1.0, tension))


def calculate_urgency(deadline: Optional[str] = None, max_time: float = 86400.0) -> float:
    """
    Calculate urgency based on deadline.
    
    Args:
        deadline: ISO format deadline string
        max_time: Maximum time in seconds (default: 24 hours)
    
    Returns:
        Urgency value between 0.0 and 1.0
    """
    if not deadline:
        return 0.5  # Default urgency
    
    from datetime import datetime
    
    try:
        deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        now = datetime.now(deadline_dt.tzinfo) if deadline_dt.tzinfo else datetime.now()
        
        time_left = (deadline_dt - now).total_seconds()
        
        if time_left <= 0:
            return 1.0  # Past deadline
        elif time_left >= max_time:
            return 0.0  # Far in future
        else:
            return 1.0 - (time_left / max_time)
    except Exception:
        return 0.5


def calculate_unresolved_ratio(nodes: List[Dict[str, Any]]) -> float:
    """
    Calculate the ratio of unresolved nodes.
    
    Args:
        nodes: List of node dictionaries
    
    Returns:
        Ratio between 0.0 (all resolved) and 1.0 (none resolved)
    """
    if not nodes:
        return 0.0
    
    resolved_count = sum(
        1 for node in nodes
        if node.get("state") in ("completed", "resolved")
    )
    
    return 1.0 - (resolved_count / len(nodes))


def calculate_blocking_factor(blocked_count: int, weight_per_blocked: float = 0.2) -> float:
    """
    Calculate blocking factor based on how many items this blocks.
    
    Args:
        blocked_count: Number of items blocked by this
        weight_per_blocked: Weight per blocked item
    
    Returns:
        Blocking factor between 0.0 and 1.0
    """
    return min(1.0, blocked_count * weight_per_blocked)


def calculate_structon_tension(structon: Dict[str, Any], config: TensionConfig = None) -> float:
    """
    Calculate tension for a complete structon.
    
    Args:
        structon: Structon dictionary
        config: Optional tension configuration
    
    Returns:
        Tension value between 0.0 and 1.0
    """
    importance = structon.get("importance", 0.5)
    
    # Calculate urgency from deadline if present
    deadline = structon.get("metadata", {}).get("deadline")
    urgency = calculate_urgency(deadline)
    
    # Calculate unresolved ratio from nodes
    nodes = structon.get("nodes", [])
    unresolved = calculate_unresolved_ratio(nodes)
    
    # Calculate blocking from tension profile
    tension_profile = structon.get("tension_profile", {})
    blocked_count = len(tension_profile.get("blocked_by", []))
    blocking = calculate_blocking_factor(blocked_count)
    
    return calculate_tension(importance, urgency, unresolved, blocking, config)


def propagate_tension_up(
    child_tensions: List[float],
    config: TensionConfig = None
) -> float:
    """
    Propagate tension from children to parent.
    
    Uses hybrid formula: max * 0.7 + avg * 0.3
    
    Args:
        child_tensions: List of child tension values
        config: Optional tension configuration
    
    Returns:
        Propagated tension value
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    if not child_tensions:
        return 0.5
    
    max_tension = max(child_tensions)
    avg_tension = sum(child_tensions) / len(child_tensions)
    
    return max_tension * config.max_weight + avg_tension * config.avg_weight


def inherit_importance(
    parent_importance: float,
    child_importance: Optional[float] = None,
    config: TensionConfig = None
) -> float:
    """
    Inherit importance from parent to child.
    
    Args:
        parent_importance: Parent's importance value
        child_importance: Child's existing importance (if any)
        config: Optional tension configuration
    
    Returns:
        Child's importance value
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    # If child has explicit importance, use it
    if child_importance is not None:
        return child_importance
    
    # Otherwise inherit with decay
    return parent_importance * config.importance_decay


def update_all_tensions(root: Dict[str, Any], config: TensionConfig = None) -> None:
    """
    Update all tensions in a structon tree.
    
    1. Inherit importance (top-down)
    2. Calculate leaf tensions
    3. Propagate tensions up (bottom-up)
    
    Args:
        root: Root structon dictionary
        config: Optional tension configuration
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    # Step 1: Propagate importance down
    _propagate_importance_down(root, root.get("importance", 0.5), config)
    
    # Step 2 & 3: Calculate and propagate tensions up
    root["tension"] = _propagate_tension_up_recursive(root, config)


def _propagate_importance_down(
    node: Dict[str, Any],
    parent_importance: float,
    config: TensionConfig
) -> None:
    """Recursively propagate importance down the tree."""
    # Set this node's importance
    if "importance" not in node or node["importance"] is None:
        node["importance"] = parent_importance * config.importance_decay
    
    # Propagate to children (sub-structons in nodes)
    for n in node.get("nodes", []):
        if n.get("structon_ref"):
            # This would need to load the sub-structon
            # For now, just propagate to node-level importance
            n["importance"] = inherit_importance(
                node["importance"],
                n.get("importance"),
                config
            )


def _propagate_tension_up_recursive(
    node: Dict[str, Any],
    config: TensionConfig
) -> float:
    """Recursively calculate and propagate tensions up."""
    children = node.get("nodes", [])
    
    if not children:
        # Leaf node: calculate tension
        return calculate_structon_tension(node, config)
    
    # Get child tensions
    child_tensions = []
    for child in children:
        if child.get("structon_ref"):
            # Would need to load sub-structon
            # Use node's tension as proxy
            child_tensions.append(child.get("tension", 0.5))
        else:
            child_tensions.append(child.get("tension", 0.5))
    
    # Propagate up
    return propagate_tension_up(child_tensions, config)


class TensionManager:
    """
    Manages tension across a system of structons.
    """
    
    def __init__(self, config: TensionConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.structons: Dict[str, Dict[str, Any]] = {}
    
    def register(self, structon: Dict[str, Any]) -> None:
        """Register a structon."""
        self.structons[structon["structure_id"]] = structon
    
    def unregister(self, structure_id: str) -> None:
        """Unregister a structon."""
        self.structons.pop(structure_id, None)
    
    def update_tension(self, structure_id: str) -> float:
        """Update tension for a specific structon."""
        structon = self.structons.get(structure_id)
        if structon:
            structon["tension"] = calculate_structon_tension(structon, self.config)
            return structon["tension"]
        return 0.0
    
    def update_all(self) -> None:
        """Update tensions for all registered structons."""
        for structon in self.structons.values():
            structon["tension"] = calculate_structon_tension(structon, self.config)
    
    def get_highest_tension(self) -> Optional[Dict[str, Any]]:
        """Get the structon with highest tension."""
        if not self.structons:
            return None
        
        return max(
            self.structons.values(),
            key=lambda s: s.get("tension", 0)
        )
    
    def get_by_tension_threshold(self, threshold: float) -> List[Dict[str, Any]]:
        """Get all structons with tension above threshold."""
        return [
            s for s in self.structons.values()
            if s.get("tension", 0) >= threshold
        ]
    
    def resolve(self, structure_id: str) -> None:
        """Mark a structon as resolved (low tension)."""
        structon = self.structons.get(structure_id)
        if structon:
            structon["tension"] = 0.1
            for node in structon.get("nodes", []):
                node["state"] = "completed"
