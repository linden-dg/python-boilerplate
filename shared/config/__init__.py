import os
from dataclasses import dataclass, field

from dotenv import load_dotenv
import logging

from shared.utils import create_dir_if_not_exist


# Load Local Environment Variables
_local_env = os.path.join(os.path.abspath("."), ".env")
if os.path.exists(_local_env):
    load_dotenv(_local_env)

# Load Root Environment Variables
_root_env = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../.env"))
if os.path.exists(_root_env):
    load_dotenv(_root_env)

# Load Shared Environment Variables
load_dotenv(
    os.path.normpath(os.path.join(os.path.dirname(__file__), "../../.env.shared"))
)


@dataclass(frozen=True)
class DataPaths:
    root: str = os.getenv("ROOT_PATH", os.path.abspath("."))
    data_root: str = field(init=False)
    raw: str = field(init=False)
    working: str = field(init=False)
    outputs: str = field(init=False)
    logs: str = field(init=False)

    def __post_init__(self):
        _data_root = os.getenv("DATA_ROOT_PATH", os.path.join(self.root, "⚡️data"))
        object.__setattr__(self, "data_root", _data_root)
        object.__setattr__(
            self, "raw", os.getenv("RAW_PATH", os.path.join(_data_root, "🌱 raw"))
        )
        object.__setattr__(
            self,
            "working",
            os.getenv("WORKING_PATH", os.path.join(_data_root, "🚧 working")),
        )
        object.__setattr__(
            self,
            "outputs",
            os.getenv("OUTPUTS_PATH", os.path.join(_data_root, "🚀 outputs")),
        )
        object.__setattr__(
            self, "logs", os.getenv("LOGS_PATH", os.path.join(_data_root, "🔧 logs"))
        )

    def _get_path(self, path: str) -> str:
        if path == "root":
            return getattr(self, "root")
        try:
            return getattr(self, path)
        except AttributeError:
            logging.error(f"No path `{path}` found, defaulting to `root`")
            return getattr(self, "root")

    def get(self, path: str = "root", subfolder: str = None) -> str:
        return os.path.normpath(
            f"{self._get_path(path)}/{subfolder}" if subfolder else self._get_path(path)
        )


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

    def get_path(self, path: str = "root", subfolder: str = None) -> str:
        return self.paths.get(path, subfolder)


# %%
config = __DefaultConfig()
