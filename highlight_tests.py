import os
import highlight
import unittest
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        highlight.app.config['TESTING'] = True
        self.app = highlight.app.test_client()

    def tearDown(self):
        return

    def test_format_python(self):
        rv = self.app.post('/python', data=dict(
            body_plain='print "Hello World"',
            body_html=''
        ))
        output = json.loads(rv.data)
        assert output['body_html'] == "<html>\n<head></head>\n<body><div><pre><span style=\"color:#008000; font-weight:bold\">print</span> <span style=\"color:#BA2121\">\"Hello World\"</span>\n</pre></div></body>\n</html>\n"

    def test_skip_formatting_with_html_part(self):
        rv = self.app.post('/python', data=dict(
            body_plain='print "Hello World"',
            body_html='<pre>print "Hello World"</pre>'
        ))
        output = json.loads(rv.data)
        assert output['body_html'] == '<pre>print "Hello World"</pre>'

    def test_format_diff(self):
        rv = self.app.post('/diff', data=dict(
            body_plain="1c1\n< Hello\n---\n\n> There\n",
            body_html=''
        ))
        output = json.loads(rv.data)
        assert output['body_html'] == "<html>\n<head></head>\n<body><div><pre>1c1\n&lt; Hello\n<span style=\"color:#A00000\">---</span>\n\n&gt; There\n</pre></div></body>\n</html>\n"

    def test_format_missing(self):
        rv = self.app.post('/notreal', data=dict(
            body_plain='print "Hello World"',
            body_html=''
        ))
        assert rv.status == '404 NOT FOUND'

    def test_info(self):
        rv = self.app.get('/')
        assert 'Syntax highlighting' in rv.data

if __name__ == '__main__':
    unittest.main()
