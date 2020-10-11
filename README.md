# twwr-spoiler-log-bot

A [racetime.gg](https://racetime.gg) chat bot application for automatically 
generating [TWW Randomizer](https://github.com/LagoLunatic/wwrando) seeds in race rooms.

## How to get started

### Requirements

* Python 3.7 or greater.

### Installation

1. Clone the repo
1. Install the package using `pip install -e .` (from the repo's base
   directory).
   
### Usage

Run `randobot <github_token> <category_slug> <client_id> <client_secret>`,
where:

* `<github_token>` is a GitHub personal access token with permission to create Gists.
* `<category_slug>` is the slug of the racetime.gg category the bot should
  operate in, i.e. `twwr`
* `<client_id>` is the OAuth2 client ID for this bot on racetime.gg
* `<client_secret>` is the OAuth2 client secret for this bot on racetime.gg
