import os
from crewai import Agent, LLM
import dotenv
from langchain_openai import ChatOpenAI
from custom_tools import list_tables_tool, tables_schema_tool, execute_sql_tool, check_sql_tool

dotenv.load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY", "")

class CustomAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)

    def sql_developer(self):
        return Agent(
            role="SQL Developer",
            goal="Construct and execute SQL queries based on user requests",
            backstory=( 
                """
                You are an experienced database engineer skilled at creating efficient and complex SQL queries.
                You deeply understand databases and optimization strategies.
                from user {query} identify which columns they are referring to from the database and execute queries according to user requirement to fetch data.
                Only use the provided tools when its needed, dont make your own tools.
                """ 
            ),
            llm=self.llm,
            tools=[list_tables_tool, tables_schema_tool, execute_sql_tool, check_sql_tool], 
            allow_delegation=False,
            verbose=True,
        )

    def data_analyst(self):
        return Agent(
            role="Senior Data Analyst",
            goal="Analyze the data from the SQL developer and provide meaningful insights, explain the insights",
            backstory="You analyze datasets using Python and produce clear, concise insights.",
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
        )

    def report_writer(self):
        return Agent(
            role="Report Writer",
            goal="Summarize the analysis into a short, executive-level report,include the analysed numbers to explain the insights",
            backstory="You create concise reports highlighting the most important findings.",
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
        )

    def data_visualization_agent(self):
        return Agent(
            role="Data Visualization Agent",
            goal="""
                Generate Python code using Plotly to visualize data based on user queries. 
                Your code must be wrapped in triple backticks: ```python ... ``` and produce a 'fig' object.
                """,
            backstory="""
                You are an expert data scientist. You have a local CSV file (already prepared).
                Use Plotly to create a figure (e.g. fig = px.bar(...)). 
                Do not show or save the figure. Just produce the code snippet in triple backticks.""",
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
        )

