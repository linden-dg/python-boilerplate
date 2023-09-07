def create_dir_if_not_exist(path):
    import pathlib

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_attr(d: dict, key: str, default_value=""):
    return d[key] if key in d else default_value


def get_nonnull_attr(d: dict, key: str, default_value=""):
    attr = get_attr(d, key, default_value)
    return attr if attr is not None else default_value


def use_value(d: any, default_value=""):
    return d if d is not None else default_value
