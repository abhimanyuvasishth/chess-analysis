# chess-analysis

## Installation

### Create a virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Install the packages

```bash
pip install -r requirements.txt
```

## Setup

Create a `.env` file with the following API keys:

```bash
CHESS_USERNAME=your-username
```

Create 2 directories:

1. `data`
2. `assets`

## Running the code

```bash
python download_chess_games.py
```
