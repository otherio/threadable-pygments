import os
from flask import Flask, request, abort, jsonify

# use the pygments library for code highlighting
from pygments import highlight
from pygments.lexers import PythonLexer, DiffLexer
from pygments.formatters import HtmlFormatter

# use premailer to inline the styles from pygments for email client compatibility
from premailer import transform

# get a logger since we're running on heroku, and want logs to go to stdout
import logging

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

if os.environ['DEBUG'] == 'true':
    app.config['DEBUG'] = True

logging.getLogger().addHandler(logging.StreamHandler())

lexer_map = {
    'python': PythonLexer,
    'diff': DiffLexer
}

additional_styles = 'pre {font-size: 12px;}'

@app.route('/<lexer>', methods=['POST'])
def highlight_post(lexer):
    if not lexer in lexer_map:
        abort(404)

    message_id = request.form['Message-Id']
    app.logger.info("processing message {0} as {1}".format(message_id, lexer))

    post = {}
    for key in ['body-plain', 'stripped-text', 'body-html', 'stripped-html']:
        if key in request.form:
            post[key] = request.form[key]

    if 'body-html' in post and post['body-html']:
        app.logger.info("{0} has an html part. skipping.".format(message_id))
        return jsonify(post)

    post['body-html'] = highlight_with_lexer(post['body-plain'], lexer_map[lexer])
    post['stripped-html'] = highlight_with_lexer(post['stripped-text'], lexer_map[lexer])

    return jsonify(post)

@app.route('/', methods=['GET'])
def info():
    return 'Syntax highlighting webhook processor for Threadable! See: https://github.com/otherio/threadable-pygments'


def highlight_with_lexer(code, lexer):
    formatter = HtmlFormatter(encoding='utf-8')
    highlighted_code = highlight(code, lexer(encoding='chardet'), formatter)
    highlighted_code = "<style>{0}{1}</style>\n{2}".format(formatter.get_style_defs(), additional_styles, highlighted_code)
    return transform(highlighted_code.decode('utf-8'))
