import functools
import string

from hypothesis.errors import InvalidArgument
from hypothesis.strategies import (
    composite,
    integers,
    sampled_from,
    floats,
    text,
)
from hypothesis import strategies
from multimethod import overload
from collections.abc import Iterable
from typing import Callable

from hypothesis_csv.type_utils import *

valid_column_types = [
    integers,
    floats,
    functools.partial(
        text,
        min_size=1,
        max_size=10,
        alphabet=string.ascii_lowercase + string.ascii_uppercase + string.digits,
    ),
]


@overload
def get_columns(draw: isa(Callable), columns):
    raise InvalidArgument(
        "Columns parameter must either be an integer or a list of strategies"
    )


@overload
def get_columns(draw: isa(Callable), columns: isa(Iterable)):
    return columns


@overload
def get_columns(draw: isa(Callable), columns: isa(int)):
    columns = [draw(sampled_from(valid_column_types))() for _ in range(columns)]
    return columns


@overload
def get_columns(draw: isa(Callable), columns: is_none):
    return get_columns(draw, draw(integers(min_value=1, max_value=10)))


@overload
def get_lines_num(draw: isa(Callable), lines_param):
    raise InvalidArgument("Lines param must be an integer or None")


@overload
def get_lines_num(draw: isa(Callable), lines_param: is_none):
    return draw(integers(min_value=1, max_value=100))


@overload
def get_lines_num(draw: isa(Callable), lines_param: isa(int)):
    return lines_param


@composite
def data_rows(
    draw: Callable, lines: int | None = None, columns: int | list[strategies] = None
):
    lines_num = get_lines_num(draw, lines)
    columns = get_columns(draw, columns)
    rows = [tuple(draw(column) for column in columns) for _ in range(lines_num)]
    return rows
