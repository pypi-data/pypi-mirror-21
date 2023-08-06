# -*- coding: utf-8 -*-
"""These preprocessor functions are used to process data prior to output."""

from decimal import Decimal
import string

from cli_helpers import utils
from cli_helpers.compat import text_type


def convert_to_string(data, headers, **_):
    """Convert all *data* and *headers* to strings.

    Binary data that cannot be decoded is converted to a hexadecimal
    representation via :func:`binascii.hexlify`.

    :param iterable data: An :term:`iterable` (e.g. list) of rows.
    :param iterable headers: The column headers.
    :return: The processed data and headers.
    :rtype: tuple

    """
    return ([[utils.to_string(v) for v in row] for row in data],
            [utils.to_string(h) for h in headers])


def override_missing_value(data, headers, missing_value='', **_):
    """Override missing values in the *data* with *missing_value*.

    A missing value is any value that is :data:`None`.

    :param iterable data: An :term:`iterable` (e.g. list) of rows.
    :param iterable headers: The column headers.
    :param missing_value: The default value to use for missing data.
    :return: The processed data and headers.
    :rtype: tuple

    """
    return ([[missing_value if v is None else v for v in row] for row in data],
            headers)


def bytes_to_string(data, headers, **_):
    """Convert all *data* and *headers* bytes to strings.

    Binary data that cannot be decoded is converted to a hexadecimal
    representation via :func:`binascii.hexlify`.

    :param iterable data: An :term:`iterable` (e.g. list) of rows.
    :param iterable headers: The column headers.
    :return: The processed data and headers.
    :rtype: tuple

    """
    return ([[utils.bytes_to_string(v) for v in row] for row in data],
            [utils.bytes_to_string(h) for h in headers])


def align_decimals(data, headers, **_):
    """Align numbers in *data* on their decimal points.

    Whitespace padding is added before a number so that all numbers in a
    column are aligned.

    Outputting data before aligning the decimals::

        1
        2.1
        10.59

    Outputting data after aligning the decimals::

         1
         2.1
        10.59

    :param iterable data: An :term:`iterable` (e.g. list) of rows.
    :param iterable headers: The column headers.
    :return: The processed data and headers.
    :rtype: tuple

    """
    pointpos = len(headers) * [0]
    for row in data:
        for i, v in enumerate(row):
            if isinstance(v, Decimal):
                v = text_type(v)
                pointpos[i] = max(utils.intlen(v), pointpos[i])
    results = []
    for row in data:
        result = []
        for i, v in enumerate(row):
            if isinstance(v, Decimal):
                v = text_type(v)
                result.append((pointpos[i] - utils.intlen(v)) * " " + v)
            else:
                result.append(v)
        results.append(result)
    return results, headers


def quote_whitespaces(data, headers, quotestyle="'", **_):
    """Quote leading/trailing whitespace in *data*.

    When outputing data with leading or trailing whitespace, it can be useful
    to put quotation marks around the value so the whitespace is more
    apparent. If one value in a column needs quoted, then all values in that
    column are quoted to keep things consistent.

    .. NOTE::
       :data:`string.whitespace` is used to determine which characters are
       whitespace.

    :param iterable data: An :term:`iterable` (e.g. list) of rows.
    :param iterable headers: The column headers.
    :param str quotestyle: The quotation mark to use (defaults to ``'``).
    :return: The processed data and headers.
    :rtype: tuple

    """
    whitespace = tuple(string.whitespace)
    quote = len(headers) * [False]
    for row in data:
        for i, v in enumerate(row):
            v = text_type(v)
            if v.startswith(whitespace) or v.endswith(whitespace):
                quote[i] = True

    results = []
    for row in data:
        result = []
        for i, v in enumerate(row):
            quotation = quotestyle if quote[i] else ''
            result.append('{quotestyle}{value}{quotestyle}'.format(
                quotestyle=quotation, value=v))
        results.append(result)
    return results, headers
