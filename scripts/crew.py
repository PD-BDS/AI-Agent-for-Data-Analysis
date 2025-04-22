from crewai import Crew, Process
from agents import CustomAgents
from tasks import CustomTasks

class CustomCrew:
    def __init__(self, query, df=None, visualization=False):
        self.query = query
        self.df = df
        self.visualization = visualization

    def run(self):
        agents = CustomAgents()
        tasks = CustomTasks()

        if self.visualization:
            viz_agent = agents.data_visualization_agent()
            viz_task = tasks.generate_visualization(viz_agent, self.query, self.df)

            crew = Crew(
                agents=[viz_agent],
                tasks=[viz_task],
                process=Process.sequential,
                verbose=True,
            )
            return crew.kickoff()

        sql_dev = agents.sql_developer()
        data_analyst = agents.data_analyst()
        report_writer = agents.report_writer()

        extract_task = tasks.extract_data(sql_dev)
        analyze_task = tasks.analyze_data(data_analyst, extract_task)
        write_task = tasks.write_report(report_writer, analyze_task)

        crew = Crew(
            agents=[sql_dev, data_analyst, report_writer],
            tasks=[extract_task, analyze_task, write_task],
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff(inputs={"query": self.query})
