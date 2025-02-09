# Latest regulatory guidelines and references
REGULATORY_REFERENCES = {
    "RBI": {
        "draft_notifications": "https://www.rbi.org.in/scripts/DraftNotificationsGuildelines.aspx",
        "description": "Latest RBI draft notifications and guidelines"
    },
    "SEBI": {
        "depository_regulations": "https://www.sebi.gov.in/legal/regulations/aug-2024/securities-and-exchange-board-of-india-depositories-and-participants-regulations-2018-last-amended-on-august-29-2024-_86353.html",
        "capital_disclosure": "https://www.sebi.gov.in/legal/regulations/may-2024/securities-and-exchange-board-of-india-issue-of-capital-and-disclosure-requirements-regulations-2018-last-amended-on-may-17-2024-_80421.html",
        "description": "Latest SEBI regulations on depositories, capital issuance, and disclosure requirements"
    },
    "PMLA": {
        "amendments_2023": "https://indiaforensic.com/pmla-amendmends-2023/",
        "reporting_obligations": "https://www.india-briefing.com/news/india-prevention-of-money-laundering-rules-2023-key-provisions-new-reporting-obligations-27347.html/",
        "description": "Latest PMLA amendments and reporting obligations"
    },
    "BUDGET": {
        "fy_2025_26": "https://www.india-briefing.com/news/indias-union-budget-fy-2025-26-key-takeaways",
        "reforms": "https://www.india-briefing.com/news/indias-union-budget-2025-26-highlights-reforms-to-drive-economic-growth-manufacturing-consumption-36011.html/",
        "description": "Latest Union Budget provisions and reforms"
    }
}

def get_regulatory_context():
    """Generate regulatory context for LLM prompts"""
    context = "Latest Regulatory References:\n\n"
    
    for body, refs in REGULATORY_REFERENCES.items():
        context += f"{body}:\n"
        context += f"{refs['description']}\n"
        for name, url in refs.items():
            if name != 'description':
                context += f"- {name.replace('_', ' ').title()}: {url}\n"
        context += "\n"
    
    return context 