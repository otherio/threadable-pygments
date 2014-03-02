from flask import Flask
from flask import request
from flask import abort
import json

# use the pygments library for code highlighting
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter

# use premailer to inline the styles from pygments for email client compatibility
from premailer import transform

app = Flask(__name__)

lexer_map = {
    'python': PythonLexer,
    'diff': DiffLexer
}

@app.route('/<lexer>', methods=['POST'])
def highlight_post(lexer):
    if not lexer in lexer_map:
        abort(404)

    post = request.form.copy()
    if 'body-html' in post and post['body-html']:
        return json.dumps(post)

    highlighted_code = highlight(post['body-plain'], lexer_map[lexer](), HtmlFormatter())
    highlighted_code = "<style>{0}</style>\n{1}".format(HtmlFormatter().get_style_defs(), highlighted_code)
    post['body-html'] = transform(highlighted_code)

    highlighted_code = highlight(post['stripped-text'], lexer_map[lexer](), HtmlFormatter())
    highlighted_code = "<style>{0}</style>\n{1}".format(HtmlFormatter().get_style_defs(), highlighted_code)
    post['stripped-html'] = transform(highlighted_code)

    print json.dumps(post)

    return json.dumps(post)

@app.route('/', methods=['GET'])
def info():
    return 'Syntax highlighting webhook processor for Threadable! See: https://github.com/otherio/threadable-pygments'
