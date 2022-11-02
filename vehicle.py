import math

AIR_DENSITY = 1.29

# Electric motor functions
def peak_power(amperage, voltage, efficiency):
    return amperage * voltage * efficiency

def stall_torque(motor_constant, supply_voltage, armature_resistance, rpm):
    return (supply_voltage - rpm * motor_constant) / armature_resistance * motor_constant
    
def power_from_torque_rpm(torque, rpm):
    return torque * rpm * math.pi / 30

def torque_from_power_rpm(power, rpm):
    return (power * 30)/(math.pi * rpm)

def rpm_from_torque_power(torque, power):
    return (power * 30)/(math.pi * torque)

# Vehicle class
class Vehicle(object):
    def __init__(
        self, mass, cf_f, frontal_area,
        amperage, voltage, efficiency,
        K, wheel_radius
    ):
        self.mass = mass
        self.cf_d = 0.5 * cf_f * frontal_area * AIR_DENSITY
        self.cf_r = 0.01
        self.max_torque = stall_torque(K, voltage, voltage/amperage, 0)
        self.max_power = peak_power(amperage, voltage, efficiency)
        self.base_speed = rpm_from_torque_power(self.max_torque, self.max_power)
        
        self.traction = 0
        self.drag = 0
        self.rolling_resistance = 0
        self.longitudinal = 0
        
        self.wheel_radius = wheel_radius
        self.top_speed = ((2 * self.max_power) / (AIR_DENSITY * self.cf_d * frontal_area))**(1./3)
        self.differential = (4 * self.base_speed * 0.104719 * self.wheel_radius)/self.top_speed
        
        self.rpm = 0
        self.acceleration = 0
        self.velocity = 0
    
    def update(self):
        torque = self.max_torque if self.rpm < self.base_speed else torque_from_power_rpm(self.max_power, self.rpm)
        self.traction = (torque * self.differential) / self.wheel_radius
        self.drag = -self.cf_d * self.velocity * abs(self.velocity)
        self.rolling_resistance = -self.cf_r * self.mass * 9.81
        self.longitudinal = self.traction + self.drag + self.rolling_resistance
        self.acceleration = self.longitudinal / self.mass
        self.velocity += self.acceleration * 0.02
        self.rpm = (self.velocity / self.wheel_radius) * self.differential * 9.549296585513
        

if __name__ == "__main__":
    # Battery parameters
    amperage = 285 # in Amps
    voltage = 700 # in Volts
    efficiency = 0.96
    # Motor parameters
    K = 2.77 # Derived from rearranging key values found in the YASA-750 R spec sheet. Tested with multiple torque curves.
    
    car = Vehicle(1500, 0.3, 2.6, amperage, voltage, efficiency, K, 0.33)

    for i in range(10000):
        car.update()
        print(car.velocity * 3.6)
        
    print(f"Top speed: {car.top_speed * 3.6}")