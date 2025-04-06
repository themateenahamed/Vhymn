#!/usr/bin/env bash

# Force Python 3.10
pyenv install 3.10.13
pyenv global 3.10.13

# Set up Poetry
poetry install --no-root
