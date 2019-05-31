from datetime import time
import re
from typing import Type
import yaml
from .common import add_custom_type

TIME_TAG = '!time'
TIME_REGEX = re.compile(
    r'^(?P<hour>[0-9][0-9]?):(?P<minute>[0-9][0-9]):(?P<second>[0-9][0-9])(?:\.(?P<fraction>[0-9]*))$', re.X)


def time_representer(dumper: yaml.Dumper, data: time) -> yaml.ScalarNode:
    return dumper.represent_scalar(TIME_TAG, data.isoformat())


def time_constructor(loader: yaml.Loader, node: yaml.ScalarNode) -> time:
    value = loader.construct_scalar(node)
    data = time.fromisoformat(value)
    return data


def add_custom_type_time(loader: Type[yaml.Loader], dumper: Type[yaml.Dumper]):
    add_custom_type(loader, dumper, time, TIME_TAG, time_representer, time_constructor, TIME_REGEX)
