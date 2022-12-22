import builtins
import inspect
from enum import Enum
from sqlalchemy_serializer import SerializerMixin


def get_leaf_attr(obj, attribute_locators: list) -> (bool, object):
    for attribute_locator in attribute_locators:
        obj = builtins.getattr(obj, attribute_locator, None)
        if obj is None:
            return False, None

    return True, obj


def is_match_of_types(obj, types: tuple):
    if not inspect.isclass(obj):
        return False

    is_match: bool = True
    for matching_type in types:
        is_match = issubclass(obj, matching_type)
        if not is_match:
            break

    return is_match


def object_to_dict(obj):
    if obj is None:
        return None
    elif isinstance(obj, list):
        data = []
        for element in obj:
            data.append(object_to_dict(element))
    elif isinstance(obj, dict):
        data = {}
        for key, value in obj.items():
            data[key] = object_to_dict(value)
    elif isinstance(obj, str):
        data = obj
    elif isinstance(obj, int):
        data = obj
    elif isinstance(obj, Enum):
        data = obj.value
    elif isinstance(obj, SerializerMixin):
        data = obj.to_dict()
    else:
        data = {}
        for key, value in obj.__dict__.items():
            data[key] = object_to_dict(value)

    return data
