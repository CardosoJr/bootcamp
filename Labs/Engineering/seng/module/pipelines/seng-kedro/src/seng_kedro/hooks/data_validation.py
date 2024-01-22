from typing import Any, Dict

from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog

import great_expectations as ge
from great_expectations.exceptions import ValidationError


class DataValidationHooks:
    def __init__(self):
        self.dataset_expectation_mapping = None
        self.context_root_dir = None
        self.break_on_error = False

    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog):
        self.dataset_expectation_mapping = catalog.load(
            "params:great_expectations.checkpoint_mapper"
        )
        self.context_root_dir = catalog.load(
            "params:great_expectations.context_root_dir"
        )
        self.break_on_error = catalog.load(
            "params:great_expectations.break_on_error"
        )

    @hook_impl
    def before_node_run(self, catalog: DataCatalog, inputs: Dict[str, Any], session_id: str) -> None:
        self._run_validation(catalog, inputs, session_id)

    @hook_impl
    def after_node_run(self, catalog: DataCatalog, outputs: Dict[str, Any], session_id: str) -> None:
        self._run_validation(catalog, outputs, session_id)

    def _run_validation(self, catalog: DataCatalog, data: Dict[str, Any], session_id: str):
        for dataset_name, dataset_value in data.items():
            if dataset_name not in self.dataset_expectation_mapping:
                continue

            # data_context = ge.data_context.DataContext(context_root_dir=self.context_root_dir)
            data_context = ge.data_context.DataContext(context_root_dir=self.context_root_dir)
            checkpoint_name = self.dataset_expectation_mapping[dataset_name]

            results = data_context.run_checkpoint(
                checkpoint_name=checkpoint_name,
                batch_request={
                    "runtime_parameters": {
                        "batch_data": dataset_value,
                    },
                    # "batch_identifiers": {
                    #     "runtime_batch_identifier_name": dataset_name
                    # },
                    "batch_identifiers": {
                        "default_identifier_name": "pandas_dataframe"
                    },
                },
                run_name=session_id,
            )

            if self.break_on_error and not results['success']:
                raise ValidationError(results)

