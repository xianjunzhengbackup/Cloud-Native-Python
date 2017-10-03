
from app import app
import unittest

class FlaskappTests(unittest.TestCase):
	def setUp(self):
		#create a test client
		self.app=app.test_client()
		#propagate the exeception to the test client
		self.app.testing=True

	#the following code will test whether we get the response on /api/v1/users as 200;
	#if not,it will throw an error and our test will fail.
	#How to run the code?
	#run app.py
	#then $nosetests
	def test_users_status_code(self):
		#sends HTTP GET request to the application
		result=self.app.get('/api/v1/users')
		#assert the status code of the response
		self.assertEqual(result.status_code,200)
