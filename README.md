# Arc-Welder

Arc-Welder is a Python application that takes a natural language instruction or question and returns the appropriate response using the [Open Targets](https://www.opentargets.org/) API. The application uses an [Instructor model](https://instructor-embedding.github.io/) to map the user's question to a previous question, which is used to identify the appropriate GraphQL schema for use with [LangChain GraphQL tool](https://python.langchain.com/docs/modules/agents/tools/integrations/graphql).

This library is named after the Arc Welder gadget MacGyver created in Season 1 Episode 6 titled [Trumbo's World](https://www.imdb.com/title/tt0638810/)

This repo builds on the ideas from Onuralp Soylemez's (@cx0) repo: https://github.com/cx0/chatGPT-for-genetics

Arc-Welder was developed with Python 3.11.0 and uses the [Poetry](https://python-poetry.org/) Python project management tool. Please note that you need an OpenAI API Key to use Arc-Welder.

## Supported Instructions

Currently, Arc-Welder supports the following types of questions and instructions:

- "What are the targets of vorinostat?"
- "Find drugs that are used for treating ulcerative colitis"
- "Which diseases are associated with the genes targeted by fasudil?"

## Installation

Before you begin, ensure you have Python 3.11.0 installed on your machine.

1. Clone this repository:

   ```bash
   git clone https://github.com/rannand84/arc-welder.git
   ```

2. Navigate to the project directory:

   ```bash
   cd arc-welder
   ```

3. Install [Poetry](https://python-poetry.org/docs/):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

4. Install the project dependencies:

   ```bash
   poetry install
   ```

5. Export OpenAI API Key as an environment variable:

   ```bash
   export OPENAI_API_KEY=yourapikey
   ```

Replace `yourapikey` with your actual OpenAI API Key.

## Usage

You can run Arc-Welder using the following command:

```bash
poetry run python main.py run_arc_welder
```

If you want to run Arc-Welder in verbose mode, add the `--verbose` flag:

```bash
poetry run python main.py run_arc_welder --verbose
```

Example useage and output
```bash
❯ poetry run python main.py run-arc-welder
Running arc-welder...
How can I help you?
What are the targets of vorinostat?
load INSTRUCTOR_Transformer
max_seq_length  512
- HDAC3
- HDAC1
- HDAC2
- HDAC6
```

If you want to learn more about the support schemas please refer to `arc_welder/configs/graphql_schemas.yaml`.

To change the OpenAI model or adjust the LLM parameters please refer to `arc_welder/configs/openai_models.yaml`.


## Contact

If you have any questions, issues, or feedback, feel free to open an issue on GitHub or contact the maintainers.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## TODO:
- [ ] Remove INSTRUCTOR print statements from output
- [ ] Add 2 step query support for associated disease pathways
- [ ] Add additional insturction and question support mapped to GraphQL schemas
- [ ] Add command line support to pass directions and select schemas directly
- [ ] Refactor and modularize `pipelines.py`
- [ ] Increase test coverage
