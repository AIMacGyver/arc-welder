from pathlib import Path

import arc_welder.utils as utils


def test_load_yaml(tmp_path):
    file = Path(__file__).parent / "graphql_schemas_mock.yaml"
    data = utils.load_yaml(file)

    data = utils.load_yaml(file)

    assert data == {
        "targets_for_drug": {
            "query": "{\n  search(queryString: drug, entityNames: target) {\n    hits {\n      id\n      name\n      entity\n    }\n  }\n}\n",
            "question": "What are the targets of vorinostat?",
        },
    }


def test_get_questions():
    data = {
        "targets_for_drug": {
            "question": "What are the targets of vorinostat?",
            "query": "query content",
        },
        "drugs_for_disease": {
            "question": "Find drugs that are used for treating ulcerative colitis",
            "query": "query content",
        },
        "diseases_associated_": {
            "question": "Which diseases are associated with the genes targetted by fasudil?",
            "query": "query content",
        },
    }

    questions = utils.get_questions(data)

    assert questions == [
        "What are the targets of vorinostat?",
        "Find drugs that are used for treating ulcerative colitis",
        "Which diseases are associated with the genes targetted by fasudil?",
    ]


def test_get_query_schema():
    data = {
        "targets_for_drug": {
            "question": "What are the targets of vorinostat?",
            "query": "query content",
        },
        "drugs_for_disease": {
            "question": "Find drugs that are used for treating ulcerative colitis",
            "query": "query content",
        },
        "diseases_associated_": {
            "question": "Which diseases are associated with the genes targetted by fasudil?",
            "query": "query content",
        },
    }

    schema = utils.get_query_schema(
        data,
        "What are the targets of vorinostat?",
    )

    assert schema == "targets_for_drug"
