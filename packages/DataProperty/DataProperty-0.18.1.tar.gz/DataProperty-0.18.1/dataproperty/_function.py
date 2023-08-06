# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from decimal import Decimal
import decimal
import math

from mbstrdecoder import MultiByteStrDecoder


def is_empty_string(value):
    """
    This function will be deleted in the future.
    """

    try:
        return len(value.strip()) == 0
    except AttributeError:
        return True


def is_not_empty_string(value):
    """
    This function will be deleted in the future.
    """

    try:
        return len(value.strip()) > 0
    except AttributeError:
        return False


def get_integer_digit(value):
    from typepy.type import RealNumber

    decimal.setcontext(
        decimal.Context(prec=60, rounding=decimal.ROUND_HALF_DOWN))

    float_type = RealNumber(value)

    if not float_type.is_type():
        # bool-type/inf/nan value reaches this line
        raise ValueError(
            "the value must be a number: value='{}' type='{}'".format(
                value, type(value)))

    abs_value = abs(float_type.convert())

    if any([abs_value.is_nan(), abs_value.is_infinite()]):
        raise ValueError("invalid value '{}'".format(value))

    if abs_value.is_zero():
        return 1

    try:
        return len(str(abs_value.quantize(
            Decimal("1."), rounding=decimal.ROUND_DOWN)))
    except decimal.InvalidOperation as e:
        raise ValueError(e)


def _get_decimal_places(value):
    from collections import namedtuple
    from six.moves import range
    from typepy.type import Integer

    int_type = Integer(value)

    float_digit_len = 0
    if int_type.is_type():
        abs_value = abs(int_type.convert())
    else:
        abs_value = abs(float(value))
        text_value = str(abs_value)
        float_text = 0
        if text_value.find(".") != -1:
            float_text = text_value.split(".")[1]
            float_digit_len = len(float_text)
        elif text_value.find("e-") != -1:
            float_text = text_value.split("e-")[1]
            float_digit_len = int(float_text) - 1

    Threshold = namedtuple("Threshold", "pow digit_len")
    upper_threshold = Threshold(pow=-2, digit_len=6)
    min_digit_len = 1

    treshold_list = [
        Threshold(upper_threshold.pow + i, upper_threshold.digit_len - i)
        for i, _
        in enumerate(range(upper_threshold.digit_len, min_digit_len - 1, -1))
    ]

    abs_digit = min_digit_len
    for treshold in treshold_list:
        if abs_value < math.pow(10, treshold.pow):
            abs_digit = treshold.digit_len
            break

    return min(abs_digit, float_digit_len)


def get_number_of_digit(value):
    nan = float("nan")

    try:
        integer_digits = get_integer_digit(value)
    except (ValueError, TypeError, OverflowError):
        return (nan, nan)

    try:
        decimal_places = _get_decimal_places(value)
    except (ValueError, TypeError):
        decimal_places = nan

    return (integer_digits, decimal_places)


def is_multibyte_str(text):
    from typepy import StrictLevel
    from typepy.type import String

    if not String(text, strict_level=StrictLevel.MIN).is_type():
        return False

    try:
        unicode_text = MultiByteStrDecoder(text).unicode_str
    except ValueError:
        return False

    try:
        unicode_text.encode("ascii")
    except UnicodeEncodeError:
        return True

    return False


def get_ascii_char_width(unicode_str, east_asian_ambiguous_width=1):
    import unicodedata

    width = 0
    for c in unicode_str:
        char_width = unicodedata.east_asian_width(c)
        if char_width in "WF":
            width += 2
        elif char_width == "A":
            width += east_asian_ambiguous_width
        else:
            width += 1

    return width
