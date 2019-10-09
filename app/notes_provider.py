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

    def save_notes_content(self, evernote_client, notes_filter_by_metadata_function, folder_path):
        note_store = evernote_client.get_note_store()
        token = evernote_client.token

        print ("Start downloading notes...")
        notes_titles_and_guids = self.__get_notes_titles_and_guids(
            note_store, evernote_client, notes_filter_by_metadata_function)

        for index, titleAndGuid in enumerate(notes_titles_and_guids):
            title, guid = titleAndGuid
            current_progress_string = f"{(index + 1)}/{len(notes_titles_and_guids)}"

            print (f"Downloading note named '{title}' content, {current_progress_string}....")
            notecontent = note_store.getNoteContent(
                token, guid)

            fileName = f"{title}.html"
            self.create_drectory_if_not_exist(folder_path)

            joined_path = os.path.join(folder_path, fileName)
            self.__save_note_content_to_file(joined_path, notecontent)
            print (f"Saved file {current_progress_string} as '{joined_path}'")

        self.__print_finished_message(folder_path)

    def __get_notes_titles_and_guids(self, note_store, evernote_client, notes_filter_by_metadata_function):
        notes_metadata = self.__get_notes_metadata(
            note_store, evernote_client.token, notes_filter_by_metadata_function)
        notes_titles_and_guids = map(lambda note: (
            note.title, note.guid), notes_metadata)
        return list(notes_titles_and_guids)

    def __get_all_notes_metadata_from_notebook(self, notebook_guid, note_store, token):
        notes_filter = NoteFilter(notebookGuid=notebook_guid)

        spec = NotesMetadataResultSpec()
        spec.includeTitle = True

        allNotesFromNotebook = note_store.findNotesMetadata(
            token, notes_filter, 0, 250, spec)
        return allNotesFromNotebook.notes

    def create_drectory_if_not_exist(self, folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def __save_note_content_to_file(self, joined_path, notecontent):
        with open(joined_path, 'w') as file:
            prettyfied_note_content = BeautifulSoup(notecontent, 'html.parser').prettify()#.encode(self.__ENCODING)
            file.write(prettyfied_note_content)

    def __print_finished_message(self, folder_path):
        absolue_filepath = f"{os.path.dirname(os.path.abspath(folder_path))}/{folder_path}"
        print (f"All notes have been exported to folder: {absolue_filepath}")

    def __get_notes_metadata(self, note_store, token, notes_filter_by_metadata_function):

        notebook = self.__get_notebook_with_specified_name(
            note_store=note_store, notebook_name=self.__notebook_name)
        self.__terminate_if_notebook_is_null(notebook)

        allNotesMetadataFromNotebook = self.__get_all_notes_metadata_from_notebook(
            notebook.guid, note_store, token)

        filteredNotesMetadata = list(
            filter(lambda note: notes_filter_by_metadata_function(note), allNotesMetadataFromNotebook))

        return filteredNotesMetadata

    def __get_notebook_with_specified_name(self, note_store, notebook_name):
        notebooks = note_store.listNotebooks()

        for notebook in notebooks:
            if notebook.name == notebook_name:
                return notebook
        return None

    def __terminate_if_notebook_is_null(self, Notebook):
        if Notebook == None:
            print (f"Couldn't find a notebook named '{self.__notebook_name}', script will terminate")
            exit(1)
