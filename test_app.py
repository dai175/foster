import io
import json
import unittest
import urllib

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class FosterTestCase(unittest.TestCase):
    """This class represents the Foster test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client
        self.database_name = "foster_test"
        self.database_path = "postgres://{}/{}". \
            format('user:password@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()

        token_admin = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9UUkdORUkyTUVaRlFrVXlNak16TVRSQk5qWTBORVkwUlRsRk9EaEJORGd5UmpCRE1UZzBRUSJ9.eyJpc3MiOiJodHRwczovL2Zvc3Rlci1hbi1hbmltYWwuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlM2JmOTA3NGU0MzZkMGU3OTdhNmQzYSIsImF1ZCI6ImZvc3RlciIsImlhdCI6MTU4MTcyOTg3NSwiZXhwIjoxNTgxNzM3MDc1LCJhenAiOiI0bDJaeUF5OHRiMGk4NVI1Q1QzMk1haVVVdDVkRTBpRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFuaW1hbCIsImNyZWF0ZTpjYXRlZ29yeSIsImNyZWF0ZTp0eXBlIiwiZGVsZXRlOmFuaW1hbCIsImRlbGV0ZTpjYXRlZ29yeSIsImRlbGV0ZTp0eXBlIiwiZWRpdDphbmltYWwiLCJlZGl0OmNhdGVnb3J5IiwiZWRpdDp0eXBlIiwiZ2V0OmFuaW1hbHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDp0eXBlcyJdfQ.FalHCeHi_Rv9YiLZ5VycwovVAbLMlSct9cE7YmfYwwknEYSIni0a7vC4UTCflnvf7XNCEQKye3mcsc9MifymFyiOfA-9lpsP8EqVh7GsH6J7mqgJWZW6xDNeFs11tMOFjzcAWWGiHbMpaNzs7qygsz6HcUjJPCpgF0uUsB_vVUGiRo4pJTobeDHvQHj7WZVJ4eBJQiFMk-RXiQjwtQRQe54sODzhXlahCZLB0-s46EBEZVxctXii8DJ9rORaN_yOvMlJsNVFRh9TOFfcuLhbzbqTvpiKdb6kogQlTPVL234ajKY_AT-VsWr9aB8ZmLUL4UgnqC7E9MDlqqugWVRHTw'
        self.headers_admin = {'Authorization': 'Bearer ' + token_admin}

        token_user = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9UUkdORUkyTUVaRlFrVXlNak16TVRSQk5qWTBORVkwUlRsRk9EaEJORGd5UmpCRE1UZzBRUSJ9.eyJpc3MiOiJodHRwczovL2Zvc3Rlci1hbi1hbmltYWwuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDE1YTU0YWU3NjU0MGU3YjhjNDJjZiIsImF1ZCI6ImZvc3RlciIsImlhdCI6MTU4MTczMzI4NCwiZXhwIjoxNTgxNzQwNDg0LCJhenAiOiI0bDJaeUF5OHRiMGk4NVI1Q1QzMk1haVVVdDVkRTBpRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFuaW1hbHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDp0eXBlcyJdfQ.V6lSwt97jNV7xRwcZpPlyLOZg8cjT2Q6gfXX7sRGrEapzmIzuDZbqywsU3a_3DcUguCs4WNOvQDqMLEt02oSPI6CvqQ_NTtuCxaiCfTXrmhDpBlMhyM0OvfR5YF9cPQgM98FANL4itAK3nnlCkalen3-Dom7Qlpb2DSMLfkbxiu7UMeU2GFdtZyZG6e3paYTDUXBihgQt0eCpAgsTKTc163gugnWn0k-mjhgwgUz9S1yTi-SQbD5A2bLabWdVlmhszT4iyQ7-U4f9NnordwVQXJqnbkvYoJ0vyvBu1h6SoTeQIQBf2336lA-f-5Xi0FpCUROtL7TBrXQVWt9rpSKeg'
        self.headers_user = {'Authorization': 'Bearer ' + token_user}

        url = 'https://upload.wikimedia.org/wikipedia/commons/3/3b/' \
              'Udacity_logo.png'
        with urllib.request.urlopen(url) as f:
            img = io.BytesIO(f.read())
            self.new_category_success = {
                'name': 'Dog',
                'description': 'A group of animals that belong to '
                               'the vertebrate Subphylum Carnivora (Felidae) '
                               'in the classification of living organisms.',
                'image': (img, 'udacity_logo.png')
            }
            self.new_category_error = {
                'name': '',
                'description': '',
                'image': (img, 'udacity_logo.png')
            }
            self.new_type_success = {
                'category': 1,
                'name': 'Bulldog',
                'description': 'The Bulldog, also known as the British '
                               'Bulldog or English Bulldog, is a '
                               'medium-sized dog breed. It is a muscular, '
                               'hefty dog with a wrinkled face and a '
                               'distinctive pushed-in nose.',
                'image': (img, 'udacity_logo.png')
            }
            self.new_type_error = {
                'category': 1,
                'name': '',
                'description': '',
                'image': (img, 'udacity_logo.png')
            }
            self.new_animal_success = {
                'type': 1,
                'name': 'Spike Bulldog',
                'sex': '1',
                'date_of_birth': '2020-01-01',
                'weight': '10',
                'place_of_birth': 'Cartoon',
                'description': 'Spike Bulldog is a gray, rough bulldog '
                               'that appears in many of Tom and Jerry '
                               'cartoons. He has a somewhat minor friendship '
                               'with Jerry and is a formidable enemy to Tom, '
                               'though he is occasionally a rival to both '
                               'protagonists, as he was in the episode Dog '
                               'Trouble.',
                'image': (img, 'udacity_logo.png')
            }
            self.new_animal_error = {
                'type': 1,
                'name': '',
                'sex': '',
                'date_of_birth': '',
                'weight': '',
                'place_of_birth': '',
                'description': '',
                'image': (img, 'udacity_logo.png')
            }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    # ------------------------------------------------------------------------
    #   Root
    # ------------------------------------------------------------------------

    def test_root(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    # ------------------------------------------------------------------------
    #   Category
    # ------------------------------------------------------------------------

    def test_create_category_admin(self):
        res = self.client().post('/categories/create',
                                 content_type='multipart/form-data',
                                 data=self.new_category_success,
                                 headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_category_user(self):
        res = self.client().post('/categories/create',
                                 content_type='multipart/form-data',
                                 data=self.new_category_success,
                                 headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_create_category_validation_error(self):
        res = self.client().post('/categories/create',
                                 content_type='multipart/form-data',
                                 data=self.new_category_error,
                                 headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_edit_category_admin(self):
        res = self.client().patch('/category/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_category_success,
                                  headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_category_user(self):
        res = self.client().patch('/category/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_category_success,
                                  headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_edit_category_validation_error(self):
        res = self.client().patch('/category/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_category_error,
                                  headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_get_categories_admin(self):
        res = self.client().get('/categories',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_categories_user(self):
        res = self.client().get('/categories',
                                headers=self.headers_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_category_admin(self):
        res = self.client().get('/category/1',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_category_user(self):
        res = self.client().get('/category/1',
                                headers=self.headers_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_category_not_found(self):
        res = self.client().get('/category/99',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_z_delete_category_admin(self):
        res = self.client().delete('/category/1/delete',
                                   headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_z_delete_category_user(self):
        res = self.client().delete('/category/1/delete',
                                   headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_z_delete_category_not_found(self):
        res = self.client().delete('/category/99/delete',
                                   headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # ------------------------------------------------------------------------
    #   Type
    # ------------------------------------------------------------------------

    def test_create_type_admin(self):
        res = self.client().post('/types/create',
                                 content_type='multipart/form-data',
                                 data=self.new_type_success,
                                 headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_type_user(self):
        res = self.client().post('/types/create',
                                 content_type='multipart/form-data',
                                 data=self.new_type_success,
                                 headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_create_type_validation_error(self):
        res = self.client().post('/types/create',
                                 content_type='multipart/form-data',
                                 data=self.new_type_error,
                                 headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_edit_type_admin(self):
        res = self.client().patch('/type/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_type_success,
                                  headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_type_user(self):
        res = self.client().patch('/type/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_type_success,
                                  headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_edit_type_validation_error(self):
        res = self.client().patch('/type/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_type_error,
                                  headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_get_types_admin(self):
        res = self.client().get('/types/1',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_types_user(self):
        res = self.client().get('/types/1',
                                headers=self.headers_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_type_admin(self):
        res = self.client().get('/type/1',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_type_user(self):
        res = self.client().get('/type/1',
                                headers=self.headers_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_type_not_found(self):
        res = self.client().get('/type/99',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_y_delete_type_admin(self):
        res = self.client().delete('/type/1/delete',
                                   headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_y_delete_type_user(self):
        res = self.client().delete('/type/1/delete',
                                   headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_y_delete_type_not_found(self):
        res = self.client().delete('/type/99/delete',
                                   headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # ------------------------------------------------------------------------
    #   Animal
    # ------------------------------------------------------------------------

    def test_create_z_animal_admin(self):
        res = self.client().post('/animals/create',
                                 content_type='multipart/form-data',
                                 data=self.new_animal_success,
                                 headers=self.headers_admin)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_z_animal_user(self):
        res = self.client().post('/animals/create',
                                 content_type='multipart/form-data',
                                 data=self.new_animal_success,
                                 headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_create_z_animal_validation_error(self):
        res = self.client().post('/animals/create',
                                 content_type='multipart/form-data',
                                 data=self.new_animal_error,
                                 headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_edit_animal_admin(self):
        res = self.client().patch('/animal/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_animal_success,
                                  headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_animal_user(self):
        res = self.client().patch('/animal/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_animal_success,
                                  headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_edit_animal_validation_error(self):
        res = self.client().patch('/animal/1/edit',
                                  content_type='multipart/form-data',
                                  data=self.new_animal_error,
                                  headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_get_animals_admin(self):
        res = self.client().get('/animals/1',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_animals_user(self):
        res = self.client().get('/animals/1',
                                headers=self.headers_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_animal_admin(self):
        res = self.client().get('/animal/1',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_animal_user(self):
        res = self.client().get('/animal/1',
                                headers=self.headers_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['form'])

    def test_get_animal_not_found(self):
        res = self.client().get('/animal/99',
                                headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_x_delete_animal_admin(self):
        res = self.client().delete('/animal/1/delete',
                                   headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_x_delete_animal_user(self):
        res = self.client().delete('/animal/1/delete',
                                   headers=self.headers_user)

        self.assertEqual(res.status_code, 403)

    def test_x_delete_animal_not_found(self):
        res = self.client().delete('/animal/99/delete',
                                   headers=self.headers_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
