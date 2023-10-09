# Getting Started

* Change smaple.env file to .env file and make appropriate modifications.

```bash
pip install pipenv
pipenv install
pipenv run gunicorn --bind IP:PORT run:app
```