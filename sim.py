import math
from matplotlib import pyplot as plt

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

if __name__ == "__main__":
    # Battery parameters
    amperage = 285 # in Amps
    voltage = 700 # in Volts
    efficiency = 0.96
    
    # Motor parameters            
    K = 2.77 # Derived from rearranging key values found in the YASA-750 R spec sheet. Tested with multiple torque curves.
    max_torque = stall_torque(K, voltage, voltage/amperage, 0)
    max_power = peak_power(amperage, voltage, efficiency)
    base_speed = rpm_from_torque_power(max_torque, max_power)

    rpm, torque, power = [], [], []

    for i in range(3250):
        rpm.append(i)
        t = max_torque if i < base_speed else torque_from_power_rpm(max_power, i)
        p = power_from_torque_rpm(t, i) / 1000
        torque.append(t)
        power.append(p)

    plt.plot(rpm, torque)
    plt.plot(rpm, power)
    plt.xlabel("RPM")
    plt.ylabel("Torque (Nm) / Power (kW)")
    plt.show()