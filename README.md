# CS411Project

## Installation
[PostgreSQL](https://www.postgresql.org/download/)

(note: For pgAdmin4 installation, will ask for a deafult password. I used "password". Use this unless you want to change settings.py in /django/spotifyapp/)

[Python](https://www.python.org/downloads/)

[Git Bash](https://git-scm.com/downloads)

[pip](https://pip.pypa.io/en/stable/installing/)

After those have been installed, run this in terminal:

```
pip install -r requirements.txt
```

## Project Set Up
1. Load pgAdmin4 using: (http://127.0.0.1:65274/browser/)
2. Go to the toolbar, and under 'Tools', click on the Query Tool
3. Type this into the box and press fn + f5

```
CREATE DATABASE spotify_app;
```

4. In terminal, cd to /django/spotifyapp
5. Type this into terminal to set up admin user:

```
python manage.py createsuperuse
```

6. Type this into terminal to create tables within database:

```
python manage.py makemigrations
python manage.py migrate
```

## Running Project
1. In terminal, type in:

```
python manage.py runserver
```

2. In the browser, go to (http://127.0.0.1:8000/dash/)

## Django Commands
Relevant commands necessary for development:

```
# Run the server
python manage.py runserver

# Make migration (after change to model)
python manage.py makemigrations spotifyapp_1

# Migrate (call after makemigration)
python manage.py migrate
```
