// Emergency Response Logic
const EMERGENCY_CONTACT = "+1234567890";
const TWILIO_ENDPOINT = "https://api.roadguard.ai/v1/emergency";

class RoadGuardApp {
    constructor() {
        this.isDriveActive = false;
        this.initSensors();
    }

    initSensors() {
        window.addEventListener('devicemotion', (event) => {
            const acc = event.accelerationIncludingGravity;
            // Send to C++ compiled WebAssembly for processing
            if (this.detectCrash(acc.x, acc.y, acc.z)) {
                this.triggerEmergencyProtocol();
            }
        });
    }

    detectCrash(x, y, z) {
        const force = Math.sqrt(x*x + y*y + z*z) / 9.8;
        return force > 4.5; // 4.5G spike
    }

    async triggerEmergencyProtocol() {
        this.showUnalertDialog();
        
        // 10 Second Countdown to abort
        const countdown = setTimeout(async () => {
            const location = await this.getCurrentLocation();
            await fetch(TWILIO_ENDPOINT, {
                method: 'POST',
                body: JSON.stringify({
                    phone: EMERGENCY_CONTACT,
                    msg: `CRASH DETECTED at ${location.mapsUrl}. Medical: B+`,
                    data: location
                })
            });
        }, 10000);
    }

    updateHUD(distance, ttc) {
        const alertBox = document.getElementById('alert-system');
        const speedEl = document.getElementById('speed');
        
        if (ttc < 2.0) {
            alertBox.classList.remove('hidden');
            window.navigator.vibrate([500, 200, 500]);
        } else {
            alertBox.classList.add('hidden');
        }
    }

    async getCurrentLocation() {
        return new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(pos => {
                resolve({
                    lat: pos.coords.latitude,
                    lng: pos.coords.longitude,
                    mapsUrl: `https://google.com/maps?q=${pos.coords.latitude},${pos.coords.longitude}`
                });
            });
        });
    }
}

const app = new RoadGuardApp();