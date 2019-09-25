# coding=utf-8

import os

from bs4 import BeautifulSoup

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


class NotesProvider:
    __notebook_name = ""
    __ENCODING = "utf-8"

    def __init__(self, notebook_name):
        self.__notebook_name = notebook_name

    def saveNotesContent(self, evernoteClient, notesMetadataFilterFunction, folderPath):
        noteStore = evernoteClient.get_note_store()
        token = evernoteClient.token

        print ("Start downloading notes...")
        notesTitlesAndGuids = self.__getNotesTitlesAndGuids(
            noteStore, evernoteClient, notesMetadataFilterFunction)

        for index, titleAndGuid in enumerate(notesTitlesAndGuids):
            title, guid = titleAndGuid
            currentProgressString = f"{(index + 1)}/{len(notesTitlesAndGuids)}"

            print (f"Downloading note named '{title}' content, {currentProgressString}....")
            notecontent = noteStore.getNoteContent(
                token, guid)

            fileName = f"{title}.html"
            self.__createDirectoryIfNotExist(folderPath)

            joinedPath = os.path.join(folderPath, fileName)
            self.__saveNoteContentToFile(joinedPath, notecontent)
            print (f"Saved file {currentProgressString} as '{joinedPath}'")

        self.__printFinishedMessage(folderPath)

    def __getNotesTitlesAndGuids(self, noteStore, evernoteClient, notesMetadataFilterFunction):
        notesMetadata = self.__getNotesMetadata(
            noteStore, evernoteClient.token, notesMetadataFilterFunction)
        notesTitlesAndGuids = map(lambda note: (
            note.title, note.guid), notesMetadata)
        return list(notesTitlesAndGuids)

    def __getAllNotesMetadataFromNotebook(self, notebookGuid, noteStore, token):
        NotesFilter = NoteFilter(notebookGuid=notebookGuid)

        spec = NotesMetadataResultSpec()
        spec.includeTitle = True

        allNotesFromNotebook = noteStore.findNotesMetadata(
            token, NotesFilter, 0, 250, spec)
        return allNotesFromNotebook.notes

    def __createDirectoryIfNotExist(self, folderPath):
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)

    def __saveNoteContentToFile(self, joinedPath, notecontent):
        with open(joinedPath, 'w') as file:
            prettyfiedNoteContent = BeautifulSoup(notecontent, 'html.parser').prettify()#.encode(self.__ENCODING)
            file.write(prettyfiedNoteContent)

    def __printFinishedMessage(self, folderPath):
        absoluteFilePath = f"{os.path.dirname(os.path.abspath(folderPath))}/{folderPath}"
        print (f"All notes have been exported to folder: {absoluteFilePath}")

    def __getNotesMetadata(self, noteStore, token, notesMetadataFilterFunction):

        Notebook = self.__getNotebookWithSpecifiedName(
            noteStore=noteStore, notebookName=self.__notebook_name)
        self.__terminateIfNotebookIsNull(Notebook)

        allNotesMetadataFromNotebook = self.__getAllNotesMetadataFromNotebook(
            Notebook.guid, noteStore, token)

        filteredNotesMetadata = list(
            filter(lambda note: notesMetadataFilterFunction(note), allNotesMetadataFromNotebook))

        return filteredNotesMetadata

    def __getNotebookWithSpecifiedName(self, noteStore, notebookName):
        notebooks = noteStore.listNotebooks()

        for notebook in notebooks:
            if notebook.name == notebookName:
                return notebook
        return None

    def __terminateIfNotebookIsNull(self, Notebook):
        if Notebook == None:
            print (f"Couldn't find a notebook named '{self.__notebook_name}', script will terminate")
            exit(1)
