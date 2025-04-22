# AI Agent for Data Analysis

## Overview
This project leverages multi-agent collaboration to automate SQL query execution, data analysis, reporting, and visualization. It uses OpenAI's LLMs with the CrewAI framework to facilitate seamless interaction between SQL developers, data analysts, report writers, and data visualization agents.

## Features
- **SQL Query Execution:** Automatically generate and run SQL queries on an SQLite database.
- **Data Analysis:** Extract insights from queried data.
- **Report Generation:** Summarize analysis results into an executive-level report.
- **Data Visualization:** Create Plotly visualizations based on user queries.
- **Streamlit UI:** Interactive interface for users to upload datasets and request analysis/visualizations.

---

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- `pip`
- `virtualenv`

### Step 1: Clone the Repository
```sh
git clone <repository-url>
cd <repository-folder>
```

### Step 2: Set Up Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

### Step 5: Run the Streamlit Application
```sh
streamlit run streamlit_app.py
```

---

## Project Structure
```
├── agents.py         # Defines AI agents for SQL execution, analysis, reporting, and visualization
├── tasks.py          # Defines tasks assigned to agents
├── custom_tools.py    # Custom tools for SQL execution and validation
├── crew.py           # Orchestrates agents and tasks into a CrewAI workflow
├── streamlit_app.py   # Streamlit-based user interface
├── requirements.txt  # Required Python dependencies
├── README.md         # Project documentation
├── .env              # Environment variables (API keys)
```

### **agents.py**
Defines different AI agents:
- **SQL Developer**: Executes SQL queries.
- **Data Analyst**: Analyzes retrieved data.
- **Report Writer**: Summarizes insights.
- **Visualization Agent**: Generates Plotly charts.

### **tasks.py**
Defines the structured tasks performed by each agent.

### **custom_tools.py**
Implements tools for SQL database operations:
- List tables
- Retrieve schema
- Execute queries
- Validate SQL queries

### **crew.py**
Manages the coordination of agents and task execution using CrewAI.

### **streamlit_app.py**
Provides a web interface for:
- Uploading datasets
- Querying the AI assistant
- Viewing generated reports
- Visualizing data

---

## Usage
1. **Upload a CSV file** through the Streamlit interface.
2. **Enter a natural language query** (e.g., "Show the average salary by department").
3. **Generate an analysis report** to obtain insights.
4. **Request a visualization** by describing the desired chart (e.g., "Create a bar chart for sales over time").

---

## Contributing
Feel free to fork the repository and submit pull requests to improve the project.


