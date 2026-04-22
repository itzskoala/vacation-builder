from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool

from vacation_builder.tools.serper_tools import (
    GoogleFlightsTool,
    GoogleHotelsTool,
    GoogleImagesTool,
    GoogleEventsTool,
)
from vacation_builder.push import PushNotificationTool

#annotations
agents: list[BaseAgent] 
tasks: list[Task]

@CrewBase
class VacationBuilder():
    """VacationBuilder crew"""

    @agent
    def trip_input_resolver(self) -> Agent:
        return Agent(
            config=self.agents_config['trip_input_resolver'],  # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def plane_ticket_research(self) -> Agent:
        return Agent(
            config=self.agents_config['plane_ticket_research'],  # type: ignore[index]
            verbose=True,
            tools=[GoogleFlightsTool(), SerperDevTool()],
        )

    @agent
    def financial_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_advisor'],  # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def activities_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['activities_planner'],  # type: ignore[index]
            verbose=True,
            tools=[GoogleEventsTool(), SerperDevTool()],
        )

    @agent
    def accommodations_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['accommodations_finder'],  # type: ignore[index]
            verbose=True,
            tools=[GoogleHotelsTool(), SerperDevTool()],
        )

    @agent
    def photographer(self) -> Agent:
        return Agent(
            config=self.agents_config['photographer'],  # type: ignore[index]
            verbose=True,
            tools=[GoogleImagesTool()],
        )

    @agent
    def vacation_compiler(self) -> Agent:
        return Agent(
            config=self.agents_config['vacation_compiler'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def trip_storyteller(self) -> Agent:
        return Agent(
            config=self.agents_config['trip_storyteller'],  # type: ignore[index]
            verbose=True,
            tools=[],
        )

    # Tasks

    @task
    def resolve_inputs_task(self) -> Task:
        return Task(
            config=self.tasks_config['resolve_inputs_task'],  # type: ignore[index]
        )

    @task
    def flight_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['flight_research_task'],  # type: ignore[index]
        )

    @task
    def budget_task(self) -> Task:
        return Task(
            config=self.tasks_config['budget_task'],  # type: ignore[index]
        )

    @task
    def activities_task(self) -> Task:
        return Task(
            config=self.tasks_config['activities_task'],  # type: ignore[index]
        )

    @task
    def accommodations_task(self) -> Task:
        return Task(
            config=self.tasks_config['accommodations_task'],  # type: ignore[index]
        )

    @task
    def photo_curation_task(self) -> Task:
        return Task(
            config=self.tasks_config['photo_curation_task'],  # type: ignore[index]
        )

    @task
    def final_package_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_package_task'],  # type: ignore[index]
        )

    @task
    def storytelling_task(self) -> Task:
        return Task(
            config=self.tasks_config['storytelling_task'],  # type: ignore[index]
        )

    # Crew
    @crew
    def crew(self) -> Crew:
        """Creates the VacationBuilder crew"""
        return Crew(
            agents=self.agents,   # auto-collected via @agent decorators
            tasks=self.tasks,     # auto-collected via @task decorators
            process=Process.sequential,
            verbose=True,
        )
