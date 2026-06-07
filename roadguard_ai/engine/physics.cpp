#include <iostream>
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
};