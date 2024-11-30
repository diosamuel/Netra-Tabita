from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO('best1.pt')

# Run inference on a list of images
results = model(["test.jpg"])  # returns a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    result.show()  # display to screen
    
    # Iterate over the detected bounding boxes
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get the box coordinates as integers
        
        # Load the original image
        img = cv2.imread("test.jpg")
        
        # Crop the object using the bounding box coordinates
        cropped_object = img[y1:y2, x1:x2]
        
        # Save the cropped object as an image
        cv2.imwrite('hasilcrop.jpg', cropped_object)
    
    # Optionally save the entire result with bounding boxes
    result.save("result3.jpg")
