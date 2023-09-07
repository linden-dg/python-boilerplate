import os
from dataclasses import dataclass

from dotenv import load_dotenv
import logging

from shared.utils import create_dir_if_not_exist

load_dotenv()

_ROOT_ = os.getenv("ROOT_PATH", f'{os.path.abspath(".")}\\⚡️data')


@dataclass(frozen=True)
class DataPaths:
    root: str = _ROOT_
    raw: str = os.getenv("RAW_PATH", f"{_ROOT_}\\🌱 raw")
    working: str = os.getenv("WORKING_PATH", f"{_ROOT_}\\🚧 working")
    outputs: str = os.getenv("OUTPUTS_PATH", f"{_ROOT_}\\🚀 outputs")
    logs: str = os.getenv("LOGS_PATH", f"{_ROOT_}\\🔧 logs")

    def get(self, path: str = "root") -> str:
        if path == "root":
            return getattr(self, "root")
        try:
            p = getattr(self, path)
            return f'{getattr(self, "root")}\\{p}'
        except AttributeError:
            logging.error(f"No path `{path}` found, defaulting to `root`")
            return getattr(self, "root")


@dataclass(frozen=True)
class AwsConfig:
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")


@dataclass(frozen=True)
class __DefaultConfig:
    log_level = os.getenv("log_level", logging.INFO)
    paths: DataPaths = DataPaths()
    aws: AwsConfig = AwsConfig()

    def __init__(self, settings=None):
        if settings is not None:
            # attach settings to the config
            self.__dict__["settings"] = {} | settings

        self._setup_paths()

    def _setup_paths(self) -> None:
        # Create working file directories
        for p in vars(self.paths).items():
            if p[0] != "root":
                create_dir_if_not_exist(p[1])

    def get_setting(self, setting: str):
        if "settings" not in self.__dict__:
            return None
        return self.settings[setting] if setting in self.settings else None

    def get_path(self, path: str = "root") -> str:
        return self.paths.get(path)


config = __DefaultConfig()

# %%
