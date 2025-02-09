import asyncio
from typing import Dict, Any, Union, AsyncIterator
from src.chain_steps import ChainStep, PromptChain
from src.prompts import (
    CLAUSE_EXTRACTION_PROMPT,
    RISK_CLASSIFICATION_PROMPT,
    COMPLIANCE_REPORT_PROMPT
)
from src.parsers import (
    parse_extracted_clauses,
    parse_risk_classification,
    parse_compliance_report
)
from src.example_contract import EXAMPLE_LOAN_AGREEMENT
from src.utils.document_processor import extract_text_from_document
from src.regulatory_links import REGULATORY_LINKS

async def analyze_contract(input_data: Union[str, tuple[bytes, str]]) -> AsyncIterator[tuple[str, Dict[str, Any]]]:
    """
    Analyze a contract and yield progress updates
    
    Args:
        input_data: Either a string containing contract text,
                   or a tuple of (file_content: bytes, filename: str)
    
    Yields:
        Tuple of (progress_message, current_state)
    """
    # Extract text if input is a document
    if isinstance(input_data, tuple):
        yield "Processing document...", {}
        file_content, filename = input_data
        contract_text = extract_text_from_document(file_content, filename)
    else:
        contract_text = input_data
    
    # Define chain steps
    steps = [
        ChainStep("clause_extraction", CLAUSE_EXTRACTION_PROMPT, parse_extracted_clauses),
        ChainStep(
            "risk_classification",
            RISK_CLASSIFICATION_PROMPT,
            parse_risk_classification,
            state_adapter=lambda state: {
                "clause_text": state["clauses"][0]["text"],
                "clause_category": state["clauses"][0]["category"],
                "regulatory_links": REGULATORY_LINKS
            }
        ),
        ChainStep(
            "compliance_report",
            COMPLIANCE_REPORT_PROMPT,
            parse_compliance_report,
            state_adapter=lambda state: {
                "analyzed_clauses": state
            }
        )
    ]

    # Create and execute chain
    chain = PromptChain(steps)
    async for progress, state in chain.execute_with_updates({"contract_text": contract_text}):
        yield progress, state

if __name__ == "__main__":
    # Example usage
    result = asyncio.run(analyze_contract(EXAMPLE_LOAN_AGREEMENT))
    print(result) 