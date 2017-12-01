import json

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from utils import get_results, get_recording_files

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
    return render_template('results.html.j2', recordings=recordings, query=query)


@app.route('/download', methods=['POST'])
def download():
    # file ids
    file_ids_json = request.form['fileIds']
    file_ids = json.loads(file_ids_json)
    query = request.form['query']
    get_recording_files(file_ids, query)
    return jsonify(message='hello, world!'), 200


if __name__ == '__main__':
    app.run()
