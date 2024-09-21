from gpt_researcher import GPTResearcher

async def trial_run(config_path=None):
    query = "why is Nvidia stock going up?"
    researcher = GPTResearcher(query=query, report_type="research_report", config_path=config_path)
    # Conduct research on the given query
    research_result = await researcher.conduct_research()
    # Write the report
    report = await researcher.write_report()

def run(config_path=None):
    import asyncio
    asyncio.run(trial_run(config_path))