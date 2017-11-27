import requests

base_url = 'http://www.xeno-canto.org/api/2/recordings?query='


def get_results(urlencoded_query):
    """
    Gets JSON results from Xeno-Canto
    :param urlencoded_query: ex. 'bearded%20bellbird%20q:A'
    :return: JSON from Xeno-Canto
    """
    r = requests.get(base_url + urlencoded_query)
    return r.json()
