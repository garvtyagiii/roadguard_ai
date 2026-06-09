import cv2  # pyright: ignore[reportMissingImports]
from ultralytics import YOLO  # pyright: ignore[reportMissingImports]

class VisionBrain:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')  # Nano version for mobile performance
        self.focal_length = 600          # Calibrated for standard smartphone sensors
        self.real_car_width = 1.8        # Meters

    def estimate_distance(self, bbox_width):
        # D = (W * F) / P
        return (self.real_car_width * self.focal_length) / bbox_width

    def process_frame(self, frame):
        results = self.model(frame, conf=0.5)
        detections = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if cls in [2, 3, 5, 7]: # Car, Motorcycle, Bus, Truck
                    x1, y1, x2, y2 = box.xyxy[0]
                    pixel_width = x2 - x1
                    distance = self.estimate_distance(pixel_width)
                    detections.append({
                        "class": cls,
                        "distance": round(float(distance), 2),
                        "box": [int(x1), int(y1), int(x2), int(y2)]
                    })
        return detections