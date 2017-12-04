import requests

import os, errno
from shutil import make_archive, rmtree
from datetime import datetime
from definitions import ROOT_DIR

base_url = 'http://www.xeno-canto.org/api/2/recordings?query='
base_download_url = 'http://www.xeno-canto.org/{}/download'


def get_results(urlencoded_query):
    """
    Gets JSON results from Xeno-Canto
    :param urlencoded_query: ex. 'bearded%20bellbird%20q:A'
    :return: JSON from Xeno-Canto
    """
    r = requests.get(base_url + urlencoded_query)
    return r.json()


def get_recording_files(file_ids, query):
    tmp_folder_path = create_temp_dir(query)

    for file_id in file_ids:
        get_recording_file(file_id, tmp_folder_path)

    return tmp_folder_path


def create_temp_dir(query):
    # make temporary download folder
    date_string = datetime.now().strftime('%Y %b %d %H:%M')
    tmp_folder_name = '{} {}'.format(query, date_string)
    tmp_folder_path = os.path.join(ROOT_DIR, 'recordings')
    tmp_folder_path = os.path.join(tmp_folder_path, tmp_folder_name)

    try:
        os.makedirs(tmp_folder_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return tmp_folder_path


def zip_tmp_folder(tmp_folder_path, ziph):
    for root, dirs, files in os.walk(tmp_folder_path):
        for file in files:
            ziph.write(os.path.join(root, file))


def get_recording_file(file_id, tmp_folder_path):
    file_url = base_download_url.format(file_id)
    local_filename = os.path.join(tmp_folder_path, str(file_id)) + '.mp3'
    r = requests.get(file_url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    return local_filename
