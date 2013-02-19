import argparse
import sys
import os
import string
from time import sleep
from ConfigParser import ConfigParser
from multiprocessing import Pool

from lib.VMachine import VMachine
from lib.VMManager import VMManagerVS

def do_update(vm):
	return "updating %s" % vm

def do_dispatch(vm):
	return "dispatching tests for %s" % vm

def update(vm):
	try:
		vm = VMachine(vm_conf_file, vm_name)
		vmman.revertSnapshot(vm, vm.snapshot)
		sleep(10)
		vmman.startup(vm)
		# executing scripts for vm and wait 3 hours
		vmman.executeCmd(vm, cmd)
		sleep(3600*3)
		vmman.reboot(vm)
		vmman.refreshSnapshot(vm)

		return "%s updated"  % vm
	except:
		return "ERROR: %s is not updated"

def main():

	vm_conf_file = os.path.join("conf", "vms.cfg")
	op_conf_file = os.path.join("conf", "operations.cfg")

	# get configuration for AV update process (exe, vms, etc)

	vmman = VMManagerVS(vm_conf_file)

	# get vm names
	c = ConfigParser()
	c.read(op_conf_file)
	vm_names = c.get("test", "machines").split(",")

	pool = Pool()
	r = pool.map_async(do_update, ((vm) for vm in vm_names)) 
	print r.get()

#if __name__ == "__main___":
main()