from datetime import timedelta
import re
from typing import Optional, Type
import yaml
from .common import add_custom_type

TIMEDELTA_TAG = '!timedelta'
TIMEDELTA_REGEX = re.compile(
    r'^((?P<weeks>\d+?)w)?((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?$'
)


def format_timedelta(value: timedelta) -> str:
    seconds = value.seconds
    minutes = seconds // 60
    hours = minutes // 60
    weeks = value.days // 7
    days = value.days % 7
    hours %= 24
    minutes %= 60
    seconds %= 60
    s = ''
    if weeks:
        s += str(weeks) + 'w'
    if days:
        s += str(days) + 'd'
    if hours:
        s += str(hours) + 'h'
    if minutes:
        s += str(minutes) + 'm'
    if seconds:
        s += str(seconds) + 's'
    return s


def timedelta_representer(dumper: yaml.Dumper, data: timedelta) -> yaml.ScalarNode:
    return dumper.represent_scalar(TIMEDELTA_TAG, format_timedelta(data))


def parse_timedelta(value: str) -> Optional[timedelta]:
    parts = TIMEDELTA_REGEX.match(value)
    if not parts:
        return None
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


def timedelta_constructor(loader: yaml.Loader, node: yaml.ScalarNode) -> Optional[timedelta]:
    value = loader.construct_scalar(node)
    data = parse_timedelta(value)
    return data


def add_custom_type_timedelta(loader: Type[yaml.Loader], dumper: Type[yaml.Dumper]):
    add_custom_type(
        loader,
        dumper,
        timedelta,
        TIMEDELTA_TAG,
        timedelta_representer,
        timedelta_constructor,
        TIMEDELTA_REGEX
    )
