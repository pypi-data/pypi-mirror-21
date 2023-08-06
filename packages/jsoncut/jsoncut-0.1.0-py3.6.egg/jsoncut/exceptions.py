"""JSON Cut Custom Exceptions."""
from collections import namedtuple

import click

from . import core

Color = namedtuple('Color', ['val', 'style'])


def color_error_mesg(fmtstr, kwds, no_color=False):
    """Colorize the error message.

    Args:
        fmstr (str): see Python format string mini-language ...
            https://docs.python.org/3.6/library/string.html#formatspec
        kwds (Mapping): the keys are the names of the keywords to
            display; the values are the color names (see below)
        no_color (bool): disable colors.

    Returns:
        str: colorized message.

    Supported colors:
        * black, red, green, yellow, blue, magenta, cyan, white.
        * to make a color bold prefix it with an asterix (*)

    """
    if no_color:
        kwds = {k: v.val for k, v in kwds.items()}
    else:
        def get_style(c):
            return dict(fg=c.style.lstrip('*'), bold=c.style.startswith('*'))
        kwds = {k: click.style(str(v.val), **get_style(v))
                for k, v in kwds.items()}
    return fmtstr.format(**kwds)


def default_error_mesg_fmt(exc, no_color=False):
    """Generate a default error message for custom exceptions.

    Args:
        exc (Exception): the raised exception.
        no_color (bool): disable colors.

    Returns:
        str: colorized error message.
    """
    return color_error_mesg('{err_name}: {err_mesg}', {
        'err_name': Color(exc.__class__.__name__, '*red'),
        'err_mesg': Color(str(exc), 'white')
    }, no_color)


class JsonCutError(Exception):
    """JSON Cut Base Exception."""

    def format_error(self, nocolor=False):
        """Generate formatted error message."""
        return default_error_mesg_fmt(self, nocolor)


class KeyNumberOutOfRange(JsonCutError, ValueError):
    """Invalid Key-Number."""

    pass


class KeyTypeError(JsonCutError, TypeError):
    """Attempt to use an index on a Mapping or a key on a Sequence."""

    def __init__(self, exc, op=None, key=None, itemnum=0, data=None,
                 keylist=None):
        """Initialize KeyNumberOutOfRange Exception.

        Args:
            exc (Exception): orignial TypeError excecption.
            op (str): name of operation where the exception occured.
            key (str): the key being operated on.
            itemnum (int): the data item number; if data is a Sequence.
            data (self):  JSON data being operated on.
            keylist (List[str]): a list of keys found in the data.
        """
        msg = str(exc)
        super(KeyTypeError, self).__init__(msg)
        self.operation = op
        self.item_number = itemnum
        self.data = data
        self.keylist = keylist

    def format_error(self, nocolor=False):
        """Generate formatted error message."""
        mesg = (
            '{dashed_line}\n'
            '{error}\n'
            '{dashed_line}\n'
            'Operation: {operation}\n'
            'Item #: {item_number}\n'
            'Parsed Key List: {key_list}\n'
        )
        kwds = {
            'error': Color(self.args[0], '*red'),
            'dashed_line': Color('-' * 40, 'yellow'),
            'item_number': Color(self.item_number, 'red'),
            'operation': Color(self.operation, 'red'),
            'key_list': Color(self.keylist, 'red')
        }
        return color_error_mesg(mesg, kwds, nocolor)


class IndexOutOfRange(JsonCutError, IndexError):
    """The index number exceeded the length of the sequence."""

    def __init__(self, exc, op=None, itemnum=0, data=None, keylist=None):
        """Initialize IndexOutOfRange Exception.

        Args:
            exc (Exception): orignial TypeError excecption.
            op (str): name of operation where the exception occured.
            key (str): the key being operated on.
            itemnum (int): the data item number; if data is a Sequence.
            data (self):  JSON data being operated on.
            keylist (List[str]): a list of keys found in the data.
        """
        msg = str(exc)
        super(IndexOutOfRange, self).__init__(msg)
        self.operation = op
        self.item_number = itemnum
        self.data = data
        self.keylist = keylist

    def format_error(self, nocolor=False):
        """Generate formatted error message."""
        mesg = (
            '{dashed_line}\n'
            'IndexOutOfRange: {key_name}\n'
            '{dashed_line}\n'
            'Operation: {operation}\n'
            'Item #: {item_number}\n'
            'Parsed Key List: {key_list}\n'
            '{dashed_line}\n'
            'Available Keys:\n'
            '{dashed_line}\n'
            '{available_keys}\n'
        )
        available_keys = '\n'.join(list(core.list_keys(self.data)))
        kwds = {
            'index_number': Color(self.args[0], '*red'),
            'dashed_line': Color('-' * 39, 'yellow'),
            'item_number': Color(self.item_number, 'red'),
            'operation': Color(self.operation, 'red'),
            'available_keys': Color(available_keys, 'white'),
            'key_list': Color(self.keylist, 'red')
        }
        return color_error_mesg(mesg, kwds, nocolor)


class KeyNotFound(JsonCutError, KeyError):
    """The key was not found in the JSON document."""

    def __init__(self, exc, op=None, itemnum=0, data=None, keylist=None):
        """Initialize KeyNotFound Exception.

        Kwds:
            fn (str): name of module/funct where exception was raised
            item (self):  JSON data from which the key was missing
        :param keylist: a list of available keys
        """
        msg = str(exc)
        super(KeyNotFound, self).__init__(msg)
        self.operation = op
        self.item_number = itemnum
        self.data = data
        self.keylist = keylist

    def format_error(self, nocolor=False):
        """Generate formatted error message."""
        mesg = (
            '{dashed_line}\n'
            'KeyNotFound: {key_name}\n'
            '{dashed_line}\n'
            'Operation: {operation}\n'
            'Item #: {item_number}\n'
            'Parsed Key List: {key_list}\n'
            '{dashed_line}\n'
            'Available Keys:\n'
            '{dashed_line}\n'
            '{available_keys}\n'
        )
        name = self.args[0]
        key_name = name[1:-1] if len(name) > 2 else name
        available_keys = '\n'.join(list(core.list_keys(self.data)))
        kwds = {
            'key_name': Color(key_name, '*red'),
            'dashed_line': Color('-' * 39, 'yellow'),
            'item_number': Color(self.item_number, 'red'),
            'operation': Color(self.operation, 'red'),
            'available_keys': Color(available_keys, 'white'),
            'key_list': Color(self.keylist, 'red')
        }
        return color_error_mesg(mesg, kwds, nocolor)
