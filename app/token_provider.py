class TokenProvider:
    __filepath = ''

    def __init__(self, filepath):
        self.__filepath = filepath

    def get_token(self, is_sandbox):
        if is_sandbox:
            return self.__get_sandbox_token().rstrip("\n")
        else:
            return self.__get_sandbox_token().rstrip("\n")

    def __get_token_fom_text_file(self, line_number):
        file_content = open(self.__filepath, "r").readlines()
        return file_content[line_number - 1]

    def __get_sandbox_token(self):
        return self.__get_token_fom_text_file(line_number=1)

    def __get_sandbox_token(self):
        return self.__get_token_fom_text_file(line_number=4)
