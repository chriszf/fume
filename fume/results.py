class Result(object):
    def __init__(self):
        pass

class NotFoundResult(Result):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return """\
Error: Expected the following string but couldn't find it:
    %s
    """%(self.string)

class CodeMismatchResult(Result):
    def __init__(self, expected_code, actual_code):
        self.expected_code = expected_code
        self.actual_code = actual_code

    def __str__(self):
        return """\
Error: Expected http response code %d, got the following instead:
    %d
"""%(self.expected_code, self.actual_code)
