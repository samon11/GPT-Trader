# GPT Trader

Code for the Medium article [I Made GPT-4 Trade Options](https://medium.com/ai-advances/options-trading-with-gpt-4-and-python-a-tech-financial-future-8f299462ae41)
---

## Installation

This repo uses [poetry](https://python-poetry.org/) for dependency management. To install the dependencies, run:

```bash
poetry install

# then activate the virtual environment
poetry shell
```

Once the dependencies are installed, you must create a `.env` file at `./tradegpt/.env`. This file should contain the following:

```bash
# ------- OPTIONAL --------
API_KEY=YOUR TDAmeritrade API KEY
REDIRECT_URI=https://localhost:8080
TOKEN_PATH=credentials.json
ACCOUNT_ID=YOUR TDAmeritrade ACCOUNT ID
# --------------------------

OPENAI_KEY=YOUR OPENAI KEY
```

and to run the bot:

```bash
cd tradegpt
python main.py AAPL
```

All runs are logged to `./tradegpt/reports/`.

## Configuration

The most important files for configuration are [main.py](tradegpt/main.py) and [prompt.py](tradegpt/prompt.py). The former is the entrypoint for the bot, and the latter contains the prompt templates for the GPT-3 API.

- `main.py`: Update insights, data sources, model, and prompt selection. For a full list of insights, see [insights/](tradegpt/data/insights/). For a full list of data sources, see [sources/](tradegpt/data/sources/).
- `prompt.py`: Update prompt templates. `main.py` replaces the string `$C` with insights at runtime. 

## Contributing

If you'd like to contribute or have any questions, feel free to open an issue or PR.
