import time
from traceback import format_exc
from inspect import signature, Parameter
from .log import getLogger
logger = getLogger(__name__)


def with_retry(retry, wait, func, *args):
    for i in range(retry):
        try:
            return func(*args)
        except Exception as exc:
            logger.info(exc)
        finally:
            time.sleep(wait)


def call_with_argname_bind(func, args_dict):
    params = signature(func).parameters
    param_names = [
        p.name
        for p in params.values()
        if p.kind == Parameter.POSITIONAL_OR_KEYWORD
    ]

    acceptable_args = {k: v for k, v in args_dict.items() if k in param_names}
    try:
        return func(**acceptable_args)
    except Exception:
        logger.error("Failed to run hook ({} {})".format(func.__module__, func.__name__))
        logger.error(format_exc())


def maybe_bool(s):
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    return s


def construct_dict(key, value):
    def _(elem):
        if elem[0] is None:
            return value
        return {elem[0]: _(elem[1:])}
    return _(key.split(" ") + [None])


def split_with_re(regexp, s, func):
    ret = []
    pos = 0
    match_count = len(regexp.findall(s))

    for m in regexp.finditer(s):
        if m.start() != pos:
            ret.append(s[pos:m.start()])
        ret.append(func(m))
        pos = m.end()

    if match_count > 0:
        if m.end() != len(s):
            ret.append(s[m.end():len(s)])
    else:
        ret.append(s)

    return ret
