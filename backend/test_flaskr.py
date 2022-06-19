import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DATABASE_NAME_2, DATABASE_PORT, DATABASE_OWNER, DATABASE_PASSWORD
import math
import random

BASE_URL = '/api/v0.1.0'
QUESTIONS_PER_PAGE = 10


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DATABASE_NAME_2
        self.database_path = f'postgresql://{DATABASE_OWNER}:{DATABASE_PASSWORD}@localhost:{DATABASE_PORT}/{self.database_name}'

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

    def test_200_returned_on_get_categories(self):
        res = self.client().get(f'{BASE_URL}/categories')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_400_returned_on_invalid_post_categories_request(self):
        res = self.client().post(f'{BASE_URL}/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_400_returned_on_empty_category_post_categories_request(self):
        res = self.client().post(
            f'{BASE_URL}/categories', json={"category": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # def test_200_returned_on_valid_post_categories_request(self):
    #     ''' Test to confirm that a category is added successfully on passing the required parameters for the request
    #     Note: the value of the category variable must be changed just before a test, else a 403 error is returned indicating that the category already exists and as such, you are forbidden to add a duplicate category
    #     '''
    #     category = "Recent Category"
    #     res = self.client().post(
    #         f'{BASE_URL}/categories', json={"category": category})
    #     data = json.loads(res.data)
    #     new_category = Category.query.order_by(Category.id.desc()).first()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(category, new_category.format()['type'])

    def test_get_questions(self):
        res = self.client().get(f'{BASE_URL}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], "All")
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_returned_on_out_of_bounds_questions_page_number(self):
        question_count = Question.query.count()
        max_page = math.ceil(question_count/QUESTIONS_PER_PAGE)
        page = random.randrange(max_page+1, 1001)
        res = self.client().get(f'{BASE_URL}/questions?page={page}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_200_returned_on_valid_questions_page_number(self):
        question_count = Question.query.count()
        max_page = math.ceil(question_count/QUESTIONS_PER_PAGE)
        page = random.randrange(1, max_page+1)
        res = self.client().get(f'{BASE_URL}/questions?page={page}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], "All")
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_422_returned_on_non_existent_question_id_delete_request(self):
        question_id = 1
        questions = Question.query.order_by(Question.id).all()

        for question in questions:
            if not question_id == question.format()['id']:
                break
            else:
                question_id = question.id + 1

        invalid_question = Question.query.filter(
            Question.id == question_id).first()
        res = self.client().delete(f'{BASE_URL}/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertEqual(invalid_question, None)

    # def test_200_returned_on_valid_question_id_delete_request(self):
    #     question_id = 1
    #     questions = Question.query.order_by(Question.id).all()

    #     for question in questions:
    #         if question_id == question.format()['id']:
    #             break
    #         else:
    #             question_id = question.id + 1

    #     deleted_question = Question.query.filter(
    #         Question.id == question_id).first()
    #     res = self.client().delete(f'{BASE_URL}/questions/{question_id}')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted_id'], deleted_question.format()['id'])

    def test_400_returned_on_invalid_questions_post_request(self):
        res = self.client().post(
            f'{BASE_URL}/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_search_questions(self):
        questions = Question.query.all()
        question = questions[random.randrange(0, len(questions))]
        question_length = len(question.format()['question'])
        lower_range = random.randrange(0, math.floor(question_length/2))
        upper_range = random.randrange(math.floor(
            question_length/2) + 1, question_length)
        search_term = question.format()['question'][lower_range:upper_range]

        res = self.client().post(
            f'{BASE_URL}/questions', json={"searchTerm": search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], "All")
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_returned_on_zero_search_results_found(self):
        search_term = '1two3four5six7eight9ten'
        res = self.client().post(
            f'{BASE_URL}/questions', json={"searchTerm": search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_422_returned_on_invalid_search_post_request(self):
        res = self.client().post(
            f'{BASE_URL}/questions', json={"searchTerm": ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_400_returned_on_invalid_question_create_post_request(self):
        res = self.client().post(
            f'{BASE_URL}/questions', json={"question": "", "answer": "", "category": 0, "difficulty": 0})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_200_returned_on_valid_question_create_post_request(self):
        parameters = {
            "question": "What side effect does dynamic phototherapy have on a patient's vision?", "answer": "Night vision", "category": 1, "difficulty": 5}
        res = self.client().post(f'{BASE_URL}/questions', json=parameters)
        data = json.loads(res.data)
        question = Question.query.order_by(Question.id.desc()).first().format()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(parameters['question'], question['question'])
        self.assertEqual(parameters['answer'], question['answer'])
        self.assertEqual(parameters['category'], question['category'])
        self.assertEqual(parameters['difficulty'], question['difficulty'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
