import streamlit as st
import pandas as pd
import sqlite3
import os
from crew import CustomCrew
import statsmodels
from langchain_community.utilities.sql_database import SQLDatabase
from custom_tools import extract_code_block

# Page config
st.set_page_config(layout="wide")
st.title("AI Agent For Data Analysis")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV for analysis", type="csv")
if not uploaded_file:
    st.info("Please upload a CSV file to begin.")
    st.stop()

# Read CSV
df = pd.read_csv(uploaded_file)
st.subheader("Preview of Uploaded Data")
st.dataframe(df.head())

# Capitalize columns for consistency
df.columns = [col.capitalize() for col in df.columns]
# Database file
db_file = "temp_db.sqlite"

# Function to initialize the database safely
def init_database():
    if os.path.isfile(db_file):
        os.remove(db_file)  # Ensure old DB is removed to prevent locking issues

    conn = sqlite3.connect(db_file, check_same_thread=False)
    try:
        df.to_sql(name="data_table", con=conn, if_exists="replace", index=False)
    finally:
        conn.close()  # Always close the connection after initializing the DB

if "db_initialized" not in st.session_state:
    st.session_state["db_initialized"] = False

if not st.session_state["db_initialized"]:
    init_database()
    st.session_state["db_initialized"] = True
    st.success("Database created from uploaded CSV.")

database_uri = f"sqlite:///{db_file}"
db = SQLDatabase.from_uri(database_uri)

# Ask the Agent
st.subheader("Ask The Agent About The Dataset")
user_query = st.text_input("Example: 'Show the average of a numeric column'", "")

# Generate Report
if st.button("Generate Report"):
    if not user_query.strip():
        st.warning("Please enter a query.")
        st.stop()

    with st.spinner("Running the multi-agent pipeline..."):
        try:
            custom_crew = CustomCrew(user_query, df=df)  # Pass the DataFrame here
            result = custom_crew.run()
            st.session_state["report_result"] = result.raw or str(result)  # Store the report result in session state
            st.success("Analysis Complete!")
        except Exception as e:
            st.error(f"Error: {e}")

# Display the generated report if it exists
if "report_result" in st.session_state:
    st.subheader("Analysis Report")
    st.markdown(st.session_state["report_result"])

# Data Visualization Section
st.subheader("Visualize the Data")
viz_prompt = st.text_area(
    "Write your instructions. Example:\n'Please create a bar chart of average Score by Subject using the data'"
)

# Inside the "Generate Plot" button block:
if st.button("Generate Plot"):
    if not viz_prompt.strip():
        st.warning("Please enter a visualization prompt.")
        st.stop()

    # Save the DataFrame as a temporary CSV for the agent's reference
    csv_path = "temp.csv"
    df.to_csv(csv_path, index=False)

    with st.spinner("Generating visualization..."):
        try:
            custom_crew = CustomCrew(viz_prompt, df=df, visualization=True)  # Set visualization to True
            crew_output = custom_crew.run()
            fig_code = extract_code_block(crew_output.raw)  # Using the updated extract_code_block function
            if fig_code:
                try:
                    # Execute the code and create the Plotly figure
                    local_vars = {}
                    exec(fig_code, {}, local_vars)  # Execute and store the output in local_vars
                    fig = local_vars.get('fig')  # Get the figure object from the local variables

                    if fig:
                        st.session_state["fig_result"] = fig  # Store the plot in session state
                        st.success("Plot generated successfully!")
                    else:
                        st.error("No valid figure object was created.")
                except Exception as e:
                    st.error(f"Error generating plot: {e}")
        except Exception as e:
            st.error(f"Error generating visualization: {e}")

# Display the generated plot if it exists
if "fig_result" in st.session_state:
    st.plotly_chart(st.session_state["fig_result"])
