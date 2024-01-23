from mlflow.models import Model
from module.models.model import PipelineModel
from mlflow.models.model import MLMODEL_FILE_NAME
from pathlib import Path
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
import module

FLAVOR_NAME = "custom_flavor"


# options commented out are not necessary
def save_model(
    fake_model: PipelineModel,
    path,
    # conda_env=None,
    mlflow_model=None,
    # code_paths=None,
    # signature: ModelSignature = None,
    # input_example: ModelInputExample = None,
    # requirements_file=None,
    # extra_files=None,
    # pip_requirements=None,
    # extra_pip_requirements=None,
):

    path = Path(path).resolve()
    path.mkdir(parents=True, exist_ok=True)

    mlflow_mlmodel_file_path = path / MLMODEL_FILE_NAME
    model_subpath = path / "model.pkl"
    if mlflow_model is None:
        mlflow_model = Model()
    mlflow_model.add_flavor(FLAVOR_NAME, foo=123, bar="abc", offset=fake_model.offset)
    mlflow_model.save(mlflow_mlmodel_file_path)
    fake_model.save(model_subpath)


def load_model(model_uri, dst_path=None):
    local_model_path = _download_artifact_from_uri(
        artifact_uri=model_uri, output_path=dst_path
    )
    model_subpath = Path(local_model_path) / "model.pkl"
    return PipelineModel.load(model_subpath)


def log_model(
    model: PipelineModel,
    artifact_path,
    # conda_env=None,
    # code_paths=None,
    # registered_model_name=None,
    # signature: ModelSignature = None,
    # input_example: ModelInputExample = None,
    # pip_requirements=None,
    # extra_pip_requirements=None,
    **kwargs,
):
    return Model.log(
        artifact_path=str(artifact_path),  # must be string, numbers etc
        flavor= module.models.custom_flavor,  # points to this module itself
        # registered_model_name=registered_model_name,
        fake_model=model,
        # conda_env=conda_env,
        # code_paths=code_paths,
        # signature=signature,
        # input_example=input_example,
        # pip_requirements=pip_requirements,
        # extra_pip_requirements=extra_pip_requirements,
        **kwargs,
    )