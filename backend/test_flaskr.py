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


def get_questions_by_category_id(category_id):
    questions = Question.query.filter(
        Question.category == category_id).all()

    return questions


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

    def test_returned_on_get_categories(self):
        ''' Test to confirm the list of categories was returned successfully '''
        res = self.client().get(f'{BASE_URL}/categories')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_400_returned_on_invalid_post_categories_request(self):
        ''' Test to confirm that the valid response was returned on passing invalid parameters for the post categories request '''
        res = self.client().post(f'{BASE_URL}/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_400_returned_on_empty_category_post_categories_request(self):
        ''' Test to confirm that the valid response was returned on passing invalid parameters for the post categories request '''
        res = self.client().post(
            f'{BASE_URL}/categories', json={"category": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # def test_201_returned_on_valid_post_categories_request(self):
    #     ''' Test to confirm that a category is added successfully on passing the required parameters for the request
    #     Note: the value of the category variable must be changed just before a test, else a 409 error is returned indicating that the category already exists and as such, the provided category conflicts with an existing one
    #     '''
    #     category = "Test Category"
    #     res = self.client().post(
    #         f'{BASE_URL}/categories', json={"category": category})
    #     data = json.loads(res.data)
    #     new_category = Category.query.order_by(Category.id.desc()).first()

    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(data['message'], "created")
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(category, new_category.format()['type'])

    def test_get_questions(self):
        ''' Test to confirm the list of questions was returned successfully '''
        res = self.client().get(f'{BASE_URL}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], "All")
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_returned_on_out_of_bounds_questions_page_number(self):
        ''' Test to confirm that the valid response was returned on passing invalid page argument for the get questions request '''
        question_count = Question.query.count()
        max_page = math.ceil(question_count/QUESTIONS_PER_PAGE)
        page = random.randrange(max_page+1, 1001)
        res = self.client().get(f'{BASE_URL}/questions?page={page}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_200_returned_on_valid_questions_page_number(self):
        ''' Test to confirm the list of questions was returned successfully on passing a valid page argument '''
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
        ''' Test to confirm that the valid response was returned on passing a question id that doesn't exist in the database for the delete question request '''
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

    def test_200_returned_on_valid_question_id_delete_request(self):
        ''' Test to confirm that a valid response was returned for a successful question delete '''
        question_id = Question.query.order_by(
            Question.id.desc()).first().format()['id']

        deleted_question = Question.query.filter(
            Question.id == question_id).first()
        res = self.client().delete(f'{BASE_URL}/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], deleted_question.format()['id'])

    def test_400_returned_on_invalid_questions_post_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        res = self.client().post(
            f'{BASE_URL}/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_404_returned_on_zero_search_results_found(self):
        ''' Test to confirm that the valid response was returned when no result could be found for questions search request '''
        search_term = '1two3four5six7eight9ten'
        res = self.client().post(
            f'{BASE_URL}/questions', json={"search_term": search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_422_returned_on_invalid_search_post_request(self):
        ''' Test to confirm that the valid response was returned on passing an empty search value for questions search request '''
        res = self.client().post(
            f'{BASE_URL}/questions', json={"search_term": ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_200_returned_on_valid_search_questions_request(self):
        ''' Test to confirm that the valid response was returned on successful question search request '''
        questions = Question.query.all()
        question = questions[random.randrange(0, len(questions))]
        question_length = len(question.format()['question'])
        lower_range = random.randrange(0, math.floor(question_length/2))
        upper_range = random.randrange(math.floor(
            question_length/2) + 1, question_length)
        search_term = question.format()['question'][lower_range:upper_range]

        res = self.client().post(
            f'{BASE_URL}/questions', json={"search_term": search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], "All")
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_400_returned_on_invalid_question_create_post_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        res = self.client().post(
            f'{BASE_URL}/questions', json={"question": "", "answer": "", "category": 0, "difficulty": 0})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_201_returned_on_valid_question_create_post_request(self):
        ''' Test to confirm that the valid response was returned on successful post question request '''
        parameters = {
            "question": "What side effect does dynamic phototherapy have on a patient's vision?", "answer": "Night vision", "category": 1, "difficulty": 5}
        res = self.client().post(f'{BASE_URL}/questions', json=parameters)
        data = json.loads(res.data)
        question = Question.query.order_by(Question.id.desc()).first().format()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "created")
        self.assertEqual(parameters['question'], question['question'])
        self.assertEqual(parameters['answer'], question['answer'])
        self.assertEqual(parameters['category'], question['category'])
        self.assertEqual(parameters['difficulty'], question['difficulty'])

    def test_404_returned_due_to_category_id_out_of_bounds_on_get_questions_by_category_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        max_id = Category.query.count()
        category_id = random.randrange(max_id+1, 1001)
        res = self.client().get(
            f'{BASE_URL}/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_200_returned_on_valid_get_questions_by_category_request(self):
        ''' Test to confirm the list of questions filtered by the provided category was returned successfully '''
        categories = Category.query.order_by(Category.id).all()

        category_ids = []

        for category in categories:
            id = category.format()['id']
            if get_questions_by_category_id(category_id=id):
                category_ids.append(id)

        category_id = category_ids[random.randrange(0, len(category_ids))]

        res = self.client().get(
            f'{BASE_URL}/categories/{category_id}/questions')
        data = json.loads(res.data)
        category = Category.query.get(category_id).format()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category['type'])

    def test_404_returned_on_invalid_get_quizzes_request(self):
        ''' Test to confirm that the valid response was returned when no result could be returned for the get quizzes request '''
        id = 1
        while get_questions_by_category_id(id):
            id = id+1

        res = self.client().post(f'{BASE_URL}/quizzes', json={
            "quiz_category": {
                "id": id
            },
            "previous_questions": []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_400_returned_on_invalid_get_quizzes_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        res = self.client().post(f'{BASE_URL}/quizzes', json={
            "quiz_category": {},
            "previous_questions": None
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_200_returned_on_valid_get_quizzes_request(self):
        ''' Test to confirm that a matching the rules of the quiz was returned successfully '''
        categories = Category.query.order_by(Category.id).all()

        returned_categories = {}
        for category in categories:
            if get_questions_by_category_id(category_id=category.format()['id']):
                returned_categories[str(category.format()['id'])] = category.format()[
                    'type']

        valid_category_ids = []
        for key in returned_categories.keys():
            valid_category_ids.append(int(key))

        valid_category_id = valid_category_ids[random.randrange(
            0, len(valid_category_ids))]

        current_category = {
            "id": valid_category_id,
            "type": returned_categories[str(valid_category_id)]
        }

        questions = Question.query.filter(
            Question.category == valid_category_id).all()

        all_question_ids = [question.format()['id'] for question in questions]

        previous_questions = []
        for i in range(random.randint(0, len(questions))):
            id = all_question_ids[random.randrange(
                0, len(all_question_ids)) if len(all_question_ids) > 1 else 0]
            if id not in previous_questions:
                previous_questions.append(id)

        res = self.client().post(f'{BASE_URL}/quizzes', json={
            "quiz_category": current_category,
            "previous_questions": previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('question' in data)
        if data['question']:
            self.assertTrue(data['question'])
            self.assertTrue(data['question']['id'] not in previous_questions)
            self.assertEqual(data['question']['category'], valid_category_id)
        else:
            self.assertEqual(len(data['question']), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
