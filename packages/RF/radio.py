import Jetson.GPIO as gpio
from subprocess import Popen, PIPE# like bash scripting, but in python :)

class antenna:

    def __init__():
        # contains the current antenna in use, and sets the 
        self.currentAntenna = 1
        self.gpioV1 = 15
        self.gpioV2 = 16

        gpio.output([15,16], gpio.LOW)  # initial state is RF1

    def rssi_dict():
        """
        # Using the iwlist application provided by pre-installed linux packages,
        # scan the WiFi range, and create a dictionary that contains the SSID of
        # each AP, along with its RSSI and center frequency/channel in a list.
        #
        # Inputs: 
        #   void
        #
        # Returns:
        #   cell_list: dict, with format {(ssid: str): [(rssi: int), (freq: str)]}
        """

        cmd_out, cmd_err = Popen(["iwlist", "wlan0", "scan"], stdout=PIPE).communicate()

        cell_list = dict()
        num = 1
        for chunk in str(cmd_out).split("Cell"):
            
            ssid = ""
            rssi = 0
            freq = ""

            for line in chunk.split("\\n"):

                stripped_line = line.strip(" ")
                if "Frequency" in stripped_line:
                    freq = stripped_line[10:19]
                elif "ESSID" in stripped_line:
                    ssid = stripped_line[6:].strip('"')
                elif "Signal level" in stripped_line:
                    rssi = int(stripped_line[28:32].strip(" "))

            cell_list.update(ssid: [rssi,freq])

        return cell_list


    # this method will implement the RF switch to the next antenna
    def next_antenna():
        """
        # NOT TESTED: connect to scope and test if output works
        # 
        # With the Jetson.GPIO package, determine what antenna we are using
        # might change this in order to take an antenna number or something :/
        #
        """

        self.currentAntenna = (self.currentAntenna) % 4 + 1

        if self.currentAntenna == 1:
            gpio.output([self.gpioV1, self.gpioV2], gpio.LOW)
        elif self.currentAntenna == 2:
            gpio.output(self.gpioV1, gpio.HIGH)
            gpio.output(self.gpioV2, gpio.LOW)
        elif self.currentAntenna == 3:
            gpio.output(self.gpioV1, gpio.LOW)
            gpio.output(self.gpioV2, gpio.HIGH)
        else:
            gpio.output(self.gpioV1, gpio.HIGH)
            gpio.output(self.gpioV2, gpio.HIGH)
