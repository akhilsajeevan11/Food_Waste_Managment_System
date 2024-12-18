from weighing_module.process_weight import extract_weight,extract_item_weight
from camera_module.process_image import capture_image
from detection_engine.food_model.food_model_inference import inference_food_model
from collections import Counter
import time
from setup.setup import load_model_config
def process_data():
    initial_weight = extract_weight()
    print("Initial weight is loaded")

    # filename=capture_image()

    # new_weight=extract_item_weight(initial_weight)

    input_filename='/home/suhail/FWMS/FWMS-1/Project/Project-v2/detection_engine/food_model/raw_image/4d318a1d0c_jpg.rf.41e926a8b26b5874235f675682355614.jpg'
    output_folder='/home/suhail/FWMS/FWMS-1/Project/Project-v2/detection_engine/food_model/annotated_image'

    config = load_model_config()
    output_folder = config['food_model_annoatation_dir']
    print(output_folder)

    food_model_result=inference_food_model(input_filename,output_folder)
 

    return True

