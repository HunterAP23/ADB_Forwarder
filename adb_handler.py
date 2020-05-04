import json
import os.path as path
import socket
import subprocess as sp

import ipaddress

class ADB:
    def __init__(self):
        self.connect = None
        self.err_count = 0

        config_file = open("adb.json", "r")
        self.config = json.load(config_file)
        config_file.close()

        self.parse_config()

    def validate_adb_path(self):
        loc = path.abspath(self.config["location"])
        print("Got valid path \"{0}\".".format(self.config["location"]))
        if path.exists(loc):
            if path.isfile(loc):
                if "adb.exe" not in path.split(loc)[1]:
                    print("ERROR: \"{0}\" not a valid \"adb.exe\"".format(loc))
                    self.err_count += 1
                    return False
                print("Found \"adb.exe\" at \"{0}\"".format(loc))
                return True, loc
            else:
                print("ERROR: \"{0}\" is not a file.".format(loc))
                self.err_count += 1
                return False
        else:
            print("ERROR: \"{0}\" does not exist.".format(loc))
            self.err_count += 1
            return False

    def validate_adb(self):
        check = sp.Popen("{0} devices".format(self.config["location"]), stdout=sp.PIPE, stderr=sp.PIPE)
        out, err = check.communicate()
        out_lines = "\n".join(out.decode().strip().replace("List of devices attached", "").splitlines())
        if check.returncode == 0:
            if out_lines == "":
                print("ERROR: No devices found in ADB test, continuing for now...")
            return True
        else:
            return False

    # def validate_ip(self):
    #     try:
    #         socket.inet_aton(self.config["ip"])
    #         return True
    #     except socket.error:
    #         return False

    def validate_port(self):
        try:
            port = int(self.config["port"])
            if 1024 <= port and port <= 49151:
                return [True, None]
            else:
                return [False, True]
        except ValueError as ve:
            print(ve)
            return [False, False]

    def bind(self):
        cmd = "{0} forward tcp:{1} tcp:{1}".format(self.config["location"], int(self.config["port"]))
        self.connect = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        out, err = self.connect.communicate()
        if self.connect.returncode == 0:
            print("Port {0} should be forwarded correctly over ADB.".format(self.config["port"]))
        else:
            print("ERROR: Could not forwarding TCP port {0} through ADB.".format(self.config["port"]))
            print(err.decode().strip())

    def parse_config(self):
        print("Parsing config file...")
        if self.config["location"] == "None":
            print("ERROR: Location for \"adb.exe\" is not in the config.")
            self.err_count += 1
        else:
            print("Validating ADB file path...")
            adb_path_valid = self.validate_adb_path()
            if adb_path_valid:
                print("ADB file path is valid, testing ADB executable...")
                adb_valid = self.validate_adb()
                if adb_valid:
                    print("ADB executable is valid.")
                else:
                    print("ERROR: ADB executable is not valid.")

        # if self.config["ip"] == "None":
        #     print("No IP address found in the config.")
        #     self.err_count += 1
        # else:
        #     print("Validating IP address...")
        #     self.ip_valid = self.validate_ip()
        #     if self.ip_valid:
        #         print("IP Address {0} is valid.".format(self.config["ip"]))
        #     else:
        #         print("IP Address {0} is not valid.".format(self.config["ip"]))
        #         self.err_count += 1

        if self.config["port"] == "None":
            print("ERROR: Port not specified in the config.")
            self.err_count += 1
        else:
            port_valid = self.validate_port()
            if port_valid[0]:
                print("Port {0} is valid.".format(self.config["port"]))
            else:
                self.err_count += 1
                if port_valid[1]:
                    print("ERROR: Port {0} is not within the range of 1024 to 49151.".format(self.config["port"]))
                else:
                    print("ERROR: Port {0} is not an integer.".format(self.config["port"]))

        if self.err_count == 0:
            print("Config is as follows: ")
            for k, v in self.config.items():
                print("{0}: {1}".format(k, v))
            self.bind()
        else:
            print("Errors encountered when parsing the config. Please fix them and try running this program again.")


if __name__ == '__main__':
    my_adb = ADB()
