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

	"""
	The following code will test whether we get response on http://localhost
	:5000/api/v2/tweets/<id> where id from 1 to 10 as 200
	"""
	def test_tweets_status_code(self):
		for id in (1,20):
			link="/api/v2/tweets/%d"%id
			result=self.app.get(link)
			print("Test result for ",link,":",result.status_code)
			self.assertEqual(result.status_code,200)
