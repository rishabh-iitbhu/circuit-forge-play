"""
Design Heuristics Document Analysis
Utility functions to read and analyze design heuristics documents
"""

import os
import glob
from typing import List, Dict
import streamlit as st

def get_design_documents(component_type: str) -> List[str]:
    """
    Get list of design heuristics documents for a specific component type
    
    Args:
        component_type: 'capacitors', 'inductors', or 'mosfets'
    
    Returns:
        List of document file paths
    """
    try:
        # Get the directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to reach the project root, then into assets
        heuristics_path = os.path.join(current_dir, '..', 'assets', 'design_heuristics', component_type)
        
        if not os.path.exists(heuristics_path):
            return []
        
        # Search for various document types
        doc_patterns = ['*.docx', '*.pdf', '*.txt', '*.md']
        documents = []
        
        for pattern in doc_patterns:
            documents.extend(glob.glob(os.path.join(heuristics_path, pattern)))
        
        return documents
    except Exception as e:
        st.warning(f"Error accessing design documents: {e}")
        return []


def list_all_design_documents() -> Dict[str, List[str]]:
    """
    Get all design heuristics documents organized by component type
    
    Returns:
        Dictionary with component types as keys and document lists as values
    """
    component_types = ['capacitors', 'inductors', 'mosfets']
    all_docs = {}
    
    for comp_type in component_types:
        all_docs[comp_type] = get_design_documents(comp_type)
    
    return all_docs


def get_document_info(file_path: str) -> Dict[str, str]:
    """
    Get basic information about a document file
    
    Args:
        file_path: Path to the document
    
    Returns:
        Dictionary with file information
    """
    try:
        stat = os.stat(file_path)
        return {
            'filename': os.path.basename(file_path),
            'size_kb': round(stat.st_size / 1024, 2),
            'modified': st.session_state.get('file_mod_time', 'Unknown'),
            'extension': os.path.splitext(file_path)[1]
        }
    except Exception as e:
        return {
            'filename': os.path.basename(file_path),
            'size_kb': 0,
            'modified': 'Unknown',
            'extension': os.path.splitext(file_path)[1],
            'error': str(e)
        }


def show_design_documents_info():
    """Display information about available design heuristics documents"""
    st.subheader("📋 Available Design Heuristics Documents")
    
    all_docs = list_all_design_documents()
    
    if not any(all_docs.values()):
        st.info("No design heuristics documents found. Add .docx, .pdf, .txt, or .md files to the respective folders in `assets/design_heuristics/`")
        return
    
    # Create tabs for each component type
    tab1, tab2, tab3 = st.tabs(["💻 MOSFETs", "🔋 Capacitors", "🧲 Inductors"])
    
    with tab1:
        docs = all_docs.get('mosfets', [])
        if docs:
            for doc in docs:
                info = get_document_info(doc)
                st.markdown(f"📄 **{info['filename']}** ({info['size_kb']} KB)")
        else:
            st.info("No MOSFET design documents found in `assets/design_heuristics/mosfets/`")
    
    with tab2:
        docs = all_docs.get('capacitors', [])
        if docs:
            for doc in docs:
                info = get_document_info(doc)
                st.markdown(f"📄 **{info['filename']}** ({info['size_kb']} KB)")
        else:
            st.info("No Capacitor design documents found in `assets/design_heuristics/capacitors/`")
    
    with tab3:
        docs = all_docs.get('inductors', [])
        if docs:
            for doc in docs:
                info = get_document_info(doc)
                st.markdown(f"📄 **{info['filename']}** ({info['size_kb']} KB)")
        else:
            st.info("No Inductor design documents found in `assets/design_heuristics/inductors/`")


def refresh_recommendations_with_heuristics():
    """
    Function to be called when user wants to refresh component recommendations
    based on latest design heuristics documents
    """
    st.info("🔄 Analyzing latest design heuristics documents...")
    
    all_docs = list_all_design_documents()
    total_docs = sum(len(docs) for docs in all_docs.values())
    
    if total_docs == 0:
        st.warning("No design heuristics documents found to analyze.")
        return
    
    # Analyze inductor heuristics specifically
    inductor_analysis = None
    if all_docs.get('inductors'):
        try:
            from lib.document_analyzer import analyze_inductor_heuristics
            inductor_analysis = analyze_inductor_heuristics()
            
            if inductor_analysis['updated_algorithm']:
                st.success("✅ Inductor selection algorithm updated!")
                
                # Show what was found and applied
                st.markdown("### 📋 Applied Inductor Design Heuristics:")
                for rec in inductor_analysis.get('recommendations', []):
                    st.markdown(f"- {rec}")
                
                # Test the updated algorithm with sample parameters
                st.markdown("### 🧪 Testing Updated Algorithm:")
                try:
                    from lib.component_suggestions import suggest_inductors
                    test_suggestions = suggest_inductors(
                        required_inductance_uh=470,  # 470µH test case
                        max_current=2.0,  # 2A test case
                        frequency_hz=65000  # 65kHz test case
                    )
                    
                    if test_suggestions:
                        st.markdown("**Top recommendation with updated heuristics:**")
                        top = test_suggestions[0]
                        st.markdown(f"- **{top.component.part_number}** ({top.component.manufacturer})")
                        st.markdown(f"- Score: {top.score:.1f}")
                        st.markdown(f"- Reasoning: {top.reason}")
                        
                        if top.heuristics_applied:
                            st.markdown("**Applied Heuristics:**")
                            for h in top.heuristics_applied[:3]:
                                st.markdown(f"  - {h}")
                
                except Exception as e:
                    st.error(f"Error testing updated algorithm: {e}")
            else:
                st.warning("⚠️ No specific inductor heuristics could be applied from documents")
                
        except Exception as e:
            st.error(f"Error analyzing inductor heuristics: {e}")
    
    # Show summary of all available documents
    st.markdown("### 📊 Available Design Documents:")
    for comp_type, docs in all_docs.items():
        if docs:
            st.markdown(f"**{comp_type.title()}:** {len(docs)} documents")
            for doc in docs:
                st.markdown(f"  - {os.path.basename(doc)}")
    
    st.markdown("---")
    st.info("💡 **Next Steps:** The updated algorithm will now be used automatically in all circuit calculations. You can also extend this by adding more detailed heuristics documents for capacitors and MOSFETs.")