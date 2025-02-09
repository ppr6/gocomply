from typing import Dict, Any, List, Callable, Optional, AsyncIterator
from .prompts import (
    CLAUSE_EXTRACTION_PROMPT,
    RISK_CLASSIFICATION_PROMPT,
    COMPLIANCE_REPORT_PROMPT
)
from .parsers import (
    parse_extracted_clauses,
    parse_risk_classification,
    parse_compliance_report
)
from .llm import llm

class ChainStep:
    def __init__(self, 
                 name: str, 
                 prompt_template: str, 
                 output_parser: callable,
                 state_adapter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        self.name = name
        self.prompt_template = prompt_template
        self.output_parser = output_parser
        self.state_adapter = state_adapter or (lambda x: x)

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Transform state for this step if needed
            adapted_state = self.state_adapter(state)
            
            # Format prompt with adapted state
            prompt = self.prompt_template.format(**adapted_state)
            
            # Get LLM response
            response = await llm.complete(prompt)
            
            # Parse and return
            return self.output_parser(response)
        except Exception as e:
            raise Exception(f"Error in step {self.name}: {str(e)}")

class PromptChain:
    def __init__(self, steps: List[ChainStep]):
        self.steps = steps
        self.state = {}

    async def execute_with_updates(self, initial_input: Dict[str, Any]) -> AsyncIterator[tuple[str, Dict[str, Any]]]:
        """Execute chain and yield progress updates with state"""
        self.state = initial_input
        
        total_steps = len(self.steps)
        for i, step in enumerate(self.steps, 1):
            try:
                # Yield progress before step
                progress_msg = self._get_progress_message(step.name, i, total_steps)
                yield progress_msg, self.state

                # Execute step
                step_output = await step.execute(self.state)
                self.state.update(step_output)

                # Yield completion of step
                yield f"Completed: {progress_msg}", self.state

            except Exception as e:
                yield f"Error in {step.name}: {str(e)}", self.state
                raise

    def _get_progress_message(self, step_name: str, current: int, total: int) -> str:
        """Get user-friendly progress message"""
        messages = {
            "clause_extraction": "Analyzing contract and extracting key clauses",
            "risk_classification": "Evaluating compliance risks and regulatory requirements",
            "compliance_report": "Generating comprehensive compliance report"
        }
        base_msg = messages.get(step_name, f"Processing {step_name}")
        return f"Step {current}/{total}: {base_msg}..." 