import os
from pathlib import Path
from typing import Tuple

from InstructorEmbedding import INSTRUCTOR
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

import arc_welder.utils as utils

os.environ["TOKENIZERS_PARALLELISM"] = "false"

MAIN_PATH = Path(__file__).resolve().parents[0]
CONFIG_PATHS = {
    "graphql_schemas": MAIN_PATH / "configs/graphql_schemas.yaml",
    "langchain": MAIN_PATH / "configs/langchain.yaml",
    "openai_models": MAIN_PATH / "configs/openai_models.yaml",
    "instructor_model": MAIN_PATH / "configs/instructor_model.yaml",
}

configs = {name: utils.load_yaml(path) for name, path in CONFIG_PATHS.items()}


def similarity_component(user_input: str) -> str:
    """
    Compute the similarity between the user's input and previous questions,
    and return the most similar question.

    Args:
        user_input (str): User input string.

    Returns:
        str: The most similar question to the user input.
    """
    previous_questions = utils.get_questions(configs["graphql_schemas"])
    instruction = configs["instructor_model"]["xl-model"]["instruction"]
    previous_questions = utils.create_instruction_pairs(previous_questions, instruction)

    user_question = utils.create_instruction_pairs([user_input], instruction)

    model = INSTRUCTOR(configs["instructor_model"]["xl-model"]["model_name"])

    embeddings_questions = model.encode(previous_questions)
    embeddings_user = model.encode(user_question)

    similarities = cosine_similarity(embeddings_questions, embeddings_user)

    most_similar_index = similarities.argmax()

    return previous_questions[most_similar_index][1]


def user_input_component() -> tuple[str, str]:
    """
    Get the user input and the corresponding similar schema.

    Returns:
        Tuple[str, str]: User input and similar schema.
    """
    utils.get_openai_api_key()

    user_input = input("How can I help you?\n")

    similar_question = similarity_component(user_input)
    similar_schema = utils.get_query_schema(configs["graphql_schemas"], similar_question)

    return user_input, similar_schema


def llm_component(user_input: str, query_schema: str, verbose: bool = False) -> None:
    """
    Run the langchain tool on the user's input and the corresponding schema.

    Args:
        user_input (str): User input.
        query_schema (str): The corresponding schema.
        verbose (bool, optional): If True, prints detailed output. Defaults to False.

    Returns:
        None
    """
    utils.get_openai_api_key()

    davinci = configs["openai_models"]["davinci"]

    llm = OpenAI(
        model_name=davinci["model_name"],
        temperature=davinci["temperature"],
        max_tokens=davinci["max_tokens"],
        top_p=davinci["top_p"],
        frequency_penalty=davinci["frequency_penalty"],
        presence_penalty=davinci["presence_penalty"],
    )

    tools = load_tools(
        [configs["langchain"]["graphql"]["tool"]],
        graphql_endpoint=configs["langchain"]["graphql"]["graphql_endpoint"],
        llm=llm,
    )

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=verbose,
    )

    suffix = f"{user_input} {configs['langchain']['suffix']}"

    result = agent.run(suffix + configs["graphql_schemas"][query_schema]["query"])

    print(result)


def pipeline(verbose: bool = False) -> None:
    """
    Run the complete pipeline of getting the user input, finding the similar schema,
    and using langchain tools to complete GraphQL queries.

    Returns:
        None
    """
    user_input, similar_schema = user_input_component()

    llm_component(user_input, similar_schema, verbose=verbose)
