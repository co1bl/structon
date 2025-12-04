"""
Reasoning Loop Example

Demonstrates the sense-act-feedback loop with tension.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core import (
    Structon, Node, Edge, Phase, NodeType, 
    Interpreter, MainLoop,
    calculate_tension
)


def create_reasoning_structon(question: str) -> Structon:
    """Create a structon for reasoning about a question."""
    
    return Structon(
        structure_id="reasoning_001",
        structure_type="composite",
        intent=f"reason_about: {question}",
        phases=[Phase.SENSE, Phase.ACT, Phase.FEEDBACK],
        tension=0.9,
        importance=0.8,
        nodes=[
            # SENSE: Understand the question
            Node(
                id="s1",
                type=NodeType.INPUT,
                phase=Phase.SENSE,
                description="Load the question",
                atomic="get",
                args={"key": "question"},
                output="$question"
            ),
            Node(
                id="s2",
                type=NodeType.PROCESS,
                phase=Phase.SENSE,
                description="Analyze question complexity",
                atomic="call_llm",
                input="$question",
                args={"prompt": "Rate complexity of this question 1-10: {input}"},
                output="$complexity"
            ),
            
            # ACT: Generate answer
            Node(
                id="a1",
                type=NodeType.PROCESS,
                phase=Phase.ACT,
                description="Generate initial answer",
                atomic="call_llm",
                input="$question",
                args={"prompt": "Answer this question: {input}"},
                output="$initial_answer"
            ),
            Node(
                id="a2",
                type=NodeType.PROCESS,
                phase=Phase.ACT,
                description="Refine answer",
                atomic="call_llm",
                input="$initial_answer",
                args={"prompt": "Improve this answer: {input}"},
                output="$refined_answer"
            ),
            
            # FEEDBACK: Evaluate answer
            Node(
                id="f1",
                type=NodeType.PROCESS,
                phase=Phase.FEEDBACK,
                description="Evaluate answer quality",
                atomic="call_llm",
                input="$refined_answer",
                args={"prompt": "Rate this answer 1-10: {input}. Return JSON: {\"score\": N}"},
                output="$evaluation"
            ),
            Node(
                id="f2",
                type=NodeType.OUTPUT,
                phase=Phase.FEEDBACK,
                description="Output final result",
                atomic="emit",
                input="$refined_answer",
                output="$result"
            )
        ],
        edges=[
            Edge("s1", "s2"),
            Edge("s2", "a1"),
            Edge("a1", "a2"),
            Edge("a2", "f1"),
            Edge("f1", "f2")
        ]
    )


def main():
    print("=" * 60)
    print("Structon Reasoning Loop Example")
    print("=" * 60)
    print()
    
    question = "What are the benefits of self-similar systems?"
    
    # Create structon
    structon = create_reasoning_structon(question)
    
    print(f"Question: {question}")
    print(f"Initial tension: {structon.tension}")
    print()
    
    # Create main loop
    interpreter = Interpreter()
    loop = MainLoop(structon, interpreter)
    
    print("Running main loop...")
    print("-" * 40)
    
    # Run until tension < 0.1 or max 10 iterations
    result = loop.run(threshold=0.1, max_iterations=10)
    
    print("-" * 40)
    print()
    print("Results:")
    print(f"  Iterations: {result['iterations']}")
    print(f"  Final tension: {result['final_tension']:.2f}")
    print()
    
    if result['result']:
        print("Answer:")
        print(f"  {result['result']}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
