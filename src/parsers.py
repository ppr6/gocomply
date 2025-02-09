import json
from typing import Dict, List, Any
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_json_from_text(text: str) -> str:
    """Extract JSON object from text that might contain other content."""
    # First try to find JSON between triple backticks
    json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text)
    if json_match:
        return json_match.group(1)
    
    # If that fails, try to find a JSON object directly
    json_match = re.search(r'(\{[\s\S]*\})', text)
    if json_match:
        return json_match.group(1)
    
    # If all else fails, return the original text
    return text.strip()

def parse_extracted_clauses(response: str) -> Dict[str, List[Dict[str, str]]]:
    try:
        logger.info("Attempting to parse LLM response")
        logger.debug(f"Raw response (length: {len(response)}): {response}")
        
        # Extract JSON from the response
        json_str = extract_json_from_text(response)
        logger.debug(f"Extracted JSON string: {json_str}")
        
        # Parse the JSON
        clauses = json.loads(json_str)
        logger.debug(f"Successfully parsed JSON: {clauses}")
        
        # Validate structure
        if not isinstance(clauses, dict) or "clauses" not in clauses:
            raise ValueError("Response missing 'clauses' key")
        
        return clauses
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {str(e)}")
        logger.error(f"Failed response (length: {len(response)}): {repr(response)}")
        raise ValueError(f"Failed to parse JSON response: {str(e)}")
    except Exception as e:
        logger.error(f"Parsing failed: {str(e)}")
        raise ValueError(f"Failed to parse extracted clauses: {str(e)}")

def parse_risk_classification(response: str) -> Dict[str, Any]:
    try:
        json_str = extract_json_from_text(response)
        classification = json.loads(json_str)
        return {"risk_analysis": classification}
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse risk classification: {str(e)}")

def parse_compliance_report(response: str) -> Dict[str, str]:
    return {"compliance_report": response} 