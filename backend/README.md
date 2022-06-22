# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.10** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

For Windows Users

```bash
${path_to_your_virtual_environment}/Scripts/python.exe -m pip install -r requirements.txt
```

For Unix Users

```bash
${path_to_your_virtual_environment}/bin/python -m pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

For Unix Users

```bash
createdb trivia
```

For Windows Users
Enter your psql tool environment as root user and run the following command

```shell
root_database=# CREATE DATABASE  trivia;
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

For Unix Users

```bash
psql trivia < trivia.psql
```

For Windows Users
Enter your psql tool environment as root user and enter your trivia database then run the following command

```shell
trivia=# \i trivia.psql;
```

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Once you have your server running, you can go start up your frontend to work with the backend server.

## Api EndPoints

### Get Categories

`GET '/api/v0.1.0/categories'`

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category. If the request argument quiz is set to `true`, then only categories that have questions assigned to them are returned, else by default all categories are returned.

- Request Arguments: quiz- type boolean, default false
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### Create a new Categories

`POST '/api/v0.1.0/categories'`

Creates a new category with the name specified in the category property of the body request

- Request Arguments: None
- Request Body Properties: category- type string
- Returns: A success value and message.

```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

### Get Questions

`GET '/api/v0.1.0/questions'`

Fetches a list of dictionaries with the questions information, including the list of categories, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Returns: An object with five keys:
  - `success` that contains a boolean value
  - `questions` that contains an array of objects
  - `total_questions` that contains an integer
  - `categories` that contains an object that contains objects
  - `current_category` that contains a null value.

```json
{
  "success": true,
  "questions": [],
  "total_questions": 0,
  "categories": {},
  "current_category": null
}
```

### Delete Question

`DELETE '/api/v0.1.0/questions/<int:id>'`

Deletes a question

- Request Arguments: None
- Returns: A success value and the deleted question id.

```json
{
  "success": true,
  "deleted_id": 0,
}
```

### Search Questions

`POST '/api/v0.1.0/questions'`

Fetches a list of dictionaries with the questions information that match the search value, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Request Body Properties: search_term- type string
- Returns: An object with five keys:
  - `success` that contains a boolean value
  - `questions` that contains an array of objects
  - `total_questions` that contains an integer
  - `current_category` that contains a null value.

```json
{
  "success": true,
  "questions": [],
  "total_questions": 0,
  "current_category": null
}
```

### Create a new Question

`POST '/api/v0.1.0/questions'`

Creates a new question

- Request Arguments: None
- Request Body Properties:
  - `question` that contains a string value
  - `answer` that contains a string value
  - `category` that contains an integer value of the category id
  - `difficulty` that contains an integer value of the difficulty level
- Returns: An object with five keys:
  - `success` that contains a boolean value
  - `questions` that contains an array of objects
  - `total_questions` that contains an integer
  - `current_category` that contains a null value.
  
```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

### Get Questions by Category

`POST '/api/v0.1.0/categories/<int:category_id>/questions'`

Fetches a list of dictionaries with the questions information with a category id that matches what the one being requested for, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Request Body Properties: search_term- type string
- Returns: An object with five keys:
  - `success` that contains a boolean value
  - `questions` that contains an array of objects
  - `total_questions` that contains an integer
  - `current_category` that contains a null value.

```json
{
  "success": true,
  "questions": [],
  "total_questions": 0,
  "current_category": 0
}
```

### Load Quiz Question

`POST '/api/v0.1.0/quizzes'`

Fetches a single question for the quiz on the condition that the question's id does not already exist among the previous questions' ids coming from the client.

- Request Arguments: None
- Request Body Properties:
  - `quiz_category` that contains an object an `id` key that contains an integer indicating the category of the question to be returned
  - `previous_questions` that contains a list ids of the previous questions accepted by the client
- Returns: An object with two keys:
  - `success` that contains a boolean value
  - `question` that contains an object with the returned question information

```json
{
  "success": true,
  "question": {},
}
```
