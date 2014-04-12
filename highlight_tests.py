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
        rv = self.app.post('/python', data={
            'body-plain': 'print "Hello World"',
            'body-html': '',
            'stripped-text': 'print "Hello Stripped World"',
            'stripped-html': '',
            'Message-Id': 'amessageidgoeshere'
        })
        output = json.loads(rv.data)
        assert rv.content_type == 'application/json'
        assert output['body-html'] == "<html>\n<head></head>\n<body><div><pre style=\"font-size:12px\"><span style=\"color:#008000; font-weight:bold\">print</span> <span style=\"color:#BA2121\">\"Hello World\"</span>\n</pre></div></body>\n</html>\n"
        assert output['stripped-html'] == "<html>\n<head></head>\n<body><div><pre style=\"font-size:12px\"><span style=\"color:#008000; font-weight:bold\">print</span> <span style=\"color:#BA2121\">\"Hello Stripped World\"</span>\n</pre></div></body>\n</html>\n"

    def test_skip_formatting_with_html_part(self):
        rv = self.app.post('/python', data={
            'body-plain': 'print "Hello World"',
            'body-html': '<pre>print "Hello World"</pre>',
            'stripped-text': '',
            'stripped-html': '',
            'Message-Id': 'amessageidgoeshere'
        })
        output = json.loads(rv.data)
        assert rv.content_type == 'application/json'
        assert output['body-html'] == '<pre>print "Hello World"</pre>'

    def test_format_diff(self):
        rv = self.app.post('/diff', data={
            'body-plain': "1c1\n< Hello\n---\n\n> There\n",
            'body-html': '',
            'stripped-text': '',
            'stripped-html': '',
            'Message-Id': 'amessageidgoeshere'
        })
        output = json.loads(rv.data)
        assert output['body-html'] == "<html>\n<head></head>\n<body><div><pre style=\"font-size:12px\">1c1\n&lt; Hello\n<span style=\"color:#A00000\">---</span>\n\n&gt; There\n</pre></div></body>\n</html>\n"

    def test_format_diff_with_long_line(self):
        rv = self.app.post('/diff', data={
            'body-plain': "1c1\n< Breathe in your fears. Face them. To conquer fear, you must become fear. You must bask in the fear of other men. And men fear most what they cannot see. You have to become a terrible thought. A wraith. You have to become an idea! Feel terror cloud your senses. Feel its power to distort. To control. And know that this power can be yours. Embrace your worst fear. Become one with the darkness.\n---\n\n> There\n",
            'body-html': '',
            'stripped-text': '',
            'stripped-html': '',
            'Message-Id': 'amessageidgoeshere'
        })
        output = json.loads(rv.data)
        assert output['body-html'] == "<html>\n<head></head>\n<body><div><pre style=\"font-size:12px\">1c1\n&lt; Breathe in your fears. Face them. To conquer fear, you must become fear. You must bask in the fear of other men. And men fear most what they cannot see. You have to become a terrible thought. A wraith. You have to become an idea! Feel terror cloud your senses. Feel its power to distort. To control. And know that this power can be yours. Embrace your worst fear. Become one with the darkness.\n<span style=\"color:#A00000\">---</span>\n\n&gt; There\n</pre></div></body>\n</html>\n"

    def test_format_diff_with_unicode(self):
        rv = self.app.post('/diff', data={
            'body-plain': u"1c1\n< Hello\n---\n\n> There\xa9\n",
            'body-html': '',
            'stripped-text': '',
            'stripped-html': '',
            'Message-Id': 'amessageidgoeshere'
        })
        output = json.loads(rv.data)
        assert output['body-html'] == u"<html>\n<head></head>\n<body><div><pre style=\"font-size:12px\">1c1\n&lt; Hello\n<span style=\"color:#A00000\">---</span>\n\n&gt; There&#169;\n</pre></div></body>\n</html>\n"

    def test_format_missing(self):
        rv = self.app.post('/notreal', data={
            'body-plain': 'print "Hello World"',
            'body-html': '',
            'stripped-text': '',
            'stripped-html': '',
            'Message-Id': 'amessageidgoeshere'
        })
        assert rv.status == '404 NOT FOUND'

    def test_info(self):
        rv = self.app.get('/')
        assert 'Syntax highlighting' in rv.data

if __name__ == '__main__':
    unittest.main()
