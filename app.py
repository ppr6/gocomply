import streamlit as st
import asyncio
from src.main import analyze_contract
from src.config import setup_logging

async def run_analysis(input_data):
    """Run analysis and update progress in Streamlit"""
    progress_placeholder = st.empty()
    report_placeholder = st.empty()
    
    try:
        async for progress, state in analyze_contract(input_data):
            # Update progress message
            progress_placeholder.info(progress)
            
            # If we have a report, show it
            if state and 'compliance_report' in state:
                report_placeholder.markdown(state['compliance_report'])
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        raise

def main():
    st.title("🎯 GoComply")
    st.markdown("""
    ### AI-Powered Financial Contract Compliance Analysis
    Ensure your contracts comply with the latest Indian financial regulations. 
    Simply upload your document or paste the contract text below.
    """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload contract document (PDF, Word, or text file)", 
        type=['pdf', 'docx', 'txt']
    )
    
    # Text input
    text_input = st.text_area(
        "Or paste contract text here",
        height=300,
        help="Enter the contract text to analyze"
    )
    
    # Analysis button
    if st.button("Analyze Contract", type="primary"):
        if not uploaded_file and not text_input:
            st.warning("Please either upload a file or enter contract text.")
            return
            
        with st.spinner("Initializing analysis..."):
            if uploaded_file:
                # Handle uploaded file
                file_content = uploaded_file.read()
                input_data = (file_content, uploaded_file.name)
            else:
                # Use text input
                input_data = text_input
            
            # Run analysis
            asyncio.run(run_analysis(input_data))

if __name__ == "__main__":
    # Set up page config
    st.set_page_config(
        page_title="GoComply",
        page_icon="✓",  # Checkmark as logo
        layout="wide"
    )
    
    # Initialize logging
    setup_logging(debug_mode=False)
    
    main() 