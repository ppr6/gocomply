import groq
from .config.settings import GROQ_API_KEY, MODEL_NAME
import logging

logger = logging.getLogger(__name__)

SYSTEM_MESSAGE = """You are an expert financial compliance analyst with extensive experience in Indian regulatory frameworks. Your expertise includes:

1. Deep knowledge of Indian financial regulations and regulatory bodies:
   - Reserve Bank of India (RBI) guidelines and circulars
   - Securities and Exchange Board of India (SEBI) regulations
   - Prevention of Money Laundering Act (PMLA) requirements
   - Insurance Regulatory and Development Authority of India (IRDAI) rules

2. Expertise in:
   - Banking and financial services compliance
   - Risk assessment and mitigation
   - Anti-Money Laundering (AML) requirements
   - Know Your Customer (KYC) norms
   - Foreign Exchange Management Act (FEMA) regulations
   - Corporate governance requirements

3. Skills in:
   - Contract analysis and risk assessment
   - Regulatory impact analysis
   - Compliance gap identification
   - Remediation planning
   - Risk-based approach to compliance

Your responses should be:
- Precise and technically accurate
- Referenced to specific regulations where applicable
- Risk-focused and practical
- Clear in identifying compliance gaps
- Actionable in recommendations

When analyzing contracts or clauses:
1. Always cite specific regulatory provisions
2. Identify potential compliance risks
3. Suggest practical remediation steps
4. Consider cross-regulatory impacts
5. Evaluate both direct and indirect compliance implications"""

class LLMClient:
    def __init__(self):
        self.client = groq.Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME

    async def complete(self, prompt: str) -> str:
        try:
            logger.info("Sending request to Groq API")
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2048
            )
            response = completion.choices[0].message.content
            logger.info("Received response from Groq API")
            logger.debug(f"Raw response: {response}")
            return response
        except Exception as e:
            logger.error(f"LLM completion failed: {str(e)}")
            raise Exception(f"LLM completion failed: {str(e)}")

llm = LLMClient() 