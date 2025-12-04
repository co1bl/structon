"""
Basic Tests for Structon Core

Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core import (
    Structon, Node, Edge, Phase, NodeType, NodeState,
    Interpreter, calculate_tension
)


class TestStructon:
    """Tests for Structon class."""
    
    def test_create_structon(self):
        """Test basic structon creation."""
        s = Structon.create("test_intent")
        
        assert s.structure_id is not None
        assert s.intent == "test_intent"
        assert Phase.SENSE in s.phases
        assert Phase.ACT in s.phases
        assert Phase.FEEDBACK in s.phases
    
    def test_structon_validation(self):
        """Test structon validation."""
        with pytest.raises(ValueError):
            Structon(
                structure_id="",  # Empty ID should fail
                structure_type="composite",
                intent="test",
                phases=[Phase.SENSE],
                tension=0.5,
                importance=0.5,
                nodes=[],
                edges=[]
            )
    
    def test_tension_bounds(self):
        """Test tension must be between 0 and 1."""
        with pytest.raises(ValueError):
            Structon(
                structure_id="test",
                structure_type="composite",
                intent="test",
                phases=[Phase.SENSE],
                tension=1.5,  # Invalid
                importance=0.5,
                nodes=[Node(
                    id="n1",
                    type=NodeType.INPUT,
                    phase=Phase.SENSE,
                    description="test",
                    atomic="get"
                )],
                edges=[]
            )
    
    def test_add_node(self):
        """Test adding nodes."""
        s = Structon.create("test")
        node = Node(
            id="n1",
            type=NodeType.INPUT,
            phase=Phase.SENSE,
            description="test node",
            atomic="get"
        )
        s.nodes.append(node)
        s.add_node(Node(
            id="n2",
            type=NodeType.OUTPUT,
            phase=Phase.FEEDBACK,
            description="output",
            atomic="emit"
        ))
        
        assert len(s.nodes) == 2
    
    def test_to_dict_and_back(self):
        """Test serialization."""
        s = Structon.create("serialize_test")
        s.nodes.append(Node(
            id="n1",
            type=NodeType.INPUT,
            phase=Phase.SENSE,
            description="test",
            atomic="get"
        ))
        
        d = s.to_dict()
        s2 = Structon.from_dict(d)
        
        assert s2.structure_id == s.structure_id
        assert s2.intent == s.intent
        assert len(s2.nodes) == len(s.nodes)


class TestNode:
    """Tests for Node class."""
    
    def test_create_node(self):
        """Test node creation."""
        node = Node(
            id="test_node",
            type=NodeType.PROCESS,
            phase=Phase.ACT,
            description="A test node",
            atomic="call_llm",
            args={"prompt": "test"}
        )
        
        assert node.id == "test_node"
        assert node.type == NodeType.PROCESS
        assert node.phase == Phase.ACT
        assert node.state == NodeState.PENDING
    
    def test_node_to_dict(self):
        """Test node serialization."""
        node = Node(
            id="n1",
            type=NodeType.INPUT,
            phase=Phase.SENSE,
            description="test",
            atomic="get",
            output="$result"
        )
        
        d = node.to_dict()
        
        assert d["id"] == "n1"
        assert d["type"] == "input"
        assert d["phase"] == "sense"
        assert d["output"] == "$result"


class TestTension:
    """Tests for tension calculation."""
    
    def test_basic_tension(self):
        """Test basic tension calculation."""
        tension = calculate_tension(
            importance=1.0,
            urgency=1.0,
            unresolved=1.0,
            blocking=1.0
        )
        
        assert tension == 1.0
    
    def test_zero_tension(self):
        """Test zero tension."""
        tension = calculate_tension(
            importance=0.0,
            urgency=0.0,
            unresolved=0.0,
            blocking=0.0
        )
        
        assert tension == 0.0
    
    def test_weighted_tension(self):
        """Test weighted tension calculation."""
        tension = calculate_tension(
            importance=0.5,
            urgency=0.5,
            unresolved=0.5,
            blocking=0.5
        )
        
        assert tension == 0.5


class TestInterpreter:
    """Tests for Interpreter class."""
    
    def test_simple_execution(self):
        """Test simple structon execution."""
        s = Structon(
            structure_id="exec_test",
            structure_type="composite",
            intent="test_execution",
            phases=[Phase.SENSE, Phase.ACT, Phase.FEEDBACK],
            tension=0.5,
            importance=0.5,
            nodes=[
                Node(
                    id="n1",
                    type=NodeType.INPUT,
                    phase=Phase.SENSE,
                    description="Get value",
                    atomic="get",
                    args={"key": "input"},
                    output="$value"
                ),
                Node(
                    id="n2",
                    type=NodeType.OUTPUT,
                    phase=Phase.FEEDBACK,
                    description="Emit result",
                    atomic="emit",
                    input="$value",
                    output="$result"
                )
            ],
            edges=[Edge("n1", "n2")]
        )
        
        interpreter = Interpreter()
        result = interpreter.run(s, {"input": "hello"})
        
        assert result["success"] == True
        assert result["result"] == "hello"
    
    def test_execution_order(self):
        """Test nodes execute in correct order."""
        s = Structon(
            structure_id="order_test",
            structure_type="composite",
            intent="test_order",
            phases=[Phase.SENSE, Phase.ACT, Phase.FEEDBACK],
            tension=0.5,
            importance=0.5,
            nodes=[
                Node(
                    id="a",
                    type=NodeType.INPUT,
                    phase=Phase.SENSE,
                    description="First",
                    atomic="get",
                    args={"key": "x"},
                    output="$a"
                ),
                Node(
                    id="b",
                    type=NodeType.PROCESS,
                    phase=Phase.ACT,
                    description="Second",
                    atomic="get",
                    input="$a",
                    output="$b"
                ),
                Node(
                    id="c",
                    type=NodeType.OUTPUT,
                    phase=Phase.FEEDBACK,
                    description="Third",
                    atomic="emit",
                    input="$b",
                    output="$c"
                )
            ],
            edges=[
                Edge("a", "b"),
                Edge("b", "c")
            ]
        )
        
        interpreter = Interpreter()
        result = interpreter.run(s, {"x": "test"})
        
        # Check execution order in history
        history = result["history"]
        assert len(history) == 3
        assert history[0]["node_id"] == "a"
        assert history[1]["node_id"] == "b"
        assert history[2]["node_id"] == "c"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
