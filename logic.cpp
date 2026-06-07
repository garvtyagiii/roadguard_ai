#include <iostream>
#include <cmath>
#include <vector>

struct Telemetry {
    double distance;      // meters
    double relativeSpeed; // m/s
    double acceleration;  // m/s^2
};

class RoadGuardEngine {
private:
    const double MIN_TTC_THRESHOLD = 2.5; // Seconds before alert
    const double CRASH_G_FORCE = 4.0;    // G-unit threshold

public:
    // Calculates Time-To-Collision
    double calculateTTC(double dist, double relVel) {
        if (relVel <= 0) return 999.0; // Target is moving away
        return dist / relVel;
    }

    // Detects Impact based on sensor spikes
    bool detectImpact(double accX, double accY, double accZ) {
        double magnitude = std::sqrt(accX * accX + accY * accY + accZ * accZ);
        double gForce = magnitude / 9.81;
        return gForce > CRASH_G_FORCE;
    }

    // Safety Score Algorithm
    double updateSafetyScore(int harshBrakes, int overspeedEvents) {
        double score = 100.0 - (harshBrakes * 5.0) - (overspeedEvents * 2.0);
        return (score < 0) ? 0 : score;
    }
};