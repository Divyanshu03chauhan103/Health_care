import streamlit as st
from navbar import navbar
from styles import load_styles
from footer import footer
import pandas as pd
import os
import sys
import tempfile

# Set Page Configuration
st.set_page_config(
    page_title="MediMind AI | Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add the directory containing the tools to Python path
tools_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Tools")
if tools_dir not in sys.path:
    sys.path.append(tools_dir)

# Add parent directory to path to find the tools
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import custom tools - with fallbacks for testing
try:
    from Frontend.csv_reader_tool import CSVReaderTool
    from Frontend.visualiser_tool import VisualiserTool
    tools_imported = True
except ImportError as e:
    st.sidebar.warning(f"Warning: Could not import visualization tools. Some features may be limited. Error: {e}")
    tools_imported = False

# Load custom styles
load_styles()

# Display navbar
navbar()

# Initialize session state
if 'hospital_data' not in st.session_state:
    st.session_state.hospital_data = None
if 'csv_path' not in st.session_state:
    st.session_state.csv_path = None
if 'visualizations' not in st.session_state:
    st.session_state.visualizations = None

# Hero Section
st.markdown(
    """
    <div class="hero" id="home">
        <div class="hero-content">
            <h1>
                <span style="color: #2D8CFF;">Medi</span><span style="color: #34C759;">Mind</span> AI
            </h1>
            <h2 style="margin-top: 0; color: #4A5568; font-size: 1.5rem; font-weight: 500;">Patient Record Management System</h2>
            <p>Efficiently manage patient records and gain valuable insights through advanced data visualization.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Function to visualize data using the VisualiserTool
# Function to visualize data using the VisualiserTool
def visualize_patient_data(df):
    """Generate visualizations using the VisualiserTool."""
    if not tools_imported:
        # Fallback visualization if tools are not available
        visualizations = {
            "total_patients": len(df),
            "data_preview": df.head()
        }
        
        # Add additional simple visualizations
        gender_col = next((col for col in df.columns if col.lower() == 'gender'), None)
        if gender_col:
            visualizations["gender_chart"] = df[gender_col].value_counts()
            
        diagnosis_col = next((col for col in df.columns if 'medical condition' in col.lower()), None)
        if diagnosis_col:
            visualizations["diagnosis_chart"] = df[diagnosis_col].value_counts().head(5)
            
        # Add a simple financial analysis if bill data exists
        bill_col = next((col for col in df.columns if 'bill' in col.lower() or 'amount' in col.lower()), None)
        if bill_col:
            visualizations["avg_bill"] = df[bill_col].mean()
            visualizations["total_revenue"] = df[bill_col].sum()
            
        return visualizations
    else:
        # Use the updated VisualiserTool for more advanced visualizations
        visualizer = VisualiserTool(df)
        
        # Generate visualizations
        st.subheader("Gender Distribution")
        visualizer.visualize_gender_distribution()
        
        st.subheader("Medical Condition Distribution")
        visualizer.visualize_medical_condition_distribution()
        
        st.subheader("Treatment Distribution")
        visualizer.visualize_treatment_distribution()
        
        st.subheader("Treatment Duration Over Time")
        visualizer.visualize_treatment_duration()
        
        st.subheader("Bill Amount Distribution")
        visualizer.visualize_bill_amount_distribution()

# Function to add a patient record to the CSV
def add_patient_record(csv_path, record_data):
    try:
        # Read the existing CSV file
        df = pd.read_csv(csv_path)
        
        # Create a DataFrame from the record
        new_record = pd.DataFrame([record_data], columns=df.columns)
        
        # Append the new record
        df = pd.concat([df, new_record], ignore_index=True)
        
        # Save the updated DataFrame
        df.to_csv(csv_path, index=False)
        
        # Update the session state with new data
        st.session_state.hospital_data = df
        
        return True, "Patient record added successfully!"
    except Exception as e:
        return False, f"Error adding patient record: {str(e)}"

# Main content area divided into two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Patient Records Section
    st.markdown(
        """
        <div class="card" id="patient-records">
            <div class="section-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
                <h2 style="margin: 0 0 0 10px;">Patient Records</h2>
            </div>
            <p>Manage patient records and visualize healthcare data for better insights.</p>
        """,
        unsafe_allow_html=True
    )
    
    # Upload existing patient data
    uploaded_file = st.file_uploader("Upload patient records (CSV)", type="csv", key="csv_upload")
    
    # Handle file upload
    if uploaded_file:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name
            
        # Store path in session state
        st.session_state.csv_path = temp_path
        
        try:
            # Load and display data
            df = pd.read_csv(temp_path)
            st.session_state.hospital_data = df
            
            st.success("Patient records loaded successfully!")
            
            # Display data preview
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Process and visualize the data
            if st.button("Generate Visualizations"):
                with st.spinner("Analyzing patient data..."):
                    visualize_patient_data(df)
                    st.success("Analysis complete!")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    # Display form to add a new patient record
    st.subheader("Add New Patient Record")
    
    # Only show the form if hospital data is loaded
    if st.session_state.hospital_data is not None:
        df = st.session_state.hospital_data
        columns = df.columns.tolist()
        
        # Create a dynamic form based on the columns in the CSV
        form_data = {}
        
        # Split columns into two for better layout
        mid_point = len(columns) // 2
        col_a, col_b = st.columns(2)
        
        with col_a:
            for col in columns[:mid_point]:
                # Customize input type based on column name
                if 'date' in col.lower():
                    form_data[col] = st.date_input(col)
                elif 'amount' in col.lower() or 'bill' in col.lower() or 'cost' in col.lower():
                    form_data[col] = st.number_input(col, min_value=0.0, step=100.0)
                elif 'gender' in col.lower():
                    form_data[col] = st.selectbox(col, ["Male", "Female", "Other"])
                else:
                    form_data[col] = st.text_input(col)
        
        with col_b:
            for col in columns[mid_point:]:
                # Customize input type based on column name
                if 'date' in col.lower():
                    form_data[col] = st.date_input(col)
                elif 'amount' in col.lower() or 'bill' in col.lower() or 'cost' in col.lower():
                    form_data[col] = st.number_input(col, min_value=0.0, step=100.0)
                elif 'gender' in col.lower():
                    form_data[col] = st.selectbox(col, ["Male", "Female", "Other"])
                else:
                    form_data[col] = st.text_input(col)
        
        # Convert date objects to string format
        for key, value in form_data.items():
            if hasattr(value, 'strftime'):  # Check if it's a date object
                form_data[key] = value.strftime("%Y-%m-%d")
        
        # Add button to submit the form
        if st.button("Add Record"):
            # Create a list of values in the order of columns
            record_values = [form_data[col] for col in columns]
    
            # Add the record to the CSV
            success, message = add_patient_record(st.session_state.csv_path, record_values)
    
            if success:
                st.success(message)
        
                # Force refresh of visualizations
                with st.spinner("Updating visualizations..."):
                    visualize_patient_data(st.session_state.hospital_data)
                    # Use rerun to refresh the page with new data
                    st.experimental_rerun()
            else:
                st.error(message)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Visualizations Section
    st.markdown(
        """
        <div class="card" id="visualizations">
            <div class="section-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
                <h2 style="margin: 0 0 0 10px;">Data Visualizations</h2>
            </div>
            <p>Visual insights from patient records to aid in healthcare decision making.</p>
        """,
        unsafe_allow_html=True
    )
    
    # Display visualizations if available
    if st.session_state.hospital_data is not None:
        visualize_patient_data(st.session_state.hospital_data)
    else:
        st.info("Upload patient data and generate visualizations to see insights here.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Statistics
    if st.session_state.hospital_data is not None:
        df = st.session_state.hospital_data
        
        st.markdown(
            """
            <div class="card" id="statistics">
                <div class="section-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                        <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                    </svg>
                    <h2 style="margin: 0 0 0 10px;">Quick Statistics</h2>
                </div>
            """,
            unsafe_allow_html=True
        )
        
        # Display quick stats about the data
        st.metric("Total Records", len(df))
        
        # Display unique counts for categorical columns
        for col in df.columns:
            if df[col].dtype == 'object' and len(df[col].unique()) < 10:
                st.write(f"Unique {col}: {len(df[col].unique())}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Contact section
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
    </div>
    """,
    unsafe_allow_html=True
)

# Clean up temporary files when the app is closed
def cleanup():
    if st.session_state.csv_path and os.path.exists(st.session_state.csv_path):
        os.unlink(st.session_state.csv_path)

import atexit
atexit.register(cleanup)

# Display footer
footer()