import argparse as argp
import json
import os
from pathlib import Path
import socket
import shlex
import subprocess as sp

from typing import Union


class ADB:
    def __init__(self):
        self.connect = None
        self._config = None
        self._adb = None
        self._port = None

        self._args = vars(self._parse_arguments())

        try:
            self._config_set()
            self._validate_adb()
            self._validate_port()
            self.bind()
        except Exception as e:
            print(e)
            exit(1)

    def _parse_arguments(self):
        main_help = "Port Forwarding tool for Android Devices over USB.\n"
        parser = argp.ArgumentParser(description=main_help, formatter_class=argp.RawTextHelpFormatter, add_help=False)

        optional_args = parser.add_argument_group("Optional arguments")
        adb_help = "The path to the ADB executable.\n"
        adb_help += "The path must point to the executable itself.\n\n"
        optional_args.add_argument("-a", "--adb", dest="adb", help=adb_help)

        port_help = "The port to forward between your Android device and the connected PC.\n"
        port_help += "The port must be the same one used by the \"IP Webcam\" app on your android device.\n\n"
        optional_args.add_argument("-p", "--port", dest="port", help=port_help)

        misc_args = parser.add_argument_group("Miscellaneous arguments")
        misc_args.add_argument("-h", "--help", action="help", default=argp.SUPPRESS, help="Show this help message and exit.\n")
        args = parser.parse_args()
        return args

    def _config_set(self) -> None:
        try:
            config_file = open("adb.json", "r")
            self._config = json.load(config_file)
            config_file.close()

            print("Config is as follows: ")
            for k, v in self._config.items():
                print("\t{0}: {1}".format(k, v))
        except json.JSONDecodeError as jde:
            msg = "ERROR: Issue parsing file {}.\n"
            msg += "Location of error in file: {}\n"
            msg += "Line: {}\n"
            msg += "Column: {}\n"
            msg += "Please fix them and try running this program again."
            print(msg.format(jde.doc, jde.pos, jde.lineno, jde.colno))
            exit(1)

    def _run_sp(self, cmd: Union[list, str, tuple]) -> tuple:
        if type(cmd) == str:
            cmd = shlex.split(cmd)

        proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        out, err = proc.communicate()
        return (out, err, proc.returncode)

    def _validate_adb(self) -> None:
        adb_execs = []
        if self._args["adb"] is not None:
            adb_execs.append(self._args["adb"])
        if self._config["location"] != "None":
            adb_execs.append(self._config["location"])

        if len(adb_execs) == 0:
            raise ValueError("User did not specify an ADB executable file in the arguments or the config file.")

        print("Validating ADB file path...")
        for i in range(len(adb_execs)):
            print("Checking \"{}\"".format(adb_execs[i]))
            try:
                loc = Path(adb_execs[i])
                if loc.exists():
                    if loc.is_file():
                        if "adb" not in loc.name:
                            raise OSError("ERROR: \"{0}\" is not named \"adb\".".format(loc))
                        if os.access(loc, os.X_OK):
                            print("Found \"adb\" executable at \"{0}\"".format(loc))
                            self._adb = loc
                        else:
                            raise OSError("ERROR: \"{0}\" does not have execute permissions".format(loc))
                    else:
                        raise IsADirectoryError("ERROR: \"{0}\" is not a file.".format(loc))
                else:
                    raise FileNotFoundError("ERROR: \"{0}\" does not exist.".format(loc))

                print("Testing ADB executable...")
                cmd = "{} devices".format(repr(str(self._adb)))
                check = self._run_sp(cmd)
                if check[2] == 0:
                    msg = "ADB executable is valid"
                    out_lines = "\n".join(check[0].decode().strip().replace("List of devices attached", "").splitlines())
                    if out_lines == "":
                        msg += " but no devices ADB-capable devices were found, continuing for now..."
                    else:
                        msg += "."
                    print(msg)
                    return
                else:
                    msg = "ERROR: ADB executable had an error.\n"
                    msg += "Stdout: {}\n".format(check[0].decode().strip())
                    msg += "Stderr: {}\n".format(check[1].decode().strip())
                    msg += "Return Code: {}".format(check[2])
                    raise OSError(msg)
            except Exception as e:
                print(e)
                if i + 1 == len(adb_execs):
                    print("ERROR: Could not find ADB executable, this program will now exit.")
                    exit(1)

    def _validate_port(self) -> None:
        ports = []
        if self._args["port"] is not None:
            ports.append(self._args["port"])
        if self._config["port"] != "None":
            ports.append(self._config["port"])

        if len(ports) == 0:
            raise ValueError("ERROR: User did not specify a port in the arguments or the config file.")

        for i in range(len(ports)):
            try:
                port_int = int(ports[i])
                if port_int >= 1024 and port_int <= 49151:
                    self._port = ports[i]
                    print("Port {0} is valid.".format(self._port))
                    return
                else:
                    raise ValueError("Port {0} is not within the range of 1024 to 49151.".format(ports[i]))
            except Exception as e:
                print("Error parsing port \"{}\".".format(ports[i]))
                if i + 1 == len(ports):
                    msg = "ERROR: Could not get usable port from user due to error: \"{}\"".format(e)
                    msg += ".\nThis program will now exit."
                    print(msg)
                    exit(1)

    def bind(self):
        cmd = "{0} forward tcp:{1} tcp:{1}".format(repr(str(self._adb)), self._port)
        connect = self._run_sp(cmd)
        if connect[2] == 0:
            print("Port {0} should be forwarded correctly over ADB.".format(self._port))
        else:
            msg = "ERROR: Could not forward TCP port {0} through ADB.\n".format(self._port)
            if connect[0].decode().strip() != "":
                msg += "Stdout: {}\n".format(connect[0].decode().strip())
            if connect[1].decode().strip() != "":
                msg += "Stderr: {}\n".format(connect[1].decode().strip().splitlines()[0])
            msg += "Return Code: {}".format(connect[2])
            raise OSError(msg)


if __name__ == '__main__':
    my_adb = ADB()
    my_adb.bind()
