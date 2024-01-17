from typing import Any, Dict

from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog

import great_expectations as ge


class DataValidationHooks:
    # Map checkpoint to dataset
    DATASET_CHECKPOINT_MAPPING = {
        "olist_order_items_dataset": "raw_order_items_checkpoint",
    }

    @hook_impl
    def before_node_run(
        self, catalog: DataCatalog, inputs: Dict[str, Any], session_id: str
    ) -> None:
        """Validate inputs data to a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        self._run_validation(catalog, inputs, session_id)

    @hook_impl
    def after_node_run(
        self, catalog: DataCatalog, outputs: Dict[str, Any], session_id: str
    ) -> None:
        """Validate outputs data from a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        self._run_validation(catalog, outputs, session_id)

    def _run_validation(
        self, catalog: DataCatalog, data: Dict[str, Any], session_id: str
    ):
        for dataset_name, dataset_value in data.items():
            if dataset_name not in self.DATASET_CHECKPOINT_MAPPING:
                continue

            data_context = ge.data_context.DataContext()

            data_context.run_checkpoint(
                checkpoint_name=self.DATASET_CHECKPOINT_MAPPING[dataset_name],
                batch_request={
                    "runtime_parameters": {
                        "batch_data": dataset_value,
                    },
                    "batch_identifiers": {
                        "runtime_batch_identifier_name": dataset_name
                    },
                },
                run_name=session_id,
            )