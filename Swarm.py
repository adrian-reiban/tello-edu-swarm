"""
 # Author: Adrian Saul Reiban
 # Date: 23/08/2019
"""

from Tello import Tello
import threading
import time


class Swarm:

    RESPONSE_TIMEOUT = 10
    TIME_BETWEEN_COMMANDS = 1
    RETRIES = 2
    last_command_time_received = time.time()

    def __init__(self):
        # Creating Tello objects with their addresses and communication ports
        self.tello1 = Tello("Tello 1", '192.168.0.103', 8889, 9010)
        self.tello2 = Tello("Tello 2", '192.168.0.104', 8889, 9011)
        self.tello3 = Tello("Tello 3", '192.168.0.105', 8889, 9012)
        self.tello4 = Tello("Tello 4", '192.168.0.106', 8889, 9013)
        self.tello5 = Tello("Tello 5", '192.168.0.107', 8889, 9014)
        self.tello6 = Tello("Tello 6", '192.168.0.108', 8889, 9015)
        self.tello7 = Tello("Tello 7", '192.168.0.109', 8889, 9016)
        self.tello8 = Tello("Tello 8", '192.168.0.110', 8889, 9017)

        # Creating a list of Tello objects
        self.tellos = [self.tello1, self.tello2, self.tello3, self.tello4,
                       self.tello5, self.tello6, self.tello7, self.tello8]

        # Save the state of the timer, it can be True or False
        self.control_timer = False

    # This function changes the state of the time control variable, setting it to True
    def cancel_timer(self):
        self.control_timer = True

    # This function initializes the selected drones to accept control commands
    def start_mission(self, selected_drones):
        for i in range(len(selected_drones)):
            self.tellos[selected_drones[i]].send("command")
        self.simultaneous_checking_egalitarian_actions(selected_drones, "command")

    # Close the communication sockets of each of the drones
    def end_mission(self):
        time.sleep(5)
        for i in range(len(self.tellos)):
            self.tellos[i].close_sockets()

    # Function that allows you to enable the mission pads of the selected drones
    def enable_mission_pads(self, selected_drones):
        for i in range(len(selected_drones)):
            self.tellos[selected_drones[i]].send("mon")
        self.simultaneous_checking_egalitarian_actions(selected_drones, "mon")
        for j in range(len(selected_drones)):
            self.tellos[selected_drones[j]].send("mdirection 0")
        self.simultaneous_checking_egalitarian_actions(selected_drones, "mdirection 0")

    # Function that disables the detection of mission pads in selected drones
    def disable_mission_pads(self, selected_drones):
        for i in range(len(selected_drones)):
            self.tellos[selected_drones[i]].send("moff")
        self.simultaneous_checking_egalitarian_actions(selected_drones, "moff")

    # Function responsible for sending the same control commands to all drones
    def simultaneous_control_egalitarian_actions(self, selected_drones, command):
        # Wait a reasonable time to not saturate the communications
        diff = time.time() * 1000 - self.last_command_time_received
        if diff < self.TIME_BETWEEN_COMMANDS:
            time.sleep(diff)
        for j in range(len(selected_drones)):
            self.tellos[selected_drones[j]].send(command)
        self.simultaneous_checking_egalitarian_actions(selected_drones, command)
        self.last_command_time_received = time.time() * 1000

    # Function responsible for sending the different control messages to the respective drones
    def simultaneous_control_different_actions(self, selected_drones, commands):
        # Wait a reasonable time to not saturate the communications
        diff = time.time() * 1000 - self.last_command_time_received
        if diff < self.TIME_BETWEEN_COMMANDS:
            time.sleep(diff)
        for j in range(len(selected_drones)):
            self.tellos[selected_drones[j]].send(commands[j])
        self.simultaneous_checking_different_actions(selected_drones, commands)
        self.last_command_time_received = time.time() * 1000

    # Check if the common control messages have been executed; otherwise call the function in charge of forwarding
    # said messages (simultaneous_resending_egalitarian_actions)
    def simultaneous_checking_egalitarian_actions(self, selected_drones, command):
        visited = list()
        self.control_timer = False
        # Creating a timer that will work for the time set in RESPONSE_TIMEOUT and then call the cancel_timer function
        temp = threading.Timer(self.RESPONSE_TIMEOUT, self.cancel_timer)
        # Start temp
        temp.start()
        while len(visited) < len(selected_drones):
            if self.control_timer is True:
                break
            for i in range(len(selected_drones)):
                if selected_drones[i] not in visited:
                    if self.tellos[selected_drones[i]].response is not None:
                        visited.append(selected_drones[i])
                        self.tellos[selected_drones[i]].response = None
        temp.cancel()
        resend = list(set(selected_drones) - set(visited))
        visited = list()
        for j in range(len(resend)):
            if self.tellos[resend[j]].response is not None:
                visited.append(resend[j])
                self.tellos[resend[j]].response = None
        resend = list(set(resend) - set(visited))
        if len(resend) > 0:
            self.simultaneous_resending_egalitarian_actions(resend, command)

    # Function responsible for sending common messages to all drones
    def simultaneous_resending_egalitarian_actions(self, resend, command):
        for i in range(self.RETRIES):
            visited = list()
            for j in range(len(resend)):
                self.tellos[resend[j]].send(command)
            self.control_timer = False
            # Creating a timer that will work for the time set in RESPONSE_TIMEOUT and then call
            # the cancel_timer function
            temp = threading.Timer(self.RESPONSE_TIMEOUT, self.cancel_timer)
            # Start temp
            temp.start()
            while len(visited) < len(resend):
                if self.control_timer is True:
                    break
                for k in range(len(resend)):
                    if resend[k] not in visited:
                        if self.tellos[resend[k]].response is not None:
                            visited.append(resend[k])
                            self.tellos[resend[k]].response = None
            temp.cancel()
            resend = list(set(resend) - set(visited))
            visited = list()
            for l in range(len(resend)):
                if resend[l] not in visited:
                    if self.tellos[resend[l]].response is not None:
                        visited.append(resend[l])
                        self.tellos[resend[l]].response = None
            resend = list(set(resend) - set(visited))

    # Check if the common control messages have been executed; otherwise call the function in charge of forwarding
    # said messages (simultaneous_resending_different_actions)
    def simultaneous_checking_different_actions(self, selected_drones, commands):
        visited = list()
        self.control_timer = False
        # Creating a timer that will work for the time set in RESPONSE_TIMEOUT and then call the cancel_timer function
        temp = threading.Timer(self.RESPONSE_TIMEOUT, self.cancel_timer)
        # Start temp
        temp.start()
        while len(visited) < len(selected_drones):
            if self.control_timer is True:
                break
            for i in range(len(selected_drones)):
                if selected_drones[i] not in visited:
                    if self.tellos[selected_drones[i]].response is not None:
                        visited.append(selected_drones[i])
                        self.tellos[selected_drones[i]].response = None
        temp.cancel()
        resend = list(set(selected_drones) - set(visited))
        visited = list()
        for j in range(len(resend)):
            if self.tellos[resend[j]].response is not None:
                visited.append(resend[j])
                self.tellos[resend[j]].response = None
        resend = list(set(resend) - set(visited))
        if len(resend) > 0:
            self.simultaneous_resending_different_actions(resend, commands)

    # Function responsible for sending different messages to the respective drones
    def simultaneous_resending_different_actions(self, resend, commands):
        for i in range(self.RETRIES):
            visited = list()
            for j in range(len(resend)):
                self.tellos[resend[j]].send(commands[resend[j]])
            self.control_timer = False
            # Creating a timer that will work for the time set in RESPONSE_TIMEOUT and then call
            # the cancel_timer function
            temp = threading.Timer(self.RESPONSE_TIMEOUT, self.cancel_timer)
            # Start temp
            temp.start()
            while len(visited) < len(resend):
                if self.control_timer is True:
                    break
                for k in range(len(resend)):
                    if resend[k] not in visited:
                        if self.tellos[resend[k]].response is not None:
                            visited.append(resend[k])
                            self.tellos[resend[k]].response = None
            temp.cancel()
            resend = list(set(resend) - set(visited))
            visited = list()
            for l in range(len(resend)):
                if resend[l] not in visited:
                    if self.tellos[resend[l]].response is not None:
                        visited.append(resend[l])
                        self.tellos[resend[l]].response = None
            resend = list(set(resend) - set(visited))
