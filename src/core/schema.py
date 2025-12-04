"""
Structon Schema Module

Defines the Structon class and validation logic.
"""

import json
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class StructonType(Enum):
    SENSE = "sense"
    ACT = "act"
    FEEDBACK = "feedback"
    COMPOSITE = "composite"
    BLUEPRINT = "blueprint"


class NodeType(Enum):
    INPUT = "input"
    PROCESS = "process"
    OUTPUT = "output"
    SUB_STRUCTON = "sub_structon"
    DECISION = "decision"


class Phase(Enum):
    SENSE = "sense"
    ACT = "act"
    FEEDBACK = "feedback"


class NodeState(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Node:
    """A single node within a structon."""
    
    id: str
    type: NodeType
    phase: Phase
    description: str
    atomic: Optional[str] = None
    structon_ref: Optional[str] = None
    input: Optional[Any] = None
    output: Optional[str] = None
    args: Dict[str, Any] = field(default_factory=dict)
    tension: float = 0.5
    state: NodeState = NodeState.PENDING
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value if isinstance(self.type, NodeType) else self.type,
            "phase": self.phase.value if isinstance(self.phase, Phase) else self.phase,
            "description": self.description,
            "atomic": self.atomic,
            "structon_ref": self.structon_ref,
            "input": self.input,
            "output": self.output,
            "args": self.args,
            "tension": self.tension,
            "state": self.state.value if isinstance(self.state, NodeState) else self.state
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        return cls(
            id=data["id"],
            type=NodeType(data["type"]) if isinstance(data["type"], str) else data["type"],
            phase=Phase(data["phase"]) if isinstance(data["phase"], str) else data["phase"],
            description=data["description"],
            atomic=data.get("atomic"),
            structon_ref=data.get("structon_ref"),
            input=data.get("input"),
            output=data.get("output"),
            args=data.get("args", {}),
            tension=data.get("tension", 0.5),
            state=NodeState(data.get("state", "pending"))
        )


@dataclass
class Edge:
    """A connection between two nodes."""
    
    from_node: str
    to_node: str
    condition: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"from": self.from_node, "to": self.to_node}
        if self.condition:
            result["condition"] = self.condition
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge":
        return cls(
            from_node=data["from"],
            to_node=data["to"],
            condition=data.get("condition")
        )


@dataclass
class TensionProfile:
    """Tension-related metadata for a structon."""
    
    max_tension: float = 1.0
    node_conflicts: List[str] = field(default_factory=list)
    barriers: List[str] = field(default_factory=list)
    unresolved_desires: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_tension": self.max_tension,
            "node_conflicts": self.node_conflicts,
            "barriers": self.barriers,
            "unresolved_desires": self.unresolved_desires
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TensionProfile":
        return cls(
            max_tension=data.get("max_tension", 1.0),
            node_conflicts=data.get("node_conflicts", []),
            barriers=data.get("barriers", []),
            unresolved_desires=data.get("unresolved_desires", [])
        )


@dataclass
class Metadata:
    """Metadata for a structon."""
    
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: int = 1
    parent_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "parent_id": self.parent_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Metadata":
        return cls(
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat()),
            version=data.get("version", 1),
            parent_id=data.get("parent_id")
        )


@dataclass
class Structon:
    """
    The core Structon class.
    
    A structon is a self-similar cognitive unit with three phases:
    sense, act, and feedback. Each can contain other structons.
    """
    
    structure_id: str
    structure_type: StructonType
    intent: str
    phases: List[Phase]
    tension: float
    importance: float
    nodes: List[Node]
    edges: List[Edge]
    tension_profile: TensionProfile = field(default_factory=TensionProfile)
    metadata: Metadata = field(default_factory=Metadata)
    
    def __post_init__(self):
        """Validate after initialization."""
        self.validate()
    
    def validate(self) -> bool:
        """Validate the structon structure."""
        # Check required fields
        if not self.structure_id:
            raise ValueError("structure_id is required")
        if not self.intent:
            raise ValueError("intent is required")
        if not self.nodes:
            raise ValueError("At least one node is required")
        
        # Check tension bounds
        if not 0.0 <= self.tension <= 1.0:
            raise ValueError("tension must be between 0.0 and 1.0")
        if not 0.0 <= self.importance <= 1.0:
            raise ValueError("importance must be between 0.0 and 1.0")
        
        # Validate edges reference existing nodes
        node_ids = {node.id for node in self.nodes}
        for edge in self.edges:
            if edge.from_node not in node_ids:
                raise ValueError(f"Edge references non-existent node: {edge.from_node}")
            if edge.to_node not in node_ids:
                raise ValueError(f"Edge references non-existent node: {edge.to_node}")
        
        # Validate node types
        for node in self.nodes:
            if node.type == NodeType.SUB_STRUCTON and not node.structon_ref:
                raise ValueError(f"Sub-structon node {node.id} must have structon_ref")
            if node.type != NodeType.SUB_STRUCTON and not node.atomic:
                raise ValueError(f"Node {node.id} must have atomic function")
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "structure_id": self.structure_id,
            "structure_type": self.structure_type.value if isinstance(self.structure_type, StructonType) else self.structure_type,
            "intent": self.intent,
            "phases": [p.value if isinstance(p, Phase) else p for p in self.phases],
            "tension": self.tension,
            "importance": self.importance,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "tension_profile": self.tension_profile.to_dict(),
            "metadata": self.metadata.to_dict()
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Structon":
        """Create from dictionary."""
        return cls(
            structure_id=data["structure_id"],
            structure_type=StructonType(data["structure_type"]),
            intent=data["intent"],
            phases=[Phase(p) if isinstance(p, str) else p for p in data["phases"]],
            tension=data["tension"],
            importance=data["importance"],
            nodes=[Node.from_dict(n) for n in data["nodes"]],
            edges=[Edge.from_dict(e) for e in data["edges"]],
            tension_profile=TensionProfile.from_dict(data.get("tension_profile", {})),
            metadata=Metadata.from_dict(data.get("metadata", {}))
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "Structon":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def from_file(cls, filepath: str) -> "Structon":
        """Load from file."""
        with open(filepath, 'r') as f:
            return cls.from_dict(json.load(f))
    
    def save(self, filepath: str) -> None:
        """Save to file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def create(cls, intent: str, phases: List[str] = None) -> "Structon":
        """Create a new empty structon."""
        if phases is None:
            phases = ["sense", "act", "feedback"]
        
        return cls(
            structure_id=str(uuid.uuid4()),
            structure_type=StructonType.COMPOSITE,
            intent=intent,
            phases=[Phase(p) for p in phases],
            tension=0.8,
            importance=0.5,
            nodes=[],
            edges=[],
            tension_profile=TensionProfile(),
            metadata=Metadata()
        )
    
    def add_node(self, node: Node) -> None:
        """Add a node to the structon."""
        self.nodes.append(node)
        self.metadata.updated_at = datetime.utcnow().isoformat()
    
    def add_edge(self, from_node: str, to_node: str, condition: str = None) -> None:
        """Add an edge between nodes."""
        self.edges.append(Edge(from_node, to_node, condition))
        self.metadata.updated_at = datetime.utcnow().isoformat()
    
    def resolve(self) -> None:
        """Mark this structon as resolved (low tension)."""
        self.tension = 0.1
        for node in self.nodes:
            node.state = NodeState.COMPLETED
        self.metadata.updated_at = datetime.utcnow().isoformat()
    
    def get_nodes_by_phase(self, phase: Phase) -> List[Node]:
        """Get all nodes belonging to a specific phase."""
        return [n for n in self.nodes if n.phase == phase]
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
    
    def __repr__(self) -> str:
        return f"Structon(id={self.structure_id}, intent={self.intent}, tension={self.tension})"
