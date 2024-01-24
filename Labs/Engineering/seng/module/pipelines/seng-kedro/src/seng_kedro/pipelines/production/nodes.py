from ..modeling.nodes import metrics_node

def mlflow_metrics(*data):
    """
    Other ways to log metrics in mlflow https://kedro-mlflow.readthedocs.io/en/stable/source/04_experimentation_tracking/05_version_metrics.html
    """
    metrics = metrics_node(*data)

    mlflow_metrics = {}

    for m,v in metrics.items():
        mlflow_metrics[m] = {"value" : v, "step" : 1}

    return mlflow_metrics