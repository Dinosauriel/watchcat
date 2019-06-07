#!/usr/bin/env python

import subprocess
import re
import os.path
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper




root = os.path.dirname(__file__)

servers_yaml = open(os.path.join(root, "servers.yaml"))
servers = yaml.load(servers_yaml, Loader=Loader)
servers_yaml.close()


screens_active = subprocess.run(["screen", "-ls"], stdout=subprocess.PIPE).stdout.decode("utf-8")
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
		#print("server " + server_name + " is already running")
		continue


	server_file = server["file"]
	if server_file is None:
		print("please provide a start file for the server " + server_name)
		continue


	print("server " + server_name + " is not running. running file: " + server_file)
	subprocess.run(["sh", server_file], stdout=subprocess.DEVNULL)
