from expectations import GetExpectation, PostExpectation
from parse import break_line

class DebugInfo(object):
    def __init__(self):
        self.line_num = 0
        self.line_content = None

    def line(self, line):
        self.line_num += 1
        self.line_content = line


class Flow(object):
    """Flow is a sequence of expectations"""
    def __init__(self, name, line_num = None):
        self.name = name
        self.expectations = []
        self.line_num = line_num

    def add_expectation(self, e):
        self.expectations.append(e)

    def run(self, server):
        print "Running flow %s\t(line %d)"%(self.name, self.line_num)
        for e in self.expectations:
            e.run(server)

    @classmethod
    def _parse(cls, name, script_lines, dbg):
        f = cls(name, line_num=dbg.line_num)
        while script_lines:
            line = script_lines.pop(0).strip()
            dbg.line(line)
            command, rest = break_line(line)
            if command == "get":
                e = GetExpectation._parse(rest, script_lines, dbg)
                f.add_expectation(e)
            elif command == "post":
                e = PostExpectation._parse(rest, script_lines, dbg)
                f.add_expectation(e)
            elif command == "end":
                break
        return f

    def summarize(self):
        print "Flow %s summary: %d expectation(s)"%(self.name, len(self.expectations))
        for e in self.expectations:
            print e

class Script(object):
    def __init__(self):
        self.server = "http://localhost:5000"
        self.flows = []

    def add_flow(self, flow):
        self.flows.append(flow)

    def run(self):
        print "Running script against %s"%(self.server)
        print "%d flow(s) to be run."%(len(self.flows))
        for flow_num, flow in enumerate(self.flows):
            print "Running flow number %d"%(flow_num+1)
            flow.run(self.server)

        self.summarize()

    def summarize(self):
        print "Server target %s, %d flow(s)"%(self.server, len(self.flows))
        for flow in self.flows:
            flow.summarize()
    
    @classmethod
    def parse_script(cls, filename):
        """Reads configuration out of the script and separates each flow"""
        dbg = DebugInfo()
        f = open(filename)
        script_lines = f.readlines()
        f.close()

        script = cls()
        while script_lines:
            line = script_lines.pop(0).strip()
            dbg.line(line)
            command, rest = break_line(line)

            if command == "server":
                script.server = rest.strip("/")

            elif command == "flow":
                name = rest
                f = Flow._parse(name, script_lines, dbg)
                script.add_flow(f)

        return script
