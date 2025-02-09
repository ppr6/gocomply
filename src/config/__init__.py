# Make src/config a Python package 
from .settings import GROQ_API_KEY, MODEL_NAME, setup_logging
from .regulatory_references import get_regulatory_context, REGULATORY_REFERENCES

__all__ = ['GROQ_API_KEY', 'MODEL_NAME', 'setup_logging', 
           'get_regulatory_context', 'REGULATORY_REFERENCES'] 