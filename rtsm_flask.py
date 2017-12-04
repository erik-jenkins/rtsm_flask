import json, os, zipfile, pathlib
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, send_file, Response
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
    file_ids_json = request.form['fileIds']
    file_ids = json.loads(file_ids_json)
    query = request.form['query']
    tmp_folder_path = pathlib.Path(get_recording_files(file_ids, query))

    data = BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for filename in tmp_folder_path.iterdir():
            z.write(filename)
        data.seek(0)
        return Response(data,
                        mimetype='application/zip',
                        headers={'Content-Disposition': 'attachment;filename=data.zip'})


if __name__ == '__main__':
    app.run()
