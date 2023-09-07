from datetime import datetime


def get_timestamp(time_format="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(time_format)


def get_today():
    return get_timestamp("%Y-%m-%d")


def get_now():
    return get_timestamp()


def get_file_friendly_timestamp():
    return get_timestamp("%Y-%m-%d T%H-%M-%S")
