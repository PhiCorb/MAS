import subprocess
import colorama

colorama.init()


def spawn_vm(vm_path):
    # vm_path = "\"/home/phil/vmware/XP VM 1/XP VM 1.vmx\""
    subprocess.Popen(["vmrun", "start", vm_path])


def end_vm(vm_path):
    subprocess.Popen(["vmrun", "stop", vm_path, "hard"])


def restore_vm(vm_path, snapshot_name):
    # snapshot_name = "snapshot"
    subprocess.Popen(["vmrun", "revertToSnapshot", vm_path, snapshot_name])

if __name__ == "__main__":
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: this is not intended to be executed directly!" +
          colorama.Style.RESET_ALL)
    exit(1)
