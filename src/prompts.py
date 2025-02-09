from src.regulatory_links import REGULATORY_LINKS

CLAUSE_EXTRACTION_PROMPT = """
Analyze the following financial contract and extract key clauses. Focus on clauses related to:
1. Financial obligations
2. Compliance requirements
3. Risk allocation
4. Regulatory reporting

Contract text:
{contract_text}

Provide your analysis as a JSON object with the following structure. Ensure the response is valid JSON:

{{
    "clauses": [
        {{
            "text": "The exact clause text from the contract",
            "category": "financial_obligation",
            "location": "1.1"
        }}
    ]
}}

Categories must be one of: financial_obligation, compliance_requirement, risk_allocation, regulatory_reporting.
Each clause must include its exact text from the contract, appropriate category, and section number.
"""

RISK_CLASSIFICATION_PROMPT = """
Analyze the following contract clause for compliance with the latest Indian financial regulations (RBI, SEBI, PMLA) along with additional regulatory context below:

Regulatory Context:
{regulatory_links}

Clause: {clause_text}
Category: {clause_category}

Consider:
1. Regulatory compliance
2. Financial exposure
3. Operational impact
4. Ambiguity level

Format your response as JSON with:
- risk_level: (HIGH, MEDIUM, LOW)
- regulatory_bodies: List of relevant regulatory bodies
- risk_factors: List of identified risk factors
- recommendations: Suggested improvements
"""

COMPLIANCE_REPORT_PROMPT = """
Generate a compliance report based on the analyzed clauses and their risk classifications:

Analyzed Clauses: {analyzed_clauses}

Format the report with:
1. Executive Summary
2. Risk Assessment
3. Regulatory Compliance Gaps
4. Recommended Actions

Under "Risk Assessment", organize findings into these categories:
### High Risk Findings
(List high-risk items or write "None identified" if no high risks found)

### Medium Risk Findings
(List medium-risk items or write "None identified" if no medium risks found)

### Low Risk Findings
(List low-risk items or write "None identified" if no low risks found)

Write all recommended actions in passive voice (e.g., "The clause should be corrected" instead of "Correct the clause").

Use markdown formatting for better readability.
""" 