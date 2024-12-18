import os
import numpy as np  # Import NumPy
from PIL import Image
import cv2
from ultralytics import YOLO


#load Model
from detection_engine.load_model import load_food_model



food_model = load_food_model()

# Define font parameters
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.7
thickness = 1  # Adjusted thickness for contour
line_type = cv2.LINE_AA

# Define the color for the outline (white)
outline_color = (255, 255, 255)  # White color
rectangle_color = (255, 255, 255)  # White color for rectangle

def inference_food_model(input_image, output_folder, item_weight=0.35, total_weight=12.3):
    # Ensure output folder exists
    # os.makedirs(output_folder, exist_ok=True)
    # Load the image using OpenCV
    frame = cv2.imread(input_image)
 
    # Resize the image to 512x512
    frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_AREA)
 
    # Perform prediction
    results = food_model.predict(frame, save=False, imgsz=512, conf=0.5)
 
    # Check if any results are returned
    if not results or not results[0].boxes.xyxy.cpu().numpy().size:
        print("No detections found.")
        return "no_detection"
 
    # Iterate through the results
    for result in results:
        # Move the tensor to the CPU before converting to numpy
        boxes = result.boxes.xyxy.cpu().numpy()
 
        # Check if masks are available
        if result.masks is not None:
            masks = result.masks.data.cpu().numpy()  # Assuming masks are in result.masks.data
 
            for i, box in enumerate(boxes):
                # Get the corresponding mask
                mask = masks[i]
             
                # Remove single-dimensional entries from the shape
                mask = mask.squeeze()  # if needed, based on the mask dimensions
 
                # Resize the mask to match the original image size
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
 
                # Threshold the mask to get a binary mask
                _, binary_mask = cv2.threshold(mask, 0.5, 1, cv2.THRESH_BINARY)
 
                # Convert the binary mask to an 8-bit format
                binary_mask = (binary_mask * 255).astype(np.uint8)
 
                # Find contours in the binary mask
                contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
                # Draw the white outline around the contours
                cv2.drawContours(frame, contours, -1, outline_color, thickness=thickness)
 
    # Display weight and other details
    info_text = f"Item weight: {item_weight:.2f}kg \n Total weight: {total_weight:.2f}kg"
    info_pos = (10, frame.shape[0] - 50)
 
 
    # Put text inside the rectangle
    cv2.putText(frame, info_text, info_pos, font, font_scale, (255, 255, 255), thickness, line_type)
 
    # Save the annotated image to the output folder with the same name
    output_img_path = os.path.join(output_folder, os.path.basename(input_image))
    cv2.imwrite(output_img_path, frame)  # Save the image using OpenCV
 
    print(f"Processed {os.path.basename(input_image)}")
    return "success"    


# # Path to your input image and output folder
# input_image = '/Users/suhail/Desktop/Suhail/Workspace/Project_Workspace_2024/Projects/FWMS/Project/Version-1/food-model/Test/2397826HA-R_345.png'
# output_folder = '/Users/suhail/Desktop/Suhail/Workspace/Project_Workspace_2024/Projects/FWMS/Project/Version-1/food-model/Anoted_Images'

# # Process the image with item and total weight displayed
# result = inference_food_model(input_image, output_folder)
# print(f"Result: {result}")
