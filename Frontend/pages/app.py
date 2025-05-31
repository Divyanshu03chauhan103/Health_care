import streamlit as st
from navbar import navbar
from styles import load_styles
from footer import footer
# import pandas as pd
# from crewai import Agent, Task, Crew
# from repl_tool import PythonREPLTool, BaseTool
# from csv_reader_tool import CSVReaderTool
# from visualiser_tool import VisualiserTool
from medical_search_tool import medical_search_tool
from query_faiss import query_faiss
import os
# import tempfile
import PyPDF2
import io
import re
from typing import Dict, List
# import json

# Set Page Configuration
st.set_page_config(
    page_title="MediMind AI | Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom styles
load_styles()

# Display navbar
navbar()

# Initialize session state variables if they don't exist
if 'hospital_data' not in st.session_state:
    st.session_state.hospital_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'csv_path' not in st.session_state:
    st.session_state.csv_path = None
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

# PDF Processing Functions
def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_medical_values(text: str) -> Dict:
    """Extract common medical values from text using regex patterns"""
    values = {}
    
    # Blood Pressure patterns
    bp_patterns = [
        r'(?:blood pressure|bp|systolic|diastolic)[\s:]*(\d{2,3})[/\-](\d{2,3})',
        r'(\d{2,3})[/\-](\d{2,3})[\s]*(?:mmhg|mm hg)',
    ]
    
    # Glucose patterns
    glucose_patterns = [
        r'(?:glucose|sugar|fbs|rbs)[\s:]*(\d+\.?\d*)[\s]*(?:mg/dl|mmol/l|mg%)',
        r'(?:fasting glucose|random glucose)[\s:]*(\d+\.?\d*)',
    ]
    
    # Cholesterol patterns
    cholesterol_patterns = [
        r'(?:cholesterol|chol)[\s:]*(\d+\.?\d*)[\s]*(?:mg/dl|mmol/l)',
        r'(?:total cholesterol|tc)[\s:]*(\d+\.?\d*)',
    ]
    
    # Hemoglobin patterns
    hb_patterns = [
        r'(?:hemoglobin|hb|haemoglobin)[\s:]*(\d+\.?\d*)[\s]*(?:g/dl|gm/dl)',
    ]
    
    # Temperature patterns
    temp_patterns = [
        r'(?:temperature|temp|fever)[\s:]*(\d+\.?\d*)[\s]*(?:°f|°c|f|c)',
    ]
    
    # Heart Rate patterns
    hr_patterns = [
        r'(?:heart rate|pulse|hr)[\s:]*(\d+)[\s]*(?:bpm|beats|/min)',
    ]
    
    text_lower = text.lower()
    
    # Extract Blood Pressure
    for pattern in bp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            values['blood_pressure'] = f"{match.group(1)}/{match.group(2)} mmHg"
            break
    
    # Extract Glucose
    for pattern in glucose_patterns:
        match = re.search(pattern, text_lower)
        if match:
            values['glucose'] = f"{match.group(1)} mg/dL"
            break
    
    # Extract Cholesterol
    for pattern in cholesterol_patterns:
        match = re.search(pattern, text_lower)
        if match:
            values['cholesterol'] = f"{match.group(1)} mg/dL"
            break
    
    # Extract Hemoglobin
    for pattern in hb_patterns:
        match = re.search(pattern, text_lower)
        if match:
            values['hemoglobin'] = f"{match.group(1)} g/dL"
            break
    
    # Extract Temperature
    for pattern in temp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            temp_val = float(match.group(1))
            # Convert Fahrenheit to Celsius if needed
            if temp_val > 50:  # Likely Fahrenheit
                temp_celsius = (temp_val - 32) * 5/9
                values['temperature'] = f"{temp_celsius:.1f}°C ({temp_val}°F)"
            else:
                values['temperature'] = f"{temp_val}°C"
            break
    
    # Extract Heart Rate
    for pattern in hr_patterns:
        match = re.search(pattern, text_lower)
        if match:
            values['heart_rate'] = f"{match.group(1)} bpm"
            break
    
    return values

def interpret_medical_values(values: Dict) -> Dict:
    """Interpret extracted medical values and provide recommendations"""
    findings = []
    recommendations = []
    
    # Blood Pressure interpretation
    if 'blood_pressure' in values:
        bp_text = values['blood_pressure']
        systolic = int(bp_text.split('/')[0])
        diastolic = int(bp_text.split('/')[1].split()[0])
        
        if systolic < 90 or diastolic < 60:
            findings.append(f"Blood pressure: {bp_text} (Low)")
            recommendations.append("Monitor for symptoms of hypotension")
        elif systolic <= 120 and diastolic <= 80:
            findings.append(f"Blood pressure: {bp_text} (Normal)")
        elif systolic <= 139 or diastolic <= 89:
            findings.append(f"Blood pressure: {bp_text} (Pre-hypertension)")
            recommendations.append("Lifestyle modifications recommended")
        else:
            findings.append(f"Blood pressure: {bp_text} (High)")
            recommendations.append("Consult physician for hypertension management")
    
    # Glucose interpretation
    if 'glucose' in values:
        glucose_text = values['glucose']
        glucose_val = float(glucose_text.split()[0])
        
        if glucose_val < 70:
            findings.append(f"Glucose: {glucose_text} (Low)")
            recommendations.append("Monitor for hypoglycemia symptoms")
        elif glucose_val <= 99:
            findings.append(f"Glucose: {glucose_text} (Normal)")
        elif glucose_val <= 125:
            findings.append(f"Glucose: {glucose_text} (Pre-diabetic)")
            recommendations.append("Dietary modifications and regular monitoring")
        else:
            findings.append(f"Glucose: {glucose_text} (High)")
            recommendations.append("Diabetes screening and management needed")
    
    # Cholesterol interpretation
    if 'cholesterol' in values:
        chol_text = values['cholesterol']
        chol_val = float(chol_text.split()[0])
        
        if chol_val < 200:
            findings.append(f"Cholesterol: {chol_text} (Normal)")
        elif chol_val <= 239:
            findings.append(f"Cholesterol: {chol_text} (Borderline high)")
            recommendations.append("Dietary changes and regular exercise")
        else:
            findings.append(f"Cholesterol: {chol_text} (High)")
            recommendations.append("Lipid management and cardiac risk assessment")
    
    # Hemoglobin interpretation
    if 'hemoglobin' in values:
        hb_text = values['hemoglobin']
        hb_val = float(hb_text.split()[0])
        
        if hb_val < 12:  # General threshold
            findings.append(f"Hemoglobin: {hb_text} (Low - Anemia)")
            recommendations.append("Iron supplementation and dietary counseling")
        elif hb_val <= 15:
            findings.append(f"Hemoglobin: {hb_text} (Normal)")
        else:
            findings.append(f"Hemoglobin: {hb_text} (High)")
            recommendations.append("Further evaluation for polycythemia")
    
    # Temperature interpretation
    if 'temperature' in values:
        temp_text = values['temperature']
        temp_val = float(temp_text.split('°')[0])
        
        if temp_val < 36:
            findings.append(f"Temperature: {temp_text} (Low)")
            recommendations.append("Monitor for hypothermia")
        elif temp_val <= 37.5:
            findings.append(f"Temperature: {temp_text} (Normal)")
        else:
            findings.append(f"Temperature: {temp_text} (Fever)")
            recommendations.append("Fever management and infection screening")
    
    # Heart Rate interpretation
    if 'heart_rate' in values:
        hr_text = values['heart_rate']
        hr_val = int(hr_text.split()[0])
        
        if hr_val < 60:
            findings.append(f"Heart rate: {hr_text} (Bradycardia)")
            recommendations.append("Cardiac evaluation recommended")
        elif hr_val <= 100:
            findings.append(f"Heart rate: {hr_text} (Normal)")
        else:
            findings.append(f"Heart rate: {hr_text} (Tachycardia)")
            recommendations.append("Cardiac assessment and monitoring")
    
    return {
        'findings': findings,
        'recommendations': recommendations
    }

def analyze_medical_report(pdf_text: str) -> Dict:
    """Comprehensive analysis of medical report"""
    # Extract medical values
    extracted_values = extract_medical_values(pdf_text)
    
    # Get interpretations
    interpretations = interpret_medical_values(extracted_values)
    
    # Use FAISS for additional context
    faiss_results = query_faiss(pdf_text[:500])  # First 500 chars for context
    
    # Use medical search for any specific conditions mentioned
    conditions_found = []
    condition_patterns = [
        r'(?:diagnosis|diagnosed with|condition)[\s:]*([a-zA-Z\s]+)',
        r'(?:hypertension|diabetes|anemia|fever|infection|pneumonia|asthma)',
    ]
    
    for pattern in condition_patterns:
        matches = re.findall(pattern, pdf_text.lower())
        conditions_found.extend(matches)
    
    additional_info = []
    for condition in conditions_found[:2]:  # Limit to 2 conditions
        if condition.strip():
            search_result = medical_search_tool.func(condition.strip())
            if search_result and "No reliable information found" not in search_result:
                additional_info.append(f"About {condition}: {search_result[:200]}...")
    
    return {
        'extracted_values': extracted_values,
        'findings': interpretations['findings'],
        'recommendations': interpretations['recommendations'],
        'faiss_context': faiss_results[:2],  # Top 2 relevant results
        'additional_info': additional_info,
        'raw_text_preview': pdf_text[:300] + "..." if len(pdf_text) > 300 else pdf_text
    }

# Initialize hospital manager and tools (keeping existing functionality)
# @st.cache_resource
# def initialize_tools(csv_path):
#     python_repl_tool = PythonREPLTool()
#     csv_reader_tool = CSVReaderTool(csv_path)
    
#     class PatientRecordManagerTool(BaseTool):
#         def __init__(self, csv_path):
#             super().__init__(
#                 name="Patient Record Manager Tool",
#                 description="A tool to manage patient records in the CSV dataset."
#             )
#             self.csv_path = csv_path
        
#         def execute(self, record):
#             df = pd.read_csv(self.csv_path)
#             df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
#             df.to_csv(self.csv_path, index=False)
#             return "Patient record added successfully."
    
#     patient_record_manager_tool = PatientRecordManagerTool(csv_path)
#     return python_repl_tool, csv_reader_tool, patient_record_manager_tool

# # Function to create hospital manager agent (keeping existing)
# def create_hospital_manager(tools):
#     return Agent(
#         role="Hospital Manager",
#         goal="Manage hospital data by reading the database, analyzing patterns, and generating insights.",
#         backstory="You are an AI specialized in processing and understanding hospital data.",
#         tools=tools,
#         verbose=True
#     )

# Hero Section (keeping existing design)
st.markdown(
    """
    <div class="hero" id="home">
        <div class="hero-content">
            <h1>
                <span style="color: #2D8CFF;">Medi</span><span style="color: #34C759;">Mind</span> AI
            </h1>
            <h2 style="margin-top: 0; color: #4A5568; font-size: 1.5rem; font-weight: 500;">Transforming Healthcare with Artificial Intelligence</h2>
            <p>Experience the future of healthcare with our AI-powered platform. Get instant insights from patient reports, manage hospital operations efficiently, and access reliable medical information with ease.</p>
            <div style="display: flex; justify-content: center; gap: 15px;">
                <a class="btn" href="#diagnostics">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                    </svg>
                    Start Diagnosis
                </a>
                <a class="btn btn-outline" href="#operations">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;">
                        <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                        <line x1="8" y1="21" x2="16" y2="21"></line>
                        <line x1="12" y1="17" x2="12" y2="21"></line>
                    </svg>
                    Hospital Operations
                </a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Create two columns for main content
col1, col2 = st.columns([2, 1])

with col1:
    # Enhanced Diagnostics Section with Dynamic Analysis
    st.markdown(
        """
        <div class="card" id="diagnostics">
            <div class="section-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                </svg>
                <h2 style="margin: 0 0 0 10px;">Upload Patient Reports</h2>
            </div>
            <p>Upload your medical reports and our AI will analyze them for personalized insights and recommendations.</p>
        """,
        unsafe_allow_html=True
    )
    
    uploaded_file = st.file_uploader("Drag and drop your patient report (PDF)", type="pdf", key="pdf")
    
    if uploaded_file:
        # Process the uploaded PDF
        with st.spinner("Analyzing your medical report..."):
            # Extract text from PDF
            pdf_text = extract_text_from_pdf(uploaded_file)
            
            if pdf_text:
                # Analyze the medical report
                analysis_result = analyze_medical_report(pdf_text)
                st.session_state.last_analysis = analysis_result
                
                # Display success message
                st.markdown(
                    """
                    <div class="success-message">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34C759" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                        </svg>
                        Report uploaded and analyzed successfully!
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Display Dynamic Analysis Results
                st.markdown(
                    """
                    <div style="margin-top: 20px;">
                        <h3 style="color: grey; font-size: 1.2rem; font-weight: 600;">AI Analysis Results:</h3>
                    """,
                    unsafe_allow_html=True
                )
                
                # Key Findings
                if analysis_result['findings']:
                    findings_html = "<br>".join([
                    f'<span style="color: black;">• {finding}</span>' 
                    for finding in analysis_result['findings']
                ])

                    st.markdown(
                        f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px;">
                            <span style="color: #d3d3d3; font-weight: 500;">Key Findings:</span><br>
                            {findings_html}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Recommendations
                if analysis_result['recommendations']:
                    recommendations_html = "<br>".join([
                    f'<span style="color: black;">• {rec}</span>'
                    for rec in analysis_result['recommendations']
                ])
                    st.markdown(
                        f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px;">
                            <span style="color: #d3d3d3;; font-weight: 500;">Recommendations:</span><br>
                            {recommendations_html}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Additional Medical Information
                if analysis_result['additional_info']:
                    additional_html = "<br><br>".join([
                    f'<span style="color: black;">{info}</span>' 
                    for info in analysis_result['additional_info']
                ])

                    st.markdown(
                        f"""
                        <div style="background-color: #f8f9ff; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px;">
                            <span style="color: #d3d3d3;; font-weight: 500;">Additional Medical Information:</span><br>
                            {additional_html}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Raw Values Extracted (for debugging/transparency)
                if analysis_result['extracted_values']:
                    with st.expander("📊 Extracted Medical Values"):
                        st.json(analysis_result['extracted_values'])
                
                # Text Preview (for debugging)
                with st.expander("📄 Document Preview"):
                    st.text_area("Extracted Text (Preview)", analysis_result['raw_text_preview'], height=150, disabled=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            else:
                st.error("Could not extract text from the PDF. Please ensure the file is not corrupted and contains readable text.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Enhanced Search Medical Information Section
    st.markdown(
        """
        <div class="card" id="search">
            <div class="section-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <h2 style="margin: 0 0 0 10px;">Medical Information</h2>
            </div>
            <p>Search for reliable information about medical conditions, treatments, and procedures.</p>
        """,
        unsafe_allow_html=True
    )
    
    search_query = st.text_input("Search medical topics", placeholder="e.g., diabetes, hypertension", key="search")
    search_button = st.button("Search", key="search_button")
    
    if search_query and search_button:
        with st.spinner("Searching medical databases..."):
            # Use the medical search tool
            search_result = medical_search_tool.func(search_query)
            
            # Also query FAISS for additional context
            faiss_results = query_faiss(search_query)
            
            st.markdown(
                f"""
                <div style="margin-top: 20px;">
                    <h3 style="color: black; font-size: 1.2rem; font-weight: 600;">Results for "{search_query}":</h3>
                """,
                unsafe_allow_html=True
            )
            
            # Display web search results
            if search_result and "No reliable information found" not in search_result:
                st.markdown(
                    f"""
                    <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px;">
                        <h4 style="color:#d3d3d3;; margin-top: 0; font-size: 1rem;">Medical Information</h4>
                        <p style="color: var(--text-dark); margin: 0;">{search_result[:500]}{'...' if len(search_result) > 500 else ''}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Display FAISS results as related information
            if faiss_results:
                related_info = "<br><br>".join([f"• {result[:200]}..." for result in faiss_results[:2]])
                st.markdown(
                    f"""
                    <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <h4 style="color: #d3d3d3;; margin-top: 0; font-size: 1rem;">Related Information</h4>
                        <p style="color: var(--text-dark); margin: 0;">{related_info}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis Summary (if available)
    if st.session_state.last_analysis:
        st.markdown(
            """
            <div class="card" id="summary">
                <div class="section-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="9" y1="9" x2="15" y2="9"></line>
                        <line x1="9" y1="15" x2="15" y2="15"></line>
                    </svg>
                    <h2 style="margin: 0 0 0 10px;">Latest Analysis</h2>
                </div>
            """,
            unsafe_allow_html=True
        )
        
        analysis = st.session_state.last_analysis
        st.write(f"**Findings:** {len(analysis['findings'])} items identified")
        st.write(f"**Recommendations:** {len(analysis['recommendations'])} suggestions")
        st.write(f"**Values Extracted:** {len(analysis['extracted_values'])} parameters")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Data Statistics Section (keeping existing functionality)
    if st.session_state.hospital_data is not None:
        st.markdown(
            """
            <div class="card" id="statistics">
                <div class="section-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                    </svg>
                    <h2 style="margin: 0 0 0 10px;">Data Statistics</h2>
                </div>
            """,
            unsafe_allow_html=True
        )
        
        df = st.session_state.hospital_data
        st.write(f"Total Records: {len(df)}")
        
        try:
            if 'Gender' in df.columns or 'gender' in df.columns:
                gender_col = 'Gender' if 'Gender' in df.columns else 'gender'
                gender_counts = df[gender_col].value_counts()
                st.write("Gender Distribution:")
                st.bar_chart(gender_counts)
            
            if 'Diagnosis' in df.columns or 'diagnosis' in df.columns:
                diagnosis_col = 'Diagnosis' if 'Diagnosis' in df.columns else 'diagnosis'
                top_diagnoses = df[diagnosis_col].value_counts().head(5)
                st.write("Top Diagnoses:")
                st.bar_chart(top_diagnoses)
        except Exception as e:
            st.error(f"Error generating statistics: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Contact (keeping existing)
    st.markdown(
        """
        <div class="card" id="contact">
            <div class="section-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
                <h2 style="margin: 0 0 0 10px;">Contact Us - </h2>
                <h4>9823123139</h4>
            </div>
            <p>Have questions? Reach out to our support team for assistance.</p>
        """,
        unsafe_allow_html=True
    )

# Clean up temporary files when the app is closed (keeping existing)
def cleanup():
    if st.session_state.csv_path and os.path.exists(st.session_state.csv_path):
        os.unlink(st.session_state.csv_path)

import atexit
atexit.register(cleanup)

# Display footer
footer()