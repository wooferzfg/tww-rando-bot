# tww-rando-bot

[![Build Status](https://github.com/wooferzfg/tww-rando-bot/workflows/CI/badge.svg)](https://github.com/wooferzfg/tww-rando-bot/actions)

A [racetime.gg](https://racetime.gg) chat bot application for automatically 
generating [TWW Randomizer](https://github.com/LagoLunatic/wwrando) seeds in race rooms.

## How to get started

### Requirements

* Docker

### Installation

1. Clone the repo: `git clone --recursive https://github.com/wooferzfg/tww-rando-bot.git`
2. Build the Docker image: `docker compose build`

### Usage

1. Set up environment variables:
```bash
export GITHUB_TOKEN=... # a GitHub personal access token with permission to create Gists
export CATEGORY_SLUG=... # the slug of the racetime.gg category the bot should operate in (e.g. `twwr`)
export CLIENT_ID=... # the OAuth2 client ID for this bot on racetime.gg
export CLIENT_SECRET=... # the OAuth2 client secret for this bot on racetime.gg
```
2. Run `docker compose up tww_rando_bot` to start the bot.

### Running tests
```bash
docker compose run --rm tww_rando_bot python -m unittest discover -s randobot/tests -p 'test_*.py'
```

### Running generator API
First, start the API server:
```bash
docker compose up generator_api
```

Then you can view the API docs at http://localhost:8000/docs.