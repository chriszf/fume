from results import NotFoundResult, CodeMismatchResult
import requests
from parse import break_line
import time

class Expectation(object):
    """An expectation is a url request and the response that's supposed to come back."""
    def __init__(self, url, args={}, form={}, code=200, line_num = None):
        self.url = url
        self.args = args
        self.form = form
        self.expected_strings = []
        self.expected_code = code
        self.line_num = line_num
        self.results = []
        self.method = None
        self.method_name = ""
        self.response_time = 0
        self.successful = True

    def report_results(self):
        print "Expectation of URL %s\t(line %d)"%(self.url, self.line_num)
        print "%s request made, %d ms"%(self.method_name, self.response_time)
        print "%d url parameters"%(len(self.args))
        for k,v in self.args.items():
            print "\t%s: %s"%(k,v)
        print "%d form parameters"%(len(self.form))
        for k,v in self.form.items():
            print "\t%s: %s"%(k,v)
        print "%d error(s)"%(len(self.results))
        for result in self.results:
            print result

    @classmethod
    def _parse(cls, url, script_lines, dbg):
        e = cls(url, line_num=dbg.line_num) 
        while script_lines:
            line = script_lines.pop(0).strip()
            dbg.line(line)
            command, rest = break_line(line)
            if command == "code":
                e.code = int(rest)
            elif command == "expect":
                e.expected_strings.append(rest)
            elif command in ["get", "post"]:
                dbg.line_num -= 1
                script_lines.insert(0, line)
                break
            elif command == "args":
                e.args = Expectation._parse_args(script_lines, dbg)
            elif command == "form":
                e.form = Expectation._parse_args(script_lines, dbg)
            elif command == "end":
                if rest == "flow":
                    dbg.line_num -= 1
                    script_lines.insert(0, line)
                break
        return e

    @staticmethod
    def _parse_args(script_lines, dbg):
        args = {}
        while script_lines:
            line = script_lines.pop(0).strip()
            dbg.line(line)
            key, val = break_line(line)
            if line == "end args" or line == "end form":
                break
            args[key] = val 
        return args

    def run(self, server):
        url = server + self.url

        start = time.time()
        resp = self.method(url, params=self.args, data=self.form)
        end = time.time()
        self.response_time = int(end*1000) - int(start*1000)

        # Check for the code
        if resp.status_code != self.code:
            res = CodeMismatchResult(self.code, resp.status_code)
            self.results.append(res)
            self.successful = False

        for s in self.expected_strings:
            if s not in resp:
                res = NotFoundResult(s)
                self.results.append(res)
                self.successful = False

        self.report_results()

    def __str__(self):
        return "Url %s: %d errors"%(self.url, len(self.results))

class GetExpectation(Expectation):
    def __init__(self, *args, **kwargs):
        Expectation.__init__(self, *args, **kwargs)
        self.method = requests.get
        self.method_name = "GET"

class PostExpectation(Expectation):
    def __init__(self, *args, **kwargs):
        Expectation.__init__(self, *args, **kwargs)
        self.method = requests.post
        self.method_name = "POST"
