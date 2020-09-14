from flask import Flask, render_template, request , session
from vsearch import search4letters
from DBcm import UseDatabase
from checker import check_logged_in

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1',
                           'user': 'root',
                           'password': 'root',
                           'database': 'vsearchlogDB', }
@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'


def log_request(req: 'request ', res: str) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        SQL = """insert into log
                     (phrase, letters, ip, browser_string, results)
                           values (%s, %s, %s, %s, %s)"""
        cursor.execute(SQL, (req.form['phrase'],
                             req.form['letters'],
                             req.remote_addr,
                             req.user_agent.browser,
                             res,))


@app.route('/search4', methods=['POST'])
@check_logged_in
def do_search():
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))

    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results, )


@app.route('/')
@app.route('/entry')
@check_logged_in
def entry_page():
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = """select phrase, letters, ip, browser_string, results
            from log"""
        cursor.execute(sql)
        contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents, )

app.secret_key = 'YouWillNeverGuessMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)
