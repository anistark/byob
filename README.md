# BYOB - Build Your Own Blockchain

## Setup

1. Install virtualenv or venv and activate it.
2. Install pipenv. (Not necessary though, makes it easier to manage python environments). If on Mac OsX, install via `brew install pipenv`.

```
$ pip install pipenv
```

3. Specify pipenv to use the current environment. `pipenv --three`

4. Install requirements.

```
$ pipenv install
```

## Run:

(Default port is `8000`)
* Node 1: `pipenv run python blockchain.py`
* Node 2: `pipenv run python blockchain.py -p 8001`
* Node 3: `pipenv run python blockchain.py -p 8002`
