from crewai import Task
from textwrap import dedent


class CustomTasks:
    def extract_data(self, agent):
        return Task(
            description=dedent("""
                User Query: {query}
                Write any necessary SQL, run it, and return the result.
                only use the provided tools if its needed.
                """),
            expected_output="Raw data from the SQL query as text or structured data from the whole data table.",
            agent=agent,
        )

    def analyze_data(self, agent, extract_task):
        return Task(
            description=dedent("""
                Analyze the data retrieved from the SQL Developer.
                Provide a detailed explanation for {query}.
                """),
            expected_output="Detailed analysis text",
            agent=agent,
            context=[extract_task],
        )

    def write_report(self, agent, analyze_task):
        return Task(
            description=dedent("""
                Write a detailed executive level summary of the report based on the analysis, 
                provide explanation and insights of the numbers found in the analysis.
                """),
            expected_output="A short bullet-point or paragraph summarizing the analysis in markdown format.",
            agent=agent,
            context=[analyze_task],
        )

    def generate_visualization(self, agent, viz_prompt, df):
        return Task(
            description=dedent(f"""
                We have a CSV file named 'temp.csv' with columns: {', '.join(df.columns)}.
                Below are the first few rows:
                {df.head(5).to_csv(index=False)}

                User wants a Plotly figure: "{viz_prompt}"

                Produce the code in triple backticks.
                """),
            expected_output="A snippet of valid Plotly code wrapped in triple backticks that creates a 'fig' object.",
            agent=agent,
        )
