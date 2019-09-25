import evernote.edam.userstore.constants as UserStoreConstants

class APIVersionValidator:
    def validateAPIVersion(self, evernoteClient):
        user_store = evernoteClient.get_user_store()

        isVersionOK = user_store.checkVersion(
                "Evernote EDAMTest (Python)",
                UserStoreConstants.EDAM_VERSION_MAJOR,
                UserStoreConstants.EDAM_VERSION_MINOR
            )
        print (f"Is my Evernote API version up to date? {str(isVersionOK)}")
        print ("")
        if isVersionOK:
            print ("API version is up to date")
        else:
            print ("There's newer API available")

        return isVersionOK
        