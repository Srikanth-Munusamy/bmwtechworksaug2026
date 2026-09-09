import json
import os

import joblib
import numpy as np


def model_fn(model_dir):
    model_file = os.path.join(
        model_dir,
        "model.joblib",
    )

    return joblib.load(model_file)


def input_fn(request_body, content_type):
    if content_type != "application/json":
        raise ValueError(
            "Only application/json is supported."
        )

    request = json.loads(request_body)

    return np.asarray(
        request["instances"],
        dtype=float,
    )


def predict_fn(input_data, model):
    return model.predict(input_data)


def output_fn(prediction, accept):
    response = {
        "predictions": prediction.tolist()
    }

    return (
        json.dumps(response),
        "application/json",
    )