import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

class VisualiserTool:
    def __init__(self, df):
        self.df = df

    def visualize_gender_distribution(self):
        """Visualize the distribution of genders in the dataset."""
        gender_col = next((col for col in self.df.columns if col.lower() == 'gender'), None)
        if not gender_col:
            return st.error("No gender column found in the data")
        
        gender_counts = self.df[gender_col].value_counts()
        fig = go.Figure(data=[go.Pie(labels=gender_counts.index, values=gender_counts.values, hole=.3)])
        fig.update_layout(title_text='Gender Distribution', transition_duration=500)
        st.plotly_chart(fig, key="gender_distribution")  # Add a unique key

    def visualize_medical_condition_distribution(self):
        """Visualize the distribution of medical conditions."""
        condition_col = next((col for col in self.df.columns if 'medical condition' in col.lower()), None)
        if not condition_col:
            return st.error("No medical condition column found in the data")
        
        condition_counts = self.df[condition_col].value_counts()
        fig = px.bar(x=condition_counts.index, y=condition_counts.values, labels={'x': 'Medical Condition', 'y': 'Number of Patients'})
        fig.update_layout(title_text='Number of Patients per Medical Condition', transition_duration=500)
        st.plotly_chart(fig, key="medical_condition_distribution")  # Add a unique key

    def visualize_treatment_distribution(self):
        """Visualize the distribution of treatments."""
        treatment_col = next((col for col in self.df.columns if 'treatments' in col.lower()), None)
        if not treatment_col:
            return st.error("No treatments column found in the data")
        
        treatment_counts = self.df[treatment_col].value_counts()
        fig = go.Figure(data=[go.Pie(labels=treatment_counts.index, values=treatment_counts.values, hole=.3)])
        fig.update_layout(title_text='Treatment Distribution', transition_duration=500)
        st.plotly_chart(fig, key="treatment_distribution")  # Add a unique key

    def visualize_treatment_duration(self):
        """Visualize the duration of treatments over time."""
        admit_col = next((col for col in self.df.columns if 'admit date' in col.lower()), None)
        discharge_col = next((col for col in self.df.columns if 'discharge date' in col.lower()), None)
        if not admit_col or not discharge_col:
            return st.error("Admit Date or Discharge Date column not found in the data")
        
        self.df[admit_col] = pd.to_datetime(self.df[admit_col])
        self.df[discharge_col] = pd.to_datetime(self.df[discharge_col])
        self.df['Treatment Duration'] = (self.df[discharge_col] - self.df[admit_col]).dt.days

        # Filter the dataset to show records only for the year 2024
        recent_df = self.df[self.df[admit_col].dt.year == 2024]

        fig = px.line(recent_df, x=admit_col, y='Treatment Duration', labels={admit_col: 'Admit Date', 'Treatment Duration': 'Treatment Duration (days)'})
        fig.update_layout(title_text='Treatment Duration Over Time', transition_duration=500)
        st.plotly_chart(fig, key="treatment_duration")  # Add a unique key

    def visualize_bill_amount_distribution(self):
        """Visualize the distribution of bill amounts."""
        bill_col = next((col for col in self.df.columns if 'bill amount' in col.lower()), None)
        if not bill_col:
            return st.error("No bill amount column found in the data")
        
        fig = px.histogram(self.df, x=bill_col, nbins=20, labels={bill_col: 'Bill Amount'})
        fig.update_layout(title_text='Distribution of Bill Amounts', transition_duration=500)
        st.plotly_chart(fig, key="bill_amount_distribution")  # Add a unique key