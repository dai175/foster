# Foster an animal

## Getting Started

### Overview

"Foster a animal" is a site created as the [Udacity Full Stack Developer nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) capstone project to create connections between animals and foster parents. On this site, foster parents can find animals registered by the administrator.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, regular web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:categories`
    - `get:types`
    - `get:animals`
    - `edit:category`
    - `edit:type`
    - `edit:animal`
    - `create:category`
    - `create:type`
    - `create:animal`
    - `delete:category`
    - `delete:type`
    - `delete:animal`
6. Create new roles for:
    - User
        - can - `get:categories`
        - can - `get:types`
        - can - `get:animals`
    - Admin
        - can perform all actions

## Running the server

First ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Deployment

The url of heroku is as follows.

```bash
https://foster-an-animal.herokuapp.com/
```

The test users are:

1. User
    - e-mail: `user@example.com`
    - password: `p@ssw0rd`
2. Admin
    - e-mail: `admin@example.com`
    - password: `p@ssw0rd`
