SETUP
1. Install requirements via "pip install -r requirements.txt"

USAGE
1. Import "sys-info.py"
2. Create a SysInfo() object (no parameters)
3. This SysInfo object contains information about your computer's ...
	- OS
	- Boot Time
	- CPU
	- Virtual Memory
	- Disks
	- Network
	- Battery
NOTE that these do not automatically update. You have to use the ".reload()" function to reload the stats. 
NOTE that initializing the SysInfo class and using the ".reload()" function may take 1 to 2 seconds depending on your computer speed. 