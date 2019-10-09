import evernote.edam.userstore.constants as UserStoreConstants

class APIVersionValidator:
    def validate_api_version(self, evernote_client):
        user_store = evernote_client.get_user_store()

        is_version_ok = user_store.checkVersion(
                "Evernote EDAMTest (Python)",
                UserStoreConstants.EDAM_VERSION_MAJOR,
                UserStoreConstants.EDAM_VERSION_MINOR
            )
        print (f"Is my Evernote API version up to date? {str(is_version_ok)}")
        print ("")
        if is_version_ok:
            print ("API version is up to date")
        else:
            print ("There's newer API available")

        return is_version_ok
        