"""
Reasoning Loop Example

Demonstrates the sense-act-feedback loop with LLM integration.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core import (
    Structon, Node, Edge, Phase, NodeType, 
    Interpreter,
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
                description="Analyze question",
                atomic="call_llm",
                input="$question",
                args={"prompt": "Briefly analyze this question and identify 2-3 key aspects to address: {input}"},
                output="$analysis"
            ),
            
            # ACT: Generate answer
            Node(
                id="a1",
                type=NodeType.PROCESS,
                phase=Phase.ACT,
                description="Generate initial answer",
                atomic="call_llm",
                input="$question",
                args={"prompt": "Please answer this question thoroughly: {input}"},
                output="$initial_answer"
            ),
            Node(
                id="a2",
                type=NodeType.PROCESS,
                phase=Phase.ACT,
                description="Enhance with analysis",
                atomic="call_llm",
                input="$initial_answer",
                args={"prompt": "Enhance and improve this answer, adding examples where helpful: {input}"},
                output="$enhanced_answer"
            ),
            
            # FEEDBACK: Evaluate and output
            Node(
                id="f1",
                type=NodeType.PROCESS,
                phase=Phase.FEEDBACK,
                description="Self-evaluate answer",
                atomic="call_llm",
                input="$enhanced_answer",
                args={"prompt": "Rate this answer from 1-10 and briefly explain why: {input}"},
                output="$evaluation"
            ),
            Node(
                id="f2",
                type=NodeType.OUTPUT,
                phase=Phase.FEEDBACK,
                description="Output final result",
                atomic="emit",
                input="$enhanced_answer",
                output="$result"
            )
        ],
        edges=[
            # Sense phase flow
            Edge("s1", "s2"),
            # Act phase flow
            Edge("a1", "a2"),
            # Feedback phase flow
            Edge("f1", "f2")
        ]
    )


def create_simple_qa_structon() -> Structon:
    """Create a simpler Q&A structon for testing."""
    
    return Structon(
        structure_id="simple_qa_001",
        structure_type="composite",
        intent="answer_question",
        phases=[Phase.SENSE, Phase.ACT, Phase.FEEDBACK],
        tension=0.8,
        importance=0.7,
        nodes=[
            # SENSE: Get the question
            Node(
                id="s1",
                type=NodeType.INPUT,
                phase=Phase.SENSE,
                description="Get question from context",
                atomic="get",
                args={"key": "question"},
                output="$question"
            ),
            
            # ACT: Answer it
            Node(
                id="a1",
                type=NodeType.PROCESS,
                phase=Phase.ACT,
                description="Generate answer using LLM",
                atomic="call_llm",
                input="$question",
                args={"prompt": "Please provide a clear, comprehensive answer to this question: {input}"},
                output="$answer"
            ),
            
            # FEEDBACK: Output
            Node(
                id="f1",
                type=NodeType.OUTPUT,
                phase=Phase.FEEDBACK,
                description="Emit the answer",
                atomic="emit",
                input="$answer",
                output="$result"
            )
        ],
        edges=[
            Edge("s1", "a1"),
            Edge("a1", "f1")
        ]
    )


def run_simple_example():
    """Run a simple Q&A example."""
    print("=" * 60)
    print("Simple Q&A Example")
    print("=" * 60)
    print()
    
    question = "What are the benefits of self-similar systems?"
    
    # Create structon
    structon = create_simple_qa_structon()
    
    print(f"Question: {question}")
    print(f"Structon: {structon.structure_id}")
    print(f"Tension: {structon.tension}")
    print()
    
    # Create interpreter
    interpreter = Interpreter()
    
    print("Calling LLM...")
    print("-" * 40)
    
    # Run with question in context
    result = interpreter.run(structon, {"question": question})
    
    print("-" * 40)
    print()
    
    if result['success']:
        print("✅ Success!")
        print()
        print("Answer:")
        print("-" * 40)
        print(result['result'])
        print("-" * 40)
    else:
        print("❌ Failed:")
        for error in result['errors']:
            print(f"  - {error}")
    
    print()
    print("Execution History:")
    for entry in result['history']:
        status = "✓" if entry['action'] == 'completed' else "✗"
        print(f"  {status} {entry['node_id']}: {entry['action']}")
    
    print()
    print("=" * 60)


def run_full_reasoning_example():
    """Run the full reasoning example with multiple LLM calls."""
    print("=" * 60)
    print("Full Reasoning Loop Example")
    print("=" * 60)
    print()
    
    question = "What are the benefits of self-similar systems in software architecture?"
    
    # Create structon
    structon = create_reasoning_structon(question)
    
    print(f"Question: {question}")
    print(f"Structon: {structon.structure_id}")
    print(f"Nodes: {len(structon.nodes)}")
    print(f"Initial Tension: {structon.tension}")
    print()
    
    # Create interpreter
    interpreter = Interpreter()
    
    print("Running sense-act-feedback loop...")
    print("(This makes multiple LLM calls, please wait...)")
    print("-" * 40)
    
    # Run with question in context
    result = interpreter.run(structon, {"question": question})
    
    print("-" * 40)
    print()
    
    if result['success']:
        print("✅ Success!")
        print()
        
        # Show intermediate results
        context = result['context']
        
        if context.get('analysis'):
            print("📊 Analysis:")
            print(f"   {context['analysis'][:200]}...")
            print()
        
        if context.get('evaluation'):
            print("📝 Self-Evaluation:")
            print(f"   {context['evaluation'][:200]}...")
            print()
        
        print("💡 Final Answer:")
        print("-" * 40)
        print(result['result'])
        print("-" * 40)
    else:
        print("❌ Failed:")
        for error in result['errors']:
            print(f"  - {error}")
    
    print()
    print("Execution History:")
    for entry in result['history']:
        status = "✓" if entry['action'] == 'completed' else "✗"
        print(f"  {status} {entry['node_id']}: {entry['action']}")
    
    # Update tension based on result
    if result['success']:
        structon.tension = 0.1  # Resolved
    
    print()
    print(f"Final Tension: {structon.tension}")
    print("=" * 60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Structon Reasoning Examples")
    parser.add_argument("--simple", action="store_true", help="Run simple Q&A example")
    parser.add_argument("--full", action="store_true", help="Run full reasoning example")
    args = parser.parse_args()
    
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: No API key found!")
        print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
        print()
        print("   Example:")
        print("   export OPENAI_API_KEY='sk-...'")
        print()
    
    if args.simple:
        run_simple_example()
    elif args.full:
        run_full_reasoning_example()
    else:
        # Default: run simple example
        print("Use --simple for quick test or --full for complete reasoning loop")
        print()
        run_simple_example()


if __name__ == "__main__":
    main()