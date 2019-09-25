# coding=utf-8

from apiVersionValidator import APIVersionValidator
from evernote.api.client import EvernoteClient
from notesProvider import NotesProvider
from tokenProvider import TokenProvider
import sys


def terminateIfNewerAPIAvailabe(isVersionOK):
    if not isVersionOK:
        print ("There's newer API version available, script will terminate.")
        exit(1)


IS_SANDBOX = sys.argv[1] in ['true', "True"]
TOKEN_FILEPATH = sys.argv[2]
NOTEBOOK_NAME = sys.argv[3]
SAVED_NOTES_FOLDER_PATH = "DownloadedNotes"

tokenProvider = TokenProvider(filePath=TOKEN_FILEPATH)
auth_token = tokenProvider.getToken(IS_SANDBOX)
evernoteClient = EvernoteClient(token=auth_token, sandbox=IS_SANDBOX, china=False)

isVersionOK = APIVersionValidator().validateAPIVersion(evernoteClient)
terminateIfNewerAPIAvailabe(isVersionOK)


def NotesFilterFunction(note): return not note.title.startswith('_')


Notes = NotesProvider(NOTEBOOK_NAME).saveNotesContent(
    evernoteClient, NotesFilterFunction, SAVED_NOTES_FOLDER_PATH)