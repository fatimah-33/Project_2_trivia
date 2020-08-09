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
  Create an endpoint to handle GET requests for all available categories, done
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
  Create an endpoint to handle GET requests for questions,done 
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
  Create an endpoint to DELETE question using a question ID, done
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
  Create an endpoint to POST a new question, done 
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
  Create a POST endpoint to get questions based on a search term, done 
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
  Create a GET endpoint to get questions based on category, done 
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
  Create a POST endpoint to get questions to play the quiz, done 
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
        questions = Question.query.order_by(func.random()).filter(~Question.id.in_(previous_questions)).first()
      else:
        questions = Question.query.order_by(func.random()).filter(Question.category == category_id,~Question.id.in_(previous_questions)).first()  
      if questions is None:
        return jsonify({
          'success' : True
          }) 
      formated_questions = questions.format()
      return jsonify({
          'success' : True,
          'question' : formated_questions
          })  
    except:
      abort(422)
  '''
  Create error handlers , done
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

    