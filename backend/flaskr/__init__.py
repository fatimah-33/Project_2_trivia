# to start the local server 
# pg_ctl -D /usr/local/var/postgres start
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import String, Integer, ARRAY,  func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def question_per_page(request, selected_question):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  question = [question.format() for question in selected_question]
  current_question = question[start:end]
  return current_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # either used CORS(app) for basic CORS or spacefiy the cors by defining as next line 
  CORS=(app)
  ## cors = CORS(app, resources={r"/api/*":{"origins":"*"}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,True')
    response.headers.add('Access-Control-Allow-Methods','GET, PATCH,PUT, POST, DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=["GET"])
  def show_categories():
    categories = Category.query.order_by(Category.type).all()
    formated_categories = {category.id: category.type for category in categories}
    if len(categories) == 0:
      abort(404)
    else:
      return jsonify({
        'success':True,
        'categories' : formated_categories
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=["GET"])
  def show_questions():
    questions = Question.query.order_by(Question.id).all()
    current_question = question_per_page(request,questions)
    categories = Category.query.order_by(Category.type).all()
    formated_categories = {category.id: category.type for category in categories}
    if current_question is None:
      abort (404)
    else:
      return jsonify({
        'success':True,
        'questions': current_question,
        'total_questions': len(questions),
        'categories' : formated_categories,
        'current_category': None
      })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods= ['DELETE'])
  def delete_question(question_id):
    try:
      question =  Question.query.get(question_id)
      question.delete()
      return jsonify({
        'success' : True,
        'deleted' : question_id
      })
    except:
      abort (422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods= ['POST'])
  def create_question():
    body = request.get_json()
    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
      abort(422)
    else:
      question =  body.get('question','')
      answer =  body.get('answer','')
      difficulty =  body.get('difficulty','')
      category =  body.get('category','')
      try:
        add_question = Question(question=question,answer=answer,difficulty=difficulty,category=category)
        add_question.insert()
        return jsonify({
          'success' : True,
          'created' : add_question.id
        })
      except:
        abort (404)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods = ['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', '')
    if search_term == '':
      abort(404)
    else:
      question_search_result = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
      formated_result = [question.format() for question in question_search_result]
      return jsonify({
          'success' : True,
          'questions' : formated_result,
          'total_questions' : len(question_search_result),
          'current_category': None
        })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods= ['GET'])
  def questions_by_category(category_id):
    questions = Question.query.filter_by(category = str(category_id)).all()
    formated_question = [question.format() for question in questions]
    if questions is None:
      abort(404)
    else:
      return jsonify({
        'success' : True,
        'questions' : formated_question, 
        'total_questions' : len (questions), 
        'current_category' : category_id
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def play_quizzes():
    try:
      body = request.get_json()
      previous_questions = body.get('previous_questions','')
      quiz_category = body.get('quiz_category','')
      category_id = quiz_category['id']
      # if the category is = 0 then bring all the questions, player did not choose any category 
      if category_id == 0:
        questions = Question.query.filter(~Question.id.in_(previous_questions)).first()
        formated_questions = questions.format()
        return jsonify({
        'success' : True,
        'question' : formated_questions
        })
      else:
        questions = Question.query.order_by(func.random()).filter(Question.category == category_id,~Question.id.in_(previous_questions)).first()
        formated_questions = questions.format() 
        return jsonify({
        'success' : True,
        'question' : formated_questions
        })     
    except:
      abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(404)
  def not_found_page(error):
    return jsonify({
      'success' : False,
      'error' : 404,
      'message' : 'page not found'
    }),404

     
  @app.errorhandler(422)
  def unproccessable_elements(error):
    return jsonify({
      'success' : False,
      'error' : 422,
      'message' : 'unproccessable elements'
    }),422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success' : False,
      'error' : 405,
      'message' : 'this method is not allowed'
    }),405
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success' : False,
      'error' : 400,
      'message' : 'bad request'
    }),400
  
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success' : False,
      'error' : 500,
      'message' : 'internet server error'
    }),500

  return app

    