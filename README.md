# CS411Project
## Overview
This repo is for the CS411 Final Project for SP19. It is an application that will suggest songs for groups of people based on the individuals' music preferences. Currently both the website and PostgreSQL database are hosted on Heroku.

## Links
[App](https://https://cs411-spotify.herokuapp.com)

[Google Doc](https://docs.google.com/document/d/1FZgSn6VcPV9DvcemfN2ge1MxUPTuL0UNmxrsfGNsPt0/edit)

[Project Page](https://wiki.illinois.edu/wiki/display/CS411SP19/temp1)

## Prereq
[PostgreSQL](https://www.postgresql.org/download/), [Python](https://www.python.org/downloads/), [Git Bash](https://git-scm.com/downloads), [pip](https://pip.pypa.io/en/stable/installing/)

## Developer Set Up

### Heroku
1. Create an account on [Heroku](https://heroku.com)
2. Get added as a collaborator for the cs411-spotify project

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
deactviate
```

### Git
Automatic deployment of the ```prod``` branch is currently on. Any changes to the ```prod``` branch will be viewable on the [webpage](https://https://cs411-spotify.herokuapp.com) within a few minutes.

Basic commands:
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

7. git push - pushes your commit to the branch`

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
