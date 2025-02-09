import streamlit as st
import asyncio
from datetime import datetime
import base64
from io import StringIO
from src.main import analyze_contract
from src.config import setup_logging

def export_report():
    """Export the report as a formatted markdown file"""
    report = st.session_state.report
    
    # Add header and timestamp
    formatted_report = f"""# Contract Analysis Report
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{report}
"""
    return formatted_report.encode('utf-8')

async def run_analysis(input_data, progress_placeholder):
    """Run analysis and update progress in Streamlit"""
    try:
        async for progress, state in analyze_contract(input_data):
            progress_placeholder.markdown(progress)
            
            if state and 'compliance_report' in state:
                st.session_state.report = state['compliance_report']
                st.session_state.analysis_complete = True
                
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        raise

def main():
    # Initialize session states
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
        st.session_state.report = None
    if 'is_analyzing' not in st.session_state:
        st.session_state.is_analyzing = False

    if st.session_state.analysis_complete and st.session_state.report:
        # Display only the report
        st.markdown(st.session_state.report)
        
        # Create a small container for the buttons
        button_col1, button_col2, _ = st.columns([0.1, 0.1, 0.8])
        with button_col1:
            st.download_button(
                label="📥 Download",
                data=export_report(),
                file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with button_col2:
            if st.button("Start New Analysis", use_container_width=True):  # Make button fill the column
                st.session_state.analysis_complete = False
                st.session_state.report = None
                st.rerun()
    else:
        # Show the input interface
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
        
        # Create a container for button and progress
        button_container = st.container()
        
        with button_container:
            if st.session_state.is_analyzing:
                st.button(
                    "Analyzing...", 
                    disabled=True,
                    type="primary"
                )
                progress_placeholder = st.empty()
                if uploaded_file:
                    file_content = uploaded_file.read()
                    input_data = (file_content, uploaded_file.name)
                else:
                    input_data = text_input
                
                asyncio.run(run_analysis(input_data, progress_placeholder))
                st.session_state.is_analyzing = False
                st.rerun()
            else:
                if st.button("Analyze Contract", type="primary"):
                    if not uploaded_file and not text_input:
                        st.warning("Please either upload a file or enter contract text.")
                    else:
                        st.session_state.is_analyzing = True
                        st.rerun()

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