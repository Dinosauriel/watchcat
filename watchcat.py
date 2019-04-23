
import subprocess
import re
import os.path


root = os.path.dirname(__file__)

servers = open(os.path.join(root, "servers.txt"))

screens_active = subprocess.run(["screen", "-ls"], stdout=subprocess.PIPE).stdout.decode("utf-8")

for server in servers:
	server_name = server.strip()

	if server_name[0:2] == "//" or server_name[0] == "#" or server_name == "":
		#this is a commment
		continue
	
	if re.search(server_name, screens_active) is not None:
		#this server is running
		continue

	print("server " + server_name + " is not running. starting...")
	subprocess.run(["sh", os.path.join(root, "../start-" + server_name + ".sh")], stdout=subprocess.DEVNULL)

servers.close()