import os

# Define folder structure
folders = [
    "roadguard_ai/engine",
    "roadguard_ai/vision",
    "roadguard_ai/web/css",
    "roadguard_ai/web/js"
]

# Define file contents
files = {
    "roadguard_ai/engine/physics.cpp": """#include <iostream>
#include <cmath>

class RoadGuardEngine {
private:
    const double MIN_TTC_THRESHOLD = 2.5; 
    const double CRASH_G_FORCE = 4.0;    

public:
    double calculateTTC(double dist, double relVel) {
        if (relVel <= 0) return 999.0; 
        return dist / relVel;
    }

    bool detectImpact(double accX, double accY, double accZ) {
        double magnitude = std::sqrt(accX * accX + accY * accY + accZ * accZ);
        double gForce = magnitude / 9.81;
        return gForce > CRASH_G_FORCE;
    }
};""",

    "roadguard_ai/vision/vision_brain.py": """import cv2
from ultralytics import YOLO

class VisionBrain:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.focal_length = 600          
        self.real_car_width = 1.8        

    def estimate_distance(self, bbox_width):
        return (self.real_car_width * self.focal_length) / bbox_width

    def process_frame(self, frame):
        results = self.model(frame, conf=0.5)
        # Logic to extract coordinates and distances
        return results""",

    "roadguard_ai/web/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="css/style.css">
    <title>RoadGuard AI HUD</title>
</head>
<body>
    <div id="hud-container">
        <div class="top-bar">
            <div class="speed-unit"><span id="speed">0</span><small>KM/H</small></div>
        </div>
        <canvas id="ar-overlay"></canvas>
        <video id="camera-feed" autoplay playsinline></video>
        <div id="alert-system" class="hidden"><h1>BRAKE NOW</h1></div>
    </div>
    <script src="js/app.js"></script>
</body>
</html>""",

    "roadguard_ai/web/js/app.js": """class RoadGuardApp {
    constructor() {
        this.initSensors();
    }

    initSensors() {
        window.addEventListener('devicemotion', (event) => {
            const acc = event.accelerationIncludingGravity;
            if (this.detectCrash(acc.x, acc.y, acc.z)) {
                console.log("CRASH DETECTED - Triggering Emergency Protocol");
            }
        });
    }

    detectCrash(x, y, z) {
        const force = Math.sqrt(x*x + y*y + z*z) / 9.8;
        return force > 4.5; 
    }
}
const app = new RoadGuardApp();""",

    "roadguard_ai/web/css/style.css": """body { background: #000; color: #00ffff; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
#hud-container { position: relative; width: 100vw; height: 100vh; }
.top-bar { position: absolute; top: 20px; left: 20px; border-left: 4px solid #00ffff; padding-left: 10px; }
#camera-feed { width: 100%; height: 100%; object-fit: cover; opacity: 0.6; }
.hidden { display: none; }
#alert-system { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(255,0,0,0.8); color: white; padding: 50px; border: 5px solid white; }"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}")

# Create files
for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)
    print(f"Created file: {path}")

print("\\n[SUCCESS] RoadGuard AI project structure generated.")