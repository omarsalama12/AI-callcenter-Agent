"""
Agno Orchestrator — the brain coordinator for one client.
Manages the agent team: RAG agent, Action agent, Escalation agent.
"""
from agno.agent import Agent
from agno.team import Team


def build_team(client_id: str, config: dict) -> Team:
    """
    Builds the agent team for a specific client.
    Each agent has a scoped role and limited permissions.
    """
    rag_agent = Agent(
        name="knowledge_agent",
        description="Retrieves information from the client knowledge base.",
        instructions=[
            "You only retrieve factual information from the knowledge base.",
            "Never guess. If you don't know, say so.",
            f"You serve client: {client_id}"
        ]
    )

    action_agent = Agent(
        name="action_agent",
        description="Executes tasks on client systems via MCP tools.",
        instructions=[
            "Only execute actions that are in the allowed_actions list.",
            "Always confirm the action result before reporting to the user.",
            f"You serve client: {client_id}"
        ]
    )

    escalation_agent = Agent(
        name="escalation_agent",
        description="Handles cases that need a human supervisor.",
        instructions=[
            "Escalate when: customer anger score > 0.8, legal complaints, or unknown issues.",
            "Be empathetic and assure the customer a human will help shortly."
        ]
    )

    return Team(
        name=f"bpo_team_{client_id}",
        agents=[rag_agent, action_agent, escalation_agent],
        instructions=[
            "You are a customer service team.",
            "Route the request to the correct agent.",
            "Never reveal internal system details to the customer."
        ]
    )
