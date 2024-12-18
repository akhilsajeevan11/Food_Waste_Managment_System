
import time
from weighing_module.read_weighing_scale import WeightScale
from setup.setup import load_config

# Load configuration
config = load_config()
baud_rate = config['baud_rate']

weight_scale_port=config['weight_scale_port']



def extract_weight():
 # Initialize and read from weight scale
    weight_scale = WeightScale(weight_scale_port, baud_rate)
    weight_scale.connect()
    weight = None
    weight = weight_scale.read_weight()
    message = f"Weight: {weight} Kg"
    print(message)

    weight_scale.close()
    return weight



def extract_item_weight(initial_weight):
    # Initialize weight scale
    weight_scale = WeightScale(weight_scale_port, baud_rate)
    weight_scale.connect()
    
    print(f"Initial weight before image capture: {initial_weight} Kg")
    
    stable_weight = None
    stable_start_time = None
    last_known_weight = None
    timeout_start_time = time.time()
    
    while True:
        weight = weight_scale.read_weight()
        
        if weight is not None:
            last_known_weight = weight
            print(f"New weight reading: {weight} Kg")
            
            if weight > initial_weight:
                if stable_weight is None or weight == stable_weight:
                    if stable_start_time is None:
                        stable_start_time = time.time()
                    elif time.time() - stable_start_time >= 5:
                        print(f"Stable weight detected: {weight} Kg")
                        stable_weight = weight
                        break
                else:
                    stable_weight = weight
                    stable_start_time = time.time()
            else:
                stable_weight = None
                stable_start_time = None

        if time.time() - timeout_start_time >= 10:
            print("No stable weight detected within 10 seconds.")
            if last_known_weight is not None:
                stable_weight = last_known_weight
                break
            else:
                print("Error: No weight data available.")
                weight_scale.close()
                return None
        
        time.sleep(0.1)

    weight_scale.close()
    
    print(f"Initial weight: {initial_weight} Kg")
    print(f"Stable weight: {stable_weight} Kg")

    if stable_weight is not None:
        new_item_weight = stable_weight - initial_weight
        new_item_weight = float(new_item_weight)
        new_item_weight = round(new_item_weight, 3)
        print(f"New item weight: {new_item_weight} Kg")
        return new_item_weight
    else:
        print("Error: Could not determine a stable weight.")
        return None






# from weighing_module.process_weight import WeightScale
# from camera_module.process_image import capture_image
# import time

# def extract_item_weight(initial_weight):
#     # Initialize weight scale
#     weight_scale = WeightScale(weight_scale_port, baud_rate)
#     weight_scale.connect()
    
#     print(f"Initial weight before image capture: {initial_weight} Kg")
    
#     stable_weight = None
#     stable_start_time = None
#     last_known_weight = None
#     timeout_start_time = time.time()
    
#     while True:
#         weight = weight_scale.read_weight()
        
#         if weight is not None:
#             last_known_weight = weight
#             print(f"New weight reading: {weight} Kg")
            
#             # Check if the new weight is greater than the initial weight
#             if weight > initial_weight:
#                 if stable_weight is None or weight == stable_weight:
#                     # Check if the weight has been stable for at least 5 seconds
#                     if stable_start_time is None:
#                         stable_start_time = time.time()  # Start timer for stability
#                     elif time.time() - stable_start_time >= 5:
#                         print(f"Stable weight detected: {weight} Kg")
#                         stable_weight = weight
#                         break
#                 else:
#                     # Weight is varying, reset stability check
#                     stable_weight = weight
#                     stable_start_time = time.time()  # Reset timer if the weight changes
#             else:
#                 # Weight is not greater than the initial weight, continue monitoringso
#                 stable_weight = None
#                 stable_start_time = None

#         # Check for timeout
#         if time.time() - timeout_start_time >= 10:
#             print("No stable weight detected within 20 seconds.")
#             if last_known_weight is not None:
#                 stable_weight = last_known_weight
#                 break
#             else:
#                 print("Error: No weight data available.")
#                 weight_scale.close()
#                 return None
        
#         time.sleep(0.1)  # Short delay to prevent overwhelming the scale

#     weight_scale.close()
    
#     print(f"Initial weight: {initial_weight} Kg")
#     print(f"Stable weight: {stable_weight} Kg")

#     # Calculate the new item weight as the difference between initial weight and stable weight
#     if stable_weight is not None:
#         new_item_weight = stable_weight - initial_weight
#         new_item_weight = float(new_item_weight)
#         new_item_weight=round(new_item_weight,3)
#         print(f"New item weight: {new_item_weight} Kg")
#         return new_item_weight
#     else:
#         print("Error: Could not determine a stable weight.")
#         return None



