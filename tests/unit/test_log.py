from logging import LogRecord, INFO
from side_runner_py import log


def test_log_format(mocker):
    record = LogRecord('foo.bar', INFO, '', 0, 'Message', ['foo', 'bar', 1000], None)
    record.created = 0
    msg = log.JoinFormatter.format(record)

    assert msg == '1970-01-01T00:00:00Z INFO foo.bar: Message foo bar 1000'
