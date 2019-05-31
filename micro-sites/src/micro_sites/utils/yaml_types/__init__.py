from typing import Type
import yaml


def initialise_types(loader: Type[yaml.Loader] = yaml.FullLoader, dumper: Type[yaml.Dumper] = yaml.Dumper) -> None:
    from .time_type import add_custom_type_time
    from .timedelta_type import add_custom_type_timedelta
    add_custom_type_time(loader, dumper)
    add_custom_type_timedelta(loader, dumper)
