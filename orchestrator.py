from agents import research_agent, summarizer_agent

def run_agent(agent: str, query: str = "") -> str:
    if agent == "Research":
        return research_agent.run(query)
    elif agent == "Summarizer":
        return summarizer_agent.run(query)
    return "Unknown agent"