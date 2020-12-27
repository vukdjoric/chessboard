from io import BytesIO
import requests
import json
import os


TOKEN = os.environ['TOKEN']


def get_updates():
    """
    :return: <class 'dict'>
    """
    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    response = json.loads(response.text)

    return response['result'][-1]


def get_file(file_id):
    """
    :param file_id: <class 'str'>
    :return: <class 'str'>
    """
    url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    try:
        response = json.loads(response.text)
        result = response['result']
        file_path = result['file_path']
        return file_path
    except (ValueError, LookupError):
        return None


def download_file(file_id):
    """
    :param file_id: <class 'str'>
    :param file_path: <class 'str'>
    :return: <class '_io.BytesIO'>
    """
    file_path = get_file(file_id)
    if file_path is None:
        return None

    url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}?file_id={file_id}'

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return BytesIO(response.content)


def send_file(chat_id, file_object):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}'

    payload = {}
    files = [
        ('photo', file_object)
    ]
    headers = {}

    requests.request("GET", url, headers=headers, data=payload, files=files)


def edit_file(chat_id, message_id, file_object):
    url = f'https://api.telegram.org/bot{TOKEN}/editMessageMedia?chat_id={chat_id}&message_id={message_id}&media={{"type": "photo", "media": "attach://media"}}'

    payload = {}
    files = [
        ('media', file_object)
    ]
    headers = {}

    requests.request("GET", url, headers=headers, data=payload, files=files)
