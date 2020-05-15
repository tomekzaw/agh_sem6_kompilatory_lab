@echo off
flake8 . --exclude parsetab.py --ignore E501,F403,F405,F811
