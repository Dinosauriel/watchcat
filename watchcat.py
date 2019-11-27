#!/usr/bin/env python

import sys
import subprocess
import re
import os.path
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


root = os.path.dirname(__file__)

servers_yaml_path = os.path.join(root, "servers.yaml")
servers_yaml = open(servers_yaml_path)
servers = yaml.load(servers_yaml, Loader=Loader)
servers_yaml.close()

screens_active = subprocess.run(["screen", "-ls"], stdout=subprocess.PIPE).stdout.decode("utf-8")

def print_help():
    print("please provide a valid task to run:")
    print("  poll                 - poll all servers and take apropriate action, run at e.g. 1 min intervall using cronjob")
    print("  edit                 - edit the servers.yaml file")
    print("  start [servername]   - enable a server in the servers.yaml file and start it")
    print("  stop [servername]    - disable a server in the servers.yaml file and stop it")
    print("  restart [servername] - restart a running server")

if len(sys.argv) == 1:
    print_help()
    exit()

task = sys.argv[1]

def poll():
    i = -1
    for server in servers:
        i += 1
        #print(server)

        if not server["enabled"]:
            continue;

        server_name = server["name"]

        if server_name is None:
            print("please provide a name for server number " + str(i))
            continue


        if re.search(server_name, screens_active) is not None:
            #this server is running
            print("server " + server_name + " is already running")
            continue


        server_start_file = server["start"]
        if server_start_file is None:
            print("please provide a start file for the server " + server_name)
            continue


        print("server " + server_name + " is not running. running file: " + server_start_file)
        subprocess.run(["sh", server_start_file], stdout=subprocess.DEVNULL)

def edit():
    subprocess.run(["vim", servers_yaml_path])


if task == "poll":
    poll()
    exit()
elif task == "edit":
    edit()
    exit()
elif task == "start":
    exit()
elif task == "stop":
    exit()
elif task == "restart":
    exit()
else:
    print_help()
    exit()

