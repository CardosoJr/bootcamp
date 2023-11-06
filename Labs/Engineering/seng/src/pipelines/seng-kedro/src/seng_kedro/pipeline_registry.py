"""Project pipelines."""
from __future__ import annotations
from kedro.io import DataCatalog
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from seng_kedro.pipelines.data_preprocessing.pipeline import create_pipeline as dp_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    # """Register the project's pipelines.

    # Returns:
    #     A mapping from pipeline names to ``Pipeline`` objects.
    # """
    # pipelines = find_pipelines()
    # pipelines["__default__"] = sum(pipelines.values())
    # return pipelines

    """Method that will be assigned to the callable returned by register_dynamic_pipelines(...), by a Hook."""
    raise NotImplementedError("""
        register_pipelines() is expected to be overwritten by ProjectHooks.
        Make sure the hooks is found in hooks.py and enabled in settings.py
        """)

def register_dynamic_pipelines(catalog: DataCatalog) -> dict[str, Pipeline]:
    """Register the project's pipelines depending on the catalog.

    Create pipelines dynamically based on parameters and datasets defined in the catalog.
    The function must return a callable without any arguments that will replace the
    `register_pipelines()` method in this same module, using an `after_catalog_created_hook`.

    Args:
        catalog: The DataCatalog loaded from the KedroContext.

    Returns:
        A callable that returns a mapping from pipeline names to ``Pipeline`` objects.
    """
    # create pipelines with access to catalog
    preprocessing_pipeline = dp_pipeline(catalog = catalog)
    
    def register_pipelines():
        """Register the project's pipelines.

        Returns:
            A mapping from pipeline names to ``Pipeline`` objects.
        """
        pipelines = {
            "preprocessing_pipeline": preprocessing_pipeline,
        }
        pipelines["__default__"] = sum(pipelines.values())
        return pipelines

    return register_pipelines