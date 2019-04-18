_msg_fmt = '''Failed to {} (command: {}, target: {})
Expected
  {}
Actual
  {}'''


def _format_msg(exc, kind):
    return _msg_fmt.format(kind, exc.command_name, exc.target, exc.expected, exc.actual)


class AssertionFailure(Exception):
    def __init__(self, command_name='', target='', expected='', actual=''):
        self.command_name = command_name
        self.target = target
        self.expected = expected
        self.actual = actual

    def format_msg(self):
        return _format_msg(self, 'assert')


class VerificationFailure(Exception):
    def __init__(self, command_name='', target='', expected='', actual=''):
        self.command_name = command_name
        self.target = target
        self.expected = expected
        self.actual = actual

    def format_msg(self):
        return _format_msg(self, 'verify')


class UnresolvedTestId(Exception):
    def __init__(self, msg):
        self.msg = msg
