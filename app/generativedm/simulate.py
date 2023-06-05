"""Simulation Engine."""
import json
import logging

import networkx as nx

from generativedm.agent import Agent
from generativedm.llm_engine import LLMEngine
from generativedm.locations import Locations
from generativedm.pkg_utils.text_generation import summarize_simulation

logger = logging.getLogger(__name__)


def simulate(
    config_file: str,
    simulation_days: int = 10,
    use_openai: bool = False,
    model_engine: str = "declare-lab/flan-alpaca-xl",
):
    """Simulate NPCs.

    Args:
        config_file (str): Path to the configuration file for the world initialization.
        simulation_days (int, optional): Number of days to simulate. Defaults to 10.
        use_openai (bool, optional): Whether to use OpenAI or not. Defaults to False.
        model_engine (str, optional): Hugging Face text generation model name. Defaults to "declare-lab/flan-alpaca-xl".
    """
    # Set default value for prompt_meta if not defined elsewhere
    prompt_meta = "### Instruction:\n{}\n### Response:"

    # Initialize global time and logging variables
    global_time = 0

    log_locations = True
    log_actions = True
    log_plans = True
    log_ratings = True
    log_memories = True

    llm_engine = LLMEngine(use_openai=use_openai, model_engine=model_engine)

    # Start simulation loop
    whole_simulation_output = ""

    # Load town areas and people from JSON file
    logger.info(f"Loading config file: {config_file}")
    with open(config_file, "r") as f:
        town_data = json.load(f)

    town_people = town_data["town_people"]
    town_areas = town_data["town_areas"]

    # Create world_graph
    logger.info("Creating world graph...")
    world_graph = nx.Graph()
    last_town_area = None
    for town_area in town_areas.keys():
        world_graph.add_node(town_area)
        world_graph.add_edge(town_area, town_area)  # Add an edge to itself
        if last_town_area is not None:
            world_graph.add_edge(town_area, last_town_area)
        last_town_area = town_area

    # Add the edge between the first and the last town areas to complete the cycle
    world_graph.add_edge(list(town_areas.keys())[0], last_town_area)

    # Initialize agents and locations
    logger.info("Initializing agents and locations...")
    agents = []
    locations = Locations()
    for name, description in town_people.items():
        starting_location = description["starting_location"]
        agents.append(
            Agent(
                name,
                description["description"],
                starting_location,
                world_graph,
                llm_engine,
            )
        )

    for name, description in town_areas.items():  # noqa
        locations.add_location(name, description)

    for simulation_day in range(simulation_days):
        # log_output for one simulation_day
        log_output = ""

        log_output += f"====================== simulation_day {simulation_day} ======================\n"
        if log_locations:
            log_output += (
                f"=== LOCATIONS AT START OF simulation_day {simulation_day} ===\n"
            )
            log_output += str(locations) + "\n"
            logger.info(
                f"=== LOCATIONS AT START OF simulation_day {simulation_day} ==="
            )
            logger.info(
                [
                    f"{i}: {str(location)}\n"
                    for i, location in enumerate(locations.locations)
                ]
            )

        # Plan actions for each agent
        for agent in agents:
            agent.plan(global_time, prompt_meta)
            if log_plans:
                log_output += f"{agent.name} plans: {agent.plans}\n"
                logger.info(f"{agent.name} plans: {agent.plans}")

        # Execute planned actions and update memories
        for agent in agents:
            # Execute action
            action = agent.execute_action(
                agents,
                locations.get_location(agent.location),
                global_time,
                town_areas,
                prompt_meta,
            )
            if log_actions:
                log_output += f"{agent.name} action: {action}\n"
                logger.info(f"{agent.name} action: {action}")

            # Update memories
            for other_agent in agents:
                if other_agent != agent:
                    memory = (
                        f"[Time: {global_time}. Person: {agent.name}. Memory: {action}]"
                    )
                    other_agent.memories.append(memory)
                    if log_memories:
                        log_output += f"{other_agent.name} remembers: {memory}\n"
                        logger.info(f"{other_agent.name} remembers: {memory}")

                # Compress and rate memories for each agent
            for agent in agents:
                agent.compress_memories(global_time)
                agent.rate_memories(locations, global_time, prompt_meta)
                if log_ratings:
                    log_output += (
                        f"{agent.name} memory ratings: {agent.memory_ratings}\n"
                    )
                    logger.info(f"{agent.name} memory ratings: {agent.memory_ratings}")

        # Rate locations and determine where agents will go next
        for agent in agents:
            place_ratings = agent.rate_locations(locations, global_time, prompt_meta)
            if log_ratings:
                log_output += (
                    f"=== UPDATED LOCATION RATINGS {global_time} FOR {agent.name}===\n"
                )
                log_output += f"{agent.name} location ratings: {place_ratings}\n"
                logger.info(
                    f"=== UPDATED LOCATION RATINGS {global_time} FOR {agent.name}===\n"
                )
                logger.info(f"{agent.name} location ratings: {place_ratings}\n")

            old_location = agent.location

            new_location_name = place_ratings[0][0]
            agent.move(new_location_name)

            if log_locations:
                log_output += (
                    f"=== UPDATED LOCATIONS AT TIME {global_time} FOR {agent.name}===\n"
                )
                log_output += (
                    f"{agent.name} moved from {old_location} to {new_location_name}\n"
                )
                logger.info(
                    f"=== UPDATED LOCATIONS AT TIME {global_time} FOR {agent.name}===\n"
                )
                logger.info(
                    f"{agent.name} moved from {old_location} to {new_location_name}\n"
                )

        logger.info(
            f"----------------------- SUMMARY FOR simulation_day {simulation_day} -----------------------"
        )

        logger.info(summarize_simulation(log_output=log_output))

        whole_simulation_output += log_output

        # Increment time
        global_time += 1
