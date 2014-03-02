from flask import Flask, request, abort, jsonify

# use the pygments library for code highlighting
from pygments import highlight
from pygments.lexers import PythonLexer, DiffLexer
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

    post = {}
    for key in ['body-plain', 'stripped-text', 'body-html', 'stripped-html']:
        if key in request.form:
            post[key] = request.form[key]

    if 'body-html' in post and post['body-html']:
        return jsonify(post)

    post['body-html'] = highlight_with_lexer(post['body-plain'], lexer_map[lexer])
    post['stripped-html'] = highlight_with_lexer(post['stripped-text'], lexer_map[lexer])

    return jsonify(post)

@app.route('/', methods=['GET'])
def info():
    return 'Syntax highlighting webhook processor for Threadable! See: https://github.com/otherio/threadable-pygments'


def highlight_with_lexer(code, lexer):
    highlighted_code = highlight(code, lexer(), HtmlFormatter())
    highlighted_code = "<style>{0}</style>\n{1}".format(HtmlFormatter().get_style_defs(), highlighted_code)
    return transform(highlighted_code)
