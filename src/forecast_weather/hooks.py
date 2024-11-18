#Add memory consumption tracking
import logging
from kedro.framework.hooks import hook_impl
from memory_profiler import memory_usage
from kedro.pipeline.node import Node
from typing import Any
import time


class LoggingHook:
    """A hook that logs how many time it takes to load each dataset."""

    def __init__(self):
        self._timers = {}

    @property
    def _logger(self):
        return logging.getLogger(__name__)

    @hook_impl
    def before_dataset_loaded(self, dataset_name: str, node: Node) -> None:
        start = time.time()
        self._timers[dataset_name] = start

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, data: Any, node: Node) -> None:
        start = self._timers[dataset_name]
        end = time.time()
        self._logger.info(
            "Loading dataset %s before node '%s' takes %0.2f seconds",
            dataset_name,
            node.name,
            end - start,
        )

def _normalise_mem_usage(mem_usage):
    # memory_profiler < 0.56.0 returns list instead of float
    return mem_usage[0] if isinstance(mem_usage, (list, tuple)) else mem_usage

#################################################################################################################
#################################################################################################################

class MemoryProfilingHooks:
    def __init__(self):
        self._mem_usage = {}

    @hook_impl
    def before_dataset_loaded(self, dataset_name: str) -> None:
        before_mem_usage = memory_usage(
            -1,
            interval=0.1,
            max_usage=True,
            retval=True,
            include_children=True,
        )
        before_mem_usage = _normalise_mem_usage(before_mem_usage)
        self._mem_usage[dataset_name] = before_mem_usage

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str) -> None:
        after_mem_usage = memory_usage(
            -1,
            interval=0.1,
            max_usage=True,
            retval=True,
            include_children=True,
        )
        # memory_profiler < 0.56.0 returns list instead of float
        after_mem_usage = _normalise_mem_usage(after_mem_usage)

        logging.getLogger(__name__).info(
            "Loading %s consumed %2.2fMiB memory",
            dataset_name,
            after_mem_usage - self._mem_usage[dataset_name],
        )

#################################################################################################################
#################################################################################################################
from typing import Any, Dict, Optional

from kedro.framework.hooks import hook_impl
from kedro.pipeline.node import Node
from kedro.io import DataCatalog


class NodeInputReplacementHook:
    @hook_impl
    def before_node_run(
        self, node: Node, catalog: DataCatalog
    ) -> Optional[Dict[str, Any]]:
        """Replace `input_row` for `my_node`"""
        if node.name == "forecast_params_row":
            # return the string filepath to the `first_input` dataset
            # instead of the underlying data
            dataset_name = "input_row"
            filepath = catalog._get_dataset(dataset_name)._filepath
            return {"input_row": filepath}  # `second_input` is not affected
        return None
    
#################################################################################################################
#################################################################################################################
#Add observability to your pipeline

# import sys
# from typing import Any, Dict

# import statsd
# from kedro.framework.hooks import hook_impl
# from kedro.pipeline.node import Node


# class PipelineMonitoringHooks:
#     def __init__(self):
#         self._timers = {}
#         self._client = statsd.StatsClient(prefix="kedro")

#     @hook_impl
#     def before_node_run(self, node: Node) -> None:
#         node_timer = self._client.timer(node.name)
#         node_timer.start()
#         self._timers[node.short_name] = node_timer

#     @hook_impl
#     def after_node_run(self, node: Node, inputs: Dict[str, Any]) -> None:
#         self._timers[node.short_name].stop()
#         for dataset_name, dataset_value in inputs.items():
#             self._client.gauge(dataset_name + "_size", sys.getsizeof(dataset_value))

#     @hook_impl
#     def after_pipeline_run(self):
#         self._client.incr("run")

# #################################################################################################################
# #################################################################################################################
# #Add metrics tracking to your model

# # src/<package_name>/hooks.py
# from typing import Any, Dict

# import mlflow
# import mlflow.sklearn
# from kedro.framework.hooks import hook_impl
# from kedro.pipeline.node import Node


# class ModelTrackingHooks:
#     """Namespace for grouping all model-tracking hooks with MLflow together."""

#     @hook_impl
#     def before_pipeline_run(self, run_params: Dict[str, Any]) -> None:
#         """Hook implementation to start an MLflow run
#         with the session_id of the Kedro pipeline run.
#         """
#         mlflow.start_run(run_name=run_params["session_id"])
#         mlflow.log_params(run_params)

#     @hook_impl
#     def after_node_run(
#         self, node: Node, outputs: Dict[str, Any], inputs: Dict[str, Any]
#     ) -> None:
#         """Hook implementation to add model tracking after some node runs.
#         In this example, we will:
#         * Log the parameters after the data splitting node runs.
#         * Log the model after the model training node runs.
#         * Log the model's metrics after the model evaluating node runs.
#         """
#         if node._func_name == "split_data":
#             mlflow.log_params(
#                 {"split_data_ratio": inputs["params:example_test_data_ratio"]}
#             )

#         elif node._func_name == "train_model":
#             model = outputs["example_model"]
#             mlflow.sklearn.log_model(model, "model")
#             mlflow.log_params(inputs["parameters"])

#     @hook_impl
#     def after_pipeline_run(self) -> None:
#         """Hook implementation to end the MLflow run
#         after the Kedro pipeline finishes.
#         """
#         mlflow.end_run()