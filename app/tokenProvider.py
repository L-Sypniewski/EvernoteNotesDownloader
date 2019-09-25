class TokenProvider:
    __filePath = ''

    def __init__(self, filePath):
        self.__filePath = filePath

    def getToken(self, isSandbox):
        if isSandbox:
            return self.__getSandboxToken().rstrip("\n")
        else:
            return self.__getProdToken().rstrip("\n")

    def __getTokenFromTextFile(self, lineNumber):
        fileContent = open(self.__filePath, "r").readlines()
        return fileContent[lineNumber - 1]

    def __getSandboxToken(self):
        return self.__getTokenFromTextFile(lineNumber=1)

    def __getProdToken(self):
        return self.__getTokenFromTextFile(lineNumber=4)
