# encoding: utf-8

import collections
import functools
import math


def isnan(value):
    return value is None or math.isnan(value)


def reject(predicate, values):
    return filter(lambda value: not predicate(value), values)


def replace(string, mapping):
    for match, replacement in mapping.items():
        string = string.replace(match, replacement)
    return string


def bound(value, lower, upper):
    return max(lower, min(upper, value))


def repel(value):
    return math.copysign(max(abs(value), 1e-24), value)


def unwrap(fn):
    @functools.wraps(fn)
    def unwrapped_function(values, *vargs, **kwargs):
        scalar = not isinstance(values, collections.Iterable)

        if scalar:
            values = [values]

        results = fn(values, *vargs, **kwargs)

        if scalar:
            results = results[0]

        return results

    return unwrapped_function


def vectorize(fn):
    """
    Allows a method to accept a list argument, but internally deal only
    with a single item of that list.
    """

    @functools.wraps(fn)
    def vectorized_function(values, *vargs, **kwargs):
        return [fn(value, *vargs, **kwargs) for value in values]

    return vectorized_function
