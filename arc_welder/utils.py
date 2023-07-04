import os
from typing import Any, Dict, List

import yaml


def get_openai_api_key() -> None:
    """
    Get OpenAI API Key from environment variables. If not found, prompt the user to enter.

    Returns:
        None
    """
    if not os.environ.get("OPENAI_API_KEY"):
        openai_api_key = input("Please Enter Your OpenAI API Key: ")
        os.environ["OPENAI_API_KEY"] = openai_api_key


def create_instruction_pairs(questions: list[str], instruction: str) -> list[list[str]]:
    """
    Create instruction pairs for a given set of questions and a single instruction.

    Args:
        questions (List[str]): List of questions.
        instruction (str): Single instruction.

    Returns:
        List[List[str]]: List of [instruction, question] pairs.
    """
    return [[instruction, q] for q in questions]


def load_yaml(file: str) -> dict[str, Any]:
    """
    Load a YAML file and return its contents as a python dictionary.

    Args:
        file (str): File path.

    Returns:
        Dict[str, Any]: Parsed YAML file contents as a dictionary.
    """
    with open(file) as f:
        return yaml.safe_load(f)


def get_questions(data: dict[str, Any], yaml_key: str = "question") -> list[str]:
    """
    Extracts questions from the given data based on a provided yaml_key.

    Args:
        data (Dict[str, Any]): Data dictionary.
        yaml_key (str, optional): Key to fetch questions. Defaults to "question".

    Returns:
        List[str]: List of questions.
    """
    return [v[yaml_key] for v in data.values() if yaml_key in v]


def get_query_schema(data: dict[str, Any], question: str, yaml_key: str = "question") -> str:
    """
    Get the GraphQL Query schema for a given question in the data.

    Args:
        data (Dict[str, Any]): Data dictionary.
        question (str): Question to fetch schema for.
        yaml_key (str, optional): Key to match question. Defaults to "question".

    Returns:
        str: Schema for the question.
    """
    for k, v in data.items():
        if v[yaml_key] == question:
            return k
