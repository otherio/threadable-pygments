import os
from flask import Flask

# use the pygments library for code highlighting
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter

# use premailer to inline the styles from pygments for email client compatibility
from premailer import transform

app = Flask(__name__)

@app.route('/')
def highlight_post():
    code = 'print "Hello World"'
    highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
    highlighted_code = "<style>{0}</style>\n{1}".format(HtmlFormatter().get_style_defs(), highlighted_code)
    return transform(highlighted_code)
