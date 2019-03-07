# CS411Project
## Overview
This repo is for the CS411 Final Project for SP19. It is an application that will suggest songs for groups of people based on the individuals' music preferences. Currently both the website and PostgreSQL database are hosted on Heroku.

## Links
[App](https://cs411-spotify.herokuapp.com)

[Google Doc](https://docs.google.com/document/d/1FZgSn6VcPV9DvcemfN2ge1MxUPTuL0UNmxrsfGNsPt0/edit)

[Project Page](https://wiki.illinois.edu/wiki/display/CS411SP19/temp1)

## Prereq
[PostgreSQL](https://www.postgresql.org/download/), [Python](https://www.python.org/downloads/), [Git Bash](https://git-scm.com/downloads), [pip](https://pip.pypa.io/en/stable/installing/)

## Developer Set Up

### Heroku
1. Create an account on [Heroku](https://heroku.com)
2. Get added as a collaborator for the cs411-spotify project
3. Get added as a superuser for the cs411-spotify project

### Virtual Environment
1. Create the virtual environment (only need to be done once)

```
python -m virtualenv env
```

2. Activate the environment (must be done for every new Bash window)

```
source env/bin/activate
```

3. Install the requirements.txt (only must be done when new dependencies are added)

```
pip install -r requirements.txt
```

4. When done working, deactivate the virtualenv

```
deactivate
```

### Git
Automatic deployment of the ```prod``` branch is currently on. Any changes to the ```prod``` branch will be viewable on the [webpage](https://https://cs411-spotify.herokuapp.com) within a few minutes.

#### Making Changes:
```
git status
git add .
git commit -m "INSERT COMMIT MESSAGE"
git push

# if pushing to deploy
git push origin master:prod
```

#### Basic Commands:
1. git clone - makes a copy of this repo in your directory

```
git clone https://github.com/elnathanau1/CS411Project.git
```

2. git checkout - switches branches or restores working files

```
# switching into master branch
git checkout master
```

3. git pull - updates local files to most recent files in branch

```
git pull
```

4. git status - tells you which files you have changed

```
git status
```

5. git add - Tells git which files you have changed within the repo

```
# add all files that have been changed
git add .
```

6. git commit - stages the changes added through ```git add```

```
git commit -m "INSERT COMMIT MESSAGE HERE"
```

7. git push - pushes your commit to the branch
  - Run every time before starting work in case anyone else made changes

```
git push
```

8. git reset - reset local files to the last commit

```
git reset --hard HEAD
```

9. Pushing the ```master``` branch to ```prod``` - automatic deployment from ```prod```

```
git push origin master:prod
```

## Site Navigation
1. https://cs411-spotify.herokuapp.com is currently linked to the same page as [/connect](https://https://cs411-spotify.herokuapp.com/connect/)
  - This page allows the user to connect to Spotify, and will save their user and song info into the database
  - Python code for this page is located at ```django/spotifyapp_1/views.py``` under ```connect()```
  - HTML code for this page is located at ```django/spotifyapp_1/templates/connect.html```

2. [/dash](https://https://cs411-spotify.herokuapp.com/dash) is the page that users are redirected to after connecting to Spotify
  - BUG: this page breaks if not redirected here from [/connect](https://https://cs411-spotify.herokuapp.com/connect/)
  - Python code for this page is located at ```django/spotifyapp_1/views.py``` under ```dash()```
  - HTML code for this page is located at ```django/spotifyapp_1/templates/dash.html```

3. [/admin](https://https://cs411-spotify.herokuapp.com/admin) is the admin page to view the data stored in our database
  - must be a superuser to be able to log in
  - additional functions can be registered under ```django/spotifyapp_1/admin.py```

4. [/login](https://https://cs411-spotify.herokuapp.com/login) is no longer needed and can be used as a testing sandbox
- Python code for this page is located at ```django/spotifyapp_1/views.py``` under ```login()```
- HTML code for this page is located at ```django/spotifyapp_1/templates/login.html```
