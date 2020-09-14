import html

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


app.run()
