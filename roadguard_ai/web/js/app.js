class RoadGuardApp {
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
const app = new RoadGuardApp();