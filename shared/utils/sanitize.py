from shared.logging import getLogger

logger = getLogger(__name__)

_INVALID_CHARACTERS = ':*?"<>|\t\n\r\x0b\x0c'
_INVALID_FILENAME_CHARACTERS = _INVALID_CHARACTERS + "/\\"


def sanitize_filename(
    filename: str, replacement_text="_", invalid_characters=_INVALID_FILENAME_CHARACTERS
):
    sanitized_filename = _sanitize(filename, replacement_text, invalid_characters)
    return sanitized_filename


def sanitize_folder_path(
    folder_path: str,
    replacement_text="_",
    invalid_characters=_INVALID_CHARACTERS,
    folder_seperator="\\",
    max_folder_length=255,
):
    # standardise all slashes to one style
    path_parts = folder_path.replace("\\", "/").split("/")

    sanitized_parts = []
    for i, part in enumerate(path_parts):
        # if first item in path is a drive (`C:/`) or relative pathing (`./`) then don't sanitise
        if i == 0 and _check_root_path(part):
            sanitized_parts.append(part)
        else:
            sanitized_parts.append(
                _sanitize(part, replacement_text, invalid_characters)
            )

    # join back to `/` to check path length
    sanitized = "/".join(sanitized_parts)

    # max file/folder length for Windows
    if len(sanitized) > max_folder_length:
        logger.error(
            f"Folder Path - {sanitized} - exceeds max folder length of {max_folder_length} characters. "
            f"Trimming to max length - which may cause errors!!"
        )
        sanitized = sanitized[:255]

    # replace `/` with preferred folder_separator
    return sanitized.replace("/", folder_seperator)


def _check_root_path(path: str):
    if len(path) > 2:
        return False
    else:
        return True


def _sanitize(value: str, replacement_text="_", invalid_characters=_INVALID_CHARACTERS):
    # TODO: should probably be done with regex (re), but this was easier...
    sanitized = value
    for ch in invalid_characters:
        if ch in sanitized:
            sanitized = sanitized.replace(ch, replacement_text)
    # sanitized = "".join([replacement_text if c in invalid_characters else c for c in value])

    # max file/folder length for Windows
    sanitized = sanitized[:255]

    # Do not end a file or directory name with a space or a period
    sanitized = sanitized.rstrip(" .")

    return sanitized


def replace_line_breaks(string):
    return string.replace("\n", " ")
