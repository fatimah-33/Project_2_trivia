import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('fatimah@127.0.0.1:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_show_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['categories']))
    
    def test_404_not_fount_categories(self):
        res = self.client().get('/categories/44444')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'page not found')
    
    def test_pagination_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_wrong_pagenation_questions(self):
        res = self.client().get('/questions/page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],2)
        self.assertEqual(question,None)

    def test_delete_not_exist_question(self):
        res = self.client().delete('/questions/4444')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unproccessable elements')
    
    def test_create_question(self):
        self.new_question = {
            'question' : 'new question',
            'answer' : 'new answer',
            'difficulty' :1,
            'category'  :1
        }
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        
    
    def test_error_create_question(self):
        self.new_question = {
            'answer' : 'new answer',
            'difficulty' :1,
            'category'  :1
        }
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'unproccessable elements')

    def test_search_question(self):
        self.search_term = {
            'searchTerm' : 'What',
        }
        res = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

        
    def test_search_not_found_question(self):
        self.search_term = {
            'searchTerm' : ''
        }
        res = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'page not found')
        
    def test_show_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])
    
    def test_error_question_by_category(self):
        res = self.client().get('/categories/xx/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'page not found')

    def test_paly_the_quiz(self):
        self.currentQuestion = {
            'previous_questions' : [], 
            'quiz_category' : 
                {
                    'type' : 'math',
                    'id' : 1
                  
                }
        }
        res = self.client().post('/quizzes', json=self.currentQuestion)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_error_paly_the_quiz(self):
        self.currentQuestion = {
            'previous_questions' : [],
            'quiz_category' : 
                {
                  
                }
        }
        res = self.client().post('/quizzes', json=self.currentQuestion)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'unproccessable elements')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()