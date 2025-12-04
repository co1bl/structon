"""
LLM Generator Module

Handles LLM integration for generating and evolving structons.
"""

import json
import os
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        """Generate a response from the LLM."""
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
    
    def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        """Generate using Anthropic API."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        except ImportError:
            return "[Anthropic SDK not installed. Run: pip install anthropic]"
        except Exception as e:
            return f"[Error: {str(e)}]"


class OpenAIProvider(LLMProvider):
    """OpenAI provider."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
    
    def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        """Generate using OpenAI API."""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.choices[0].message.content
        except ImportError:
            return "[OpenAI SDK not installed. Run: pip install openai]"
        except Exception as e:
            return f"[Error: {str(e)}]"


class MockProvider(LLMProvider):
    """Mock provider for testing."""
    
    def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        """Return a mock response."""
        return json.dumps({
            "structure_id": "mock_001",
            "structure_type": "composite",
            "intent": "mock_response",
            "phases": ["sense", "act", "feedback"],
            "tension": 0.5,
            "importance": 0.5,
            "nodes": [],
            "edges": []
        })


class Generator:
    """
    Generates structons using LLM.
    """
    
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider or self._auto_detect_provider()
        self.blueprints: Dict[str, Dict[str, Any]] = {}
        self._load_blueprints()
    
    def _auto_detect_provider(self) -> LLMProvider:
        """Auto-detect available LLM provider."""
        if os.environ.get("ANTHROPIC_API_KEY"):
            return AnthropicProvider()
        elif os.environ.get("OPENAI_API_KEY"):
            return OpenAIProvider()
        else:
            return MockProvider()
    
    def _load_blueprints(self) -> None:
        """Load blueprints from files."""
        blueprint_dir = os.path.join(os.path.dirname(__file__), "..", "..", "blueprints")
        
        if os.path.exists(blueprint_dir):
            for filename in os.listdir(blueprint_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(blueprint_dir, filename)
                    with open(filepath, 'r') as f:
                        blueprint = json.load(f)
                        name = filename.replace(".json", "").replace("_blueprint", "")
                        self.blueprints[name] = blueprint
    
    def generate(
        self,
        task: str,
        blueprint: str = "meta",
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a structon for a task.
        
        Args:
            task: Description of the task
            blueprint: Blueprint name to use
            context: Additional context
        
        Returns:
            Generated structon as dictionary
        """
        blueprint_data = self.blueprints.get(blueprint, self.blueprints.get("meta", {}))
        
        prompt = self._build_generate_prompt(task, blueprint_data, context)
        
        response = self.provider.generate(prompt)
        
        return self._parse_structon(response)
    
    def _build_generate_prompt(
        self,
        task: str,
        blueprint: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> str:
        """Build the generation prompt."""
        from .prompts import GENERATE_PROMPT
        
        atomics = self._get_available_atomics()
        
        return GENERATE_PROMPT.format(
            blueprint=json.dumps(blueprint, indent=2),
            task=task,
            context=json.dumps(context or {}),
            atomics=", ".join(atomics)
        )
    
    def _get_available_atomics(self) -> List[str]:
        """Get list of available atomic functions."""
        try:
            from ..core.atomics import list_atomics
            return list_atomics()
        except ImportError:
            return [
                "get", "set", "merge", "filter", "map", "first", "sort",
                "if", "loop", "branch",
                "load_structon", "save_structon", "query_structons",
                "call_llm", "emit", "log",
                "calculate_tension", "propagate_tension"
            ]
    
    def _parse_structon(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structon."""
        try:
            # Try to extract JSON from response
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Return error structon
        return {
            "structure_id": "error_parse",
            "structure_type": "error",
            "intent": "parse_failed",
            "phases": ["feedback"],
            "tension": 1.0,
            "importance": 1.0,
            "nodes": [],
            "edges": [],
            "error": f"Failed to parse: {response[:200]}"
        }


class Evolver:
    """
    Evolves structons based on feedback.
    """
    
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider or Generator()._auto_detect_provider()
    
    def evolve(
        self,
        structon: Dict[str, Any],
        feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evolve a structon based on feedback.
        
        Args:
            structon: Original structon
            feedback: Feedback from execution
        
        Returns:
            Evolved structon
        """
        from .prompts import EVOLVE_PROMPT
        
        prompt = EVOLVE_PROMPT.format(
            structon=json.dumps(structon, indent=2),
            feedback=json.dumps(feedback, indent=2),
            error=feedback.get("error", "None")
        )
        
        response = self.provider.generate(prompt)
        
        return self._parse_evolved(response, structon)
    
    def _parse_evolved(
        self,
        response: str,
        original: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse evolved structon from response."""
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                evolved = json.loads(json_str)
                
                # Increment version
                metadata = evolved.get("metadata", {})
                metadata["version"] = metadata.get("version", 0) + 1
                metadata["parent_id"] = original.get("structure_id")
                evolved["metadata"] = metadata
                
                return evolved
        except json.JSONDecodeError:
            pass
        
        # Return original with error flag
        original["evolution_error"] = f"Failed to evolve: {response[:200]}"
        return original
