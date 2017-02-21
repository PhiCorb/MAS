import subprocess
from time import sleep

vm_path = "\"/home/phil/vmware/XP VM 1/XP VM 1.vmx\""
subprocess.Popen(["vmrun", "start", vm_path])

# Wait for analysis to finish
sleep(25)
snapshot_name = "snapshot"
subprocess.Popen(["vmrun", "revertToSnapshot", vm_path, snapshot_name])
