"""
Hello World Example

Demonstrates the simplest possible structon execution.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core import Structon, Node, Edge, Phase, NodeType, Interpreter


def create_hello_structon(name: str = "World") -> Structon:
    """Create a simple hello world structon."""
    
    return Structon(
        structure_id="hello_001",
        structure_type="composite",
        intent="greet_user",
        phases=[Phase.SENSE, Phase.ACT, Phase.FEEDBACK],
        tension=0.8,
        importance=0.5,
        nodes=[
            # SENSE: Get the name
            Node(
                id="s1",
                type=NodeType.INPUT,
                phase=Phase.SENSE,
                description="Get name to greet",
                atomic="get",
                args={"key": "name"},
                output="$name"
            ),
            # ACT: Create greeting
            Node(
                id="a1",
                type=NodeType.PROCESS,
                phase=Phase.ACT,
                description="Create greeting message",
                atomic="set",
                input="$name",
                args={"key": "greeting"},
                output="$greeting"
            ),
            # FEEDBACK: Output result
            Node(
                id="f1",
                type=NodeType.OUTPUT,
                phase=Phase.FEEDBACK,
                description="Output the greeting",
                atomic="emit",
                input="$greeting",
                output="$result"
            )
        ],
        edges=[
            Edge("s1", "a1"),
            Edge("a1", "f1")
        ]
    )


def main():
    print("=" * 50)
    print("Structon Hello World Example")
    print("=" * 50)
    print()
    
    # Create the structon
    structon = create_hello_structon()
    
    print(f"Created structon: {structon.structure_id}")
    print(f"Intent: {structon.intent}")
    print(f"Tension: {structon.tension}")
    print(f"Nodes: {len(structon.nodes)}")
    print()
    
    # Create interpreter
    interpreter = Interpreter()
    
    # Run with context
    context = {"name": "Structon World"}
    
    print("Running with context:", context)
    print()
    
    result = interpreter.run(structon, context)
    
    print("Execution Result:")
    print(f"  Success: {result['success']}")
    print(f"  Result: {result['result']}")
    print(f"  Context: {result['context']}")
    print()
    
    print("Execution History:")
    for entry in result['history']:
        print(f"  - {entry['node_id']}: {entry['action']}")
    
    if result['errors']:
        print()
        print("Errors:")
        for error in result['errors']:
            print(f"  - {error}")
    
    print()
    print("=" * 50)
    print("Done!")


if __name__ == "__main__":
    main()
