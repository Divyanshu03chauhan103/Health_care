# HealthCareSystem

An AI-powered healthcare system that leverages multiple specialized agents to provide medical diagnostics, information retrieval, and hospital data management using Google's Gemini LLM and CrewAI framework.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)


## 🔍 Overview

HealthCareSystem is an advanced medical assistance platform that combines AI agents, large language models, and specialized tools to provide comprehensive healthcare support. The system uses Retrieval-Augmented Generation (RAG) to analyze medical documents, provide preliminary diagnoses, retrieve trusted medical information, and manage hospital data.

This project demonstrates the application of AI in healthcare, focusing on improving diagnostic processes, information retrieval, and data management through a multi-agent system architecture.

## ✨ Features

### AI-Powered Medical Diagnostics
- Extract medical insights from PDFs using Retrieval-Augmented Generation (RAG)
- Provide preliminary diagnoses based on medical documents
- Leverage Google Gemini LLM for advanced natural language understanding

### Multi-Agent Healthcare System
- **Master Agent**: Orchestrates the system and delegates tasks
- **Diagnostics Agent**: Analyzes medical PDFs and provides preliminary diagnoses
- **Search Agent**: Retrieves additional medical information from trusted online sources
- **Hospital Management Agent**: Manages patient records and visualizes insights

### Medical Data Processing
- CSV data processing for hospital records
- FAISS vector database integration for efficient medical information retrieval
- Tools for querying medical information from trusted sources

### Frontend Interface
- Web-based interface for interacting with the healthcare system
- Visualization tools for medical data
- Python REPL tool for advanced interactions

## 🏗️ System Architecture

### Agent Structure

#### Master Agent (Manager Agent)
- **Role**: Central orchestrator of the MediMind system
- **Goal**: Assign tasks to other agents and retrieve information for users
- Coordinates between different specialized agents

#### Diagnostics Agent
- **Role**: Medical diagnostics specialist
- **Goal**: Provide preliminary diagnoses based on medical PDFs
- Uses RAG (Retrieval-Augmented Generation) to extract insights from medical documents

#### Search Agent
- **Role**: Medical information retrieval specialist
- **Goal**: Retrieve additional medical information from trusted online sources
- Specialized in searching the internet for reliable medical data

#### Hospital Management Agent
- **Role**: Hospital data management
- **Goal**: Manage patient records and hospital data, and visualize insights
- Processes and analyzes hospital records

### Tools and Components
- **RAGTool1.py**: Main RAG implementation for medical document processing
- **diagnostic_agent.py**: Implementation of the Diagnostics Agent
- **hospital_crew.py/hospital_crew1.py**: Implementation of the agent crew system
- **master_agent.py**: Implementation of the Master Agent
- **hospital_manager_agent.py**: Implementation of the Hospital Management Agent
- **Frontend/appFrontend**: Web interface components
- **Tools**: Directory containing specialized tools for the system
- **faiss_index**: FAISS vector database for efficient information retrieval
- **Data**: Directory containing medical data files

## 📋 Requirements

### Core Dependencies
- Python 3.x
- CrewAI framework for agent orchestration
- Google Generative AI (Gemini) for LLM capabilities
- Pandas for data processing
- FAISS for vector database operations
- dotenv for environment variable management

### API Keys
- Google Gemini API Key (stored in .env file)

### Data Requirements
- Medical PDFs for diagnostics
- Hospital records CSV files (example: hospital_records_2021_2024_with_bills.csv)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/annwhocodes/HealthCareSystem.git
   cd HealthCareSystem
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install crewai langchain-core google-generativeai pandas faiss-cpu python-dotenv
   # Additional dependencies may be required based on specific usage
   ```

4. **Set up environment variables**
   - Create a .env file in the root directory
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Prepare data directories**
   - Ensure the Data directory contains necessary medical data files
   - Set up the faiss_index directory for vector database operations

## 💻 Usage

### Basic Usage

1. **Run the master agent for a complete healthcare system experience**
   ```bash
   python master_agent.py
   ```

2. **For specific diagnostic capabilities only**
   ```bash
   python diagnostic_agent.py
   ```

3. **For hospital management features**
   ```bash
   python hospital_manager_agent.py
   ```

### Using the Web Interface

1. **Start the web server**
   ```bash
   # Command to start the web interface
   cd appFrontend
   python app.py
   ```

2. **Access the web interface**
   - Open a browser and navigate to `http://localhost:5000` (or the specified port)
   - Use the interface to interact with the healthcare system

## 📝 Examples

### Medical Diagnosis from PDF

```python
from diagnostic_agent import handle_query

# Process a medical PDF and get diagnostics
response = handle_query("Analyze the symptoms in this medical report")
print(response)
```

### Medical Information Search

```python
from master_agent import search_agent

# Search for medical information
result = search_agent.process("What are the latest treatments for type 2 diabetes?")
print(result)
```

### Hospital Data Analysis

```python
import pandas as pd
from hospital_manager_agent import process_hospital_data

# Load and process hospital data
df = pd.read_csv("Data/hospital_records_2021_2024_with_bills.csv")
insights = process_hospital_data(df)
print(insights)
```

## 🤝 Contributing

Contributions to the HealthCareSystem project are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## ⚠️ Disclaimer

This system is designed for preliminary assistance and should not replace professional medical advice. Always consult with qualified healthcare professionals for medical diagnoses and treatment.
