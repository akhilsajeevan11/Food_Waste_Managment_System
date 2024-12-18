
from setup.setup import load_model_config
import ultralytics
from ultralytics import YOLO

def load_food_model():
    config = load_model_config()
    food_model = config['food_model']

    version=ultralytics.__version__
    model_config={
        "ultralytics_vesion":version,
        "model":food_model
    }

    food_model = YOLO(food_model)
    print("Model Loaded",model_config)

    return food_model