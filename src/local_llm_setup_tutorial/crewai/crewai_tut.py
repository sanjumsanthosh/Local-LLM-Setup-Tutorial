from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class TeacherCrew():

    @agent
    def teacher(self) -> Agent:
        return Agent(
            config=self.agents_config['teacher'],
            verbose=True
        )
    
    @task
    def teacher_task(self) -> Task:
        return Task(
            config=self.tasks_config['teacher_task'],
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
    
def run():
    inputs = {
        'topic': 'AI LLMs'
    }
    TeacherCrew().crew().kickoff()