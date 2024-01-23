"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://kedro.readthedocs.io/en/stable/kedro_project_setup/settings.html."""

# Import module
from pathlib import Path
import sys
parent_dir = Path(__file__).resolve().parents[5]
sys.path.append(str(parent_dir))

from seng_kedro.hooks import proj_hooks, data_validation
from kedro_mlflow.framework.hooks import MlflowHook

HOOKS = (proj_hooks.ProjectHooks(), 
         data_validation.DataValidationHooks(),
         MlflowHook(),)

from kedro.config import OmegaConfigLoader  # noqa: import-outside-toplevel

CONFIG_LOADER_CLASS = OmegaConfigLoader

from kedro_viz.integrations.kedro.sqlite_store import SQLiteStore
SESSION_STORE_CLASS = SQLiteStore
SESSION_STORE_ARGS = {"path": str(Path(__file__).parents[2] / "data")}

# Instantiated project hooks.
# For example, after creating a hooks.py and defining a ProjectHooks class there, do
# from seng_kedro.hooks import ProjectHooks
# Hooks are executed in a Last-In-First-Out (LIFO) order.
# HOOKS = (ProjectHooks(),)

# Installed plugins for which to disable hook auto-registration.
# DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)

# Class that manages storing KedroSession data.
# from kedro.framework.session.store import BaseSessionStore
# SESSION_STORE_CLASS = BaseSessionStore
# Keyword arguments to pass to the `SESSION_STORE_CLASS` constructor.
# SESSION_STORE_ARGS = {
#     "path": "./sessions"
# }

# Directory that holds configuration.
# CONF_SOURCE = "conf"

# Class that manages how configuration is loaded.

# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
# CONFIG_LOADER_ARGS = {
#       "config_patterns": {
#           "spark" : ["spark*/"],
#           "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
#       }
# }

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog