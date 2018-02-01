import sys
from StringIO import StringIO


class redirect_stdout:
    def __init__(self, target):
        self.stdout = sys.stdout
        self.target = target

    def __enter__(self):
        sys.stdout = self.target

    def __exit__(self, type, value, tb):
        sys.stdout = self.stdout


out = StringIO()

with redirect_stdout(out):
    print "Test"

out.getvalue()