"""
Structon Interpreter Module

Executes structons by traversing nodes and calling atomic functions.
"""

from typing import Dict, Any, List, Optional
from .schema import Structon, Node, NodeState, Phase
from .atomics import get_atomic


class ExecutionContext:
    """Context for structon execution."""
    
    def __init__(self, initial_context: Dict[str, Any] = None):
        self.variables: Dict[str, Any] = initial_context or {}
        self.history: List[Dict[str, Any]] = []
        self.errors: List[str] = []
    
    def set(self, name: str, value: Any) -> None:
        """Set a variable."""
        # Remove $ prefix if present
        if name.startswith("$"):
            name = name[1:]
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable."""
        if name.startswith("$"):
            name = name[1:]
        return self.variables.get(name)
    
    def resolve(self, ref: Any) -> Any:
        """Resolve a value or variable reference."""
        if isinstance(ref, str) and ref.startswith("$"):
            return self.get(ref[1:])
        elif isinstance(ref, list):
            return [self.resolve(item) for item in ref]
        return ref
    
    def log(self, node_id: str, action: str, result: Any = None) -> None:
        """Log execution history."""
        self.history.append({
            "node_id": node_id,
            "action": action,
            "result": result
        })
    
    def add_error(self, error: str) -> None:
        """Add an error."""
        self.errors.append(error)


class Interpreter:
    """
    Executes structons by traversing nodes and calling atomic functions.
    
    The interpreter follows the sense-act-feedback pattern at every level.
    """
    
    def __init__(self, structon_loader: callable = None):
        self.structon_loader = structon_loader or self._default_loader
    
    def _default_loader(self, structon_ref: str) -> Optional[Structon]:
        """Default structon loader from file."""
        try:
            return Structon.from_file(f"./structons/{structon_ref}.json")
        except Exception:
            return None
    
    def run(self, structon: Structon, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a structon and return the result.
        
        Args:
            structon: The structon to execute
            initial_context: Initial variable context
        
        Returns:
            Dictionary with result, context, and execution metadata
        """
        context = ExecutionContext(initial_context)
        
        # Get nodes in execution order
        ordered_nodes = self._topological_sort(structon.nodes, structon.edges)
        
        result = None
        
        for node in ordered_nodes:
            try:
                result = self._execute_node(node, context, structon)
                
                # Store output in context
                if node.output:
                    context.set(node.output, result)
                
                # Update node state
                node.state = NodeState.COMPLETED
                
                context.log(node.id, "completed", result)
                
            except Exception as e:
                node.state = NodeState.FAILED
                context.add_error(f"Node {node.id} failed: {str(e)}")
                context.log(node.id, "failed", str(e))
        
        return {
            "result": result,
            "context": context.variables,
            "history": context.history,
            "errors": context.errors,
            "success": len(context.errors) == 0
        }
    
    def _execute_node(self, node: Node, context: ExecutionContext, structon: Structon) -> Any:
        """Execute a single node."""
        node.state = NodeState.ACTIVE
        
        # Resolve inputs
        input_data = context.resolve(node.input) if node.input else None
        
        # Handle sub-structon
        if node.structon_ref:
            sub_structon = self.structon_loader(node.structon_ref)
            if sub_structon:
                sub_result = self.run(sub_structon, context.variables)
                return sub_result.get("result")
            else:
                raise ValueError(f"Could not load sub-structon: {node.structon_ref}")
        
        # Handle atomic function
        if node.atomic:
            atomic_func = get_atomic(node.atomic)
            return atomic_func(input_data, node.args, context.variables)
        
        # No operation
        return input_data
    
    def _topological_sort(self, nodes: List[Node], edges: List) -> List[Node]:
        """Sort nodes in execution order based on edges."""
        if not nodes:
            return []
        
        # Build adjacency list
        node_map = {node.id: node for node in nodes}
        node_ids = set(node_map.keys())
        in_degree = {node.id: 0 for node in nodes}
        adj = {node.id: [] for node in nodes}
        
        for edge in edges:
            # Only consider edges where BOTH nodes are in our subset
            if edge.from_node in node_ids and edge.to_node in node_ids:
                adj[edge.from_node].append(edge.to_node)
                in_degree[edge.to_node] += 1
        
        # Kahn's algorithm
        queue = [nid for nid, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            nid = queue.pop(0)
            result.append(node_map[nid])
            
            for neighbor in adj[nid]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check for cycles
        if len(result) != len(nodes):
            # Fallback: return nodes in order by phase
            return self._sort_by_phase(nodes)
        
        return result
    
    def _sort_by_phase(self, nodes: List[Node]) -> List[Node]:
        """Sort nodes by phase: sense, then act, then feedback."""
        phase_order = {Phase.SENSE: 0, Phase.ACT: 1, Phase.FEEDBACK: 2}
        return sorted(nodes, key=lambda n: phase_order.get(n.phase, 1))
    
    def run_phase(self, structon: Structon, phase: Phase, context: ExecutionContext) -> Any:
        """Execute only nodes of a specific phase."""
        phase_nodes = structon.get_nodes_by_phase(phase)
        ordered_nodes = self._topological_sort(phase_nodes, structon.edges)
        
        result = None
        for node in ordered_nodes:
            result = self._execute_node(node, context, structon)
            if node.output:
                context.set(node.output, result)
        
        return result


class MainLoop:
    """
    The main sense-act-feedback loop.
    
    Runs until tension falls below threshold or max iterations reached.
    """
    
    def __init__(self, root_structon: Structon, interpreter: Interpreter = None):
        self.root = root_structon
        self.interpreter = interpreter or Interpreter()
        self.iterations = 0
        self.max_iterations = 1000
        self.threshold = 0.1
    
    def run(self, threshold: float = 0.1, max_iterations: int = 1000) -> Dict[str, Any]:
        """
        Run the main loop.
        
        Args:
            threshold: Stop when tension falls below this
            max_iterations: Maximum number of iterations
        
        Returns:
            Final result and execution metadata
        """
        self.threshold = threshold
        self.max_iterations = max_iterations
        self.iterations = 0
        
        context = ExecutionContext()
        
        while self._should_continue():
            self.iterations += 1
            
            # 1. SENSE
            sense_result = self._run_sense(context)
            
            # 2. SELECT highest tension
            target = self._select_target(sense_result)
            if not target:
                break
            
            # 3. ACT
            act_result = self._run_act(target, context)
            
            # 4. FEEDBACK
            feedback_result = self._run_feedback(target, act_result, context)
            
            # 5. Update tension
            self._update_tension(target, feedback_result)
        
        return {
            "result": context.get("result"),
            "iterations": self.iterations,
            "final_tension": self.root.tension,
            "context": context.variables
        }
    
    def _should_continue(self) -> bool:
        """Check if loop should continue."""
        return (
            self.root.tension > self.threshold and
            self.iterations < self.max_iterations
        )
    
    def _run_sense(self, context: ExecutionContext) -> Any:
        """Run sense phase."""
        sense_nodes = self.root.get_nodes_by_phase(Phase.SENSE)
        if sense_nodes:
            return self.interpreter.run_phase(self.root, Phase.SENSE, context)
        return context.variables
    
    def _select_target(self, sense_result: Any) -> Optional[Structon]:
        """Select structon with highest tension."""
        # For now, return root. In full implementation, would traverse tree.
        return self.root if self.root.tension > self.threshold else None
    
    def _run_act(self, target: Structon, context: ExecutionContext) -> Any:
        """Run act phase."""
        return self.interpreter.run_phase(target, Phase.ACT, context)
    
    def _run_feedback(self, target: Structon, act_result: Any, context: ExecutionContext) -> Any:
        """Run feedback phase."""
        context.set("action_result", act_result)
        return self.interpreter.run_phase(target, Phase.FEEDBACK, context)
    
    def _update_tension(self, target: Structon, feedback_result: Any) -> None:
        """Update tension based on feedback."""
        if isinstance(feedback_result, dict):
            if feedback_result.get("success", False):
                target.tension *= 0.5  # Reduce tension on success
            else:
                target.tension = min(1.0, target.tension * 1.1)  # Increase on failure
        else:
            target.tension *= 0.9  # Default: slight reduction
