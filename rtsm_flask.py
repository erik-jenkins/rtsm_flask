import operator

from flask import Flask, render_template, request, session, redirect, url_for
from utils import get_results

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html.j2')

    if request.method == 'POST':
        # form url from request body
        query = request.form['query']

        # render results page
        return redirect(url_for('results', query=query))


@app.route('/results', methods=['GET'])
def results():
    # get query
    query = request.args['query']

    # get results
    response = get_results(query)
    recordings = response['recordings']
    recordings = sorted(recordings, key=lambda rec: rec['q'])

    # render response
    return render_template('results.html.j2', recordings=recordings)


if __name__ == '__main__':
    app.run()
