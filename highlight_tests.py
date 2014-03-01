import os
import highlight
import unittest

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        highlight.app.config['TESTING'] = True
        self.app = highlight.app.test_client()

    def tearDown(self):
        return

    def test_hello(self):
        rv = self.app.get('/')
        assert 'Hello' in rv.data



if __name__ == '__main__':
    unittest.main()
