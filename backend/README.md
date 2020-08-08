# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Decumentation 

Here are some examples of the endpoints used in this API
1. GET/categories
   - show all avialable categories with their id & type
   - return success value 
   - Request Arguments: None
   - example of the end point curl http://127.0.0.1:5000/categories
```
{
  "categories": [
    {
      "id": 1, 
      "type": "math"
    }, 
    {
      "id": 2, 
      "type": "earth"
    }
  ], 
  "success": true
}
```
2. GET/questions
   - show all questions, each page has ten questions
   - return number of total questions, categories, success value 
   - Request Arguments: None
   - example of the end point curl http://127.0.0.1:5000/questions
```
{
  "categories": [
    {
      "id": 2, 
      "type": "earth"
    }, 
    {
      "id": 1, 
      "type": "math"
    }
  ], 
  "currentCategory": null, 
  "questions": [
    {
      "answer": "two", 
      "category": "1", 
      "difficulty": 1, 
      "id": 1, 
      "question": "one plus one is equal to"
    }, 
    {
      "answer": "three", 
      "category": "1", 
      "difficulty": 1, 
      "id": 2, 
      "question": "one plus two is equal to"
    }, 
    {
      "answer": "four", 
      "category": "1", 
      "difficulty": 1, 
      "id": 3, 
      "question": "two plus two is equal to"
    } ... ]
    , 
  "success": true, 
  "totalQuestions": 78
}
```
3. DELETE/questions/question_id
   - delete a specific question by id
   - Request Arguments: question id
   - return success value
```
   {
     "success": true,
     "deleted": question_id
   }
```
4. POST/questions
   - add a new question
   - Request Arguments: take values of the question, answer, difficulty, category id
   - return success value
```
   {
     "success": true,
     "created" : add_question.id
   }
```
5. POST/questions/search
   - search for questions by search term 
   - Request Arguments: take a string value for the question to be searched
   - return the question, total number of questions, success value 
```
{
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Two", 
      "category": "1", 
      "difficulty": 1, 
      "id": 1, 
      "question": "one plus one is equal to"
    }, 
    {
      "answer": "three", 
      "category": "1", 
      "difficulty": 1, 
      "id": 2, 
      "question": "one plus two is equal to"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}
```
6. GET/categories/category_id/questions
   - show all questions related to a specific category 
   - Request Arguments: category id
   - retrun all questions,total number of questions, categoty, success value 
   - example of the end point curl http://127.0.0.1:5000/categories/2/questions
```
{
  "currentCategory": 2, 
  "questions": [
    {
      "answer": "moon", 
      "category": "2", 
      "difficulty": 1, 
      "id": 4, 
      "question": "the nearset planet to the earth is the"
    }, 
    {
      "answer": "carbon", 
      "category": "2", 
      "difficulty": 1, 
      "id": 5, 
      "question": "What element is a diamond composed of?"
    }, 
    {
      "answer": "Solar Radiation", 
      "category": "2", 
      "difficulty": 1, 
      "id": 6, 
      "question": "What is the energy released from the sun called?"
    }
  ], 
  "success": true, 
  "totalQuestions": 3
}
```
7. POST/quizzes
   - show a question to be ansewered by the user 
   - Request Arguments: previous question and the selected category id & type to view a random question 
   - return success value
```
{
  "question": 
    {
      "answer": "Two", 
      "category": "1", 
      "difficulty": 1, 
      "id": 1, 
      "question": "one plus one is equal to"
    }
  "success": true
}
```
## Erorr Handling 

following are number of error that is handled in this API

- 404: not found page 
- 422: unproccessable element
- 405: method not allowed
- 400: bad request 
- 500: internet server error

these errors return this JSON object as follow:

```
{
  "error": 404, 
  "message": "tpage not found", 
  "success": false
}  
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```