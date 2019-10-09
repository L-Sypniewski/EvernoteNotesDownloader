# coding=utf-8

from api_version_validator import APIVersionValidator
from evernote.api.client import EvernoteClient
from notes_provider import NotesProvider
from token_provider import TokenProvider
import sys


def terminate_if_newer_API_available(is_version_ok):
    if not is_version_ok:
        print ("There's newer API version available, script will terminate.")
        exit(1)


IS_SANDBOX = sys.argv[1] in ['true', "True"]
TOKEN_FILEPATH = sys.argv[2]
NOTEBOOK_NAME = sys.argv[3]
SAVED_NOTES_FOLDER_PATH = "DownloadedNotes"

token_provider = TokenProvider(filepath=TOKEN_FILEPATH)
auth_token = token_provider.get_token(IS_SANDBOX)
evernote_client = EvernoteClient(token=auth_token, sandbox=IS_SANDBOX, china=False)

is_version_ok = APIVersionValidator().validate_api_version(evernote_client)
terminate_if_newer_API_available(is_version_ok)


def notes_filter(note): return not note.title.startswith('_')


notes = NotesProvider(NOTEBOOK_NAME).save_notes_content(
    evernote_client, notes_filter, SAVED_NOTES_FOLDER_PATH)