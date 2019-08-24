from Swarm import Swarm
import time
import logging

# Configure a logging level
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

swarm = Swarm()

init_time = time.time()

swarm.start_mission([0, 1])

# Test of sending commands
# You can comment this block
for i in range(500):
    swarm.simultaneous_control_egalitarian_actions([0, 1], "speed?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "battery?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "time?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "height?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "temp?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "attitude?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "baro?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "acceleration?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "tof?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "wifi?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "sdk?")
    swarm.simultaneous_control_egalitarian_actions([0, 1], "sn?")


# Example
swarm.simultaneous_control_egalitarian_actions([0, 1], "speed 50")
swarm.simultaneous_control_egalitarian_actions([0, 1], "takeoff")

# Example 1
for _ in range(2):
    for _ in range(2):
        swarm.simultaneous_control_different_actions([0, 1], ["up 50", "forward 50"])
        swarm.simultaneous_control_different_actions([0, 1], ["down 50", "back 50"])

    swarm.simultaneous_control_egalitarian_actions([0, 1], "cw 180")

    for _ in range(2):
        swarm.simultaneous_control_different_actions([0, 1], ["up 50", "forward 50"])
        swarm.simultaneous_control_different_actions([0, 1], ["down 50", "back 50"])

    swarm.simultaneous_control_egalitarian_actions([0, 1], "cw 180")

# Example 2
swarm.simultaneous_control_egalitarian_actions([0, 1], "up 50")
swarm.simultaneous_control_different_actions([0, 1], ["up 50", "down 50"])
action1 = "down 100"
action2 = "up 100"
for _ in range(2):
    swarm.simultaneous_control_different_actions([0, 1], [action1, action2])
    aux = action1
    action1 = action2
    action2 = aux

swarm.simultaneous_control_different_actions([0, 1], ["down 50", "up 50"])

swarm.simultaneous_control_egalitarian_actions([0, 1], "land")
swarm.end_mission()

final_time = time.time() - init_time
logging.debug("The time elapsed is: %s " % final_time)
