import asyncio
import argparse
from pathlib import Path
from src.main import analyze_contract
from src.example_contract import EXAMPLE_LOAN_AGREEMENT
from src.config import setup_logging

async def main(debug: bool = False, file_path: str = None, text_input: str = None):
    setup_logging(debug_mode=debug)
    
    if file_path:
        # Read file content and pass as tuple with filename
        file_path = Path(file_path)
        with open(file_path, 'rb') as f:
            file_content = f.read()
        contract_input = (file_content, file_path.name)
    else:
        # Use text input or example contract
        contract_input = text_input if text_input else EXAMPLE_LOAN_AGREEMENT
    
    print("\nAnalyzing contract...")
    final_state = None
    async for progress, state in analyze_contract(contract_input):
        print(progress)
        final_state = state
    
    if final_state and 'compliance_report' in final_state:
        print("\nFinal Report:")
        print(final_state['compliance_report'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze financial contracts for compliance')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--file', type=str, help='Path to contract document file')
    parser.add_argument('--text', type=str, help='Contract text to analyze')
    args = parser.parse_args()
    
    asyncio.run(main(debug=args.debug, file_path=args.file, text_input=args.text)) 