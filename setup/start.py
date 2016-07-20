# -*- coding: utf-8 -*-

import sys
import os
import argparse

from utils.utils import Logger, APP_ROOT
from lib.exceptions import * #temporary
from lib.opswork_setup import OpsWorkSetup

__author__ = "Rondineli G. de Araujo"
__copyright__ = "Copyright (C) 2015 Rondineli G. Araujo"

__version__ = "0.0.1"


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers(help='commands')

	# Management Instances
	delete_instance_parser = subparsers.add_parser('delete-instances', help="Delete specific instances")
	stop_instance_parser = subparsers.add_parser('stop-instance', help="Stop specific instances")
	start_instance_parser = subparsers.add_parser('start-instance', help="Start specific instances")

	delete_instance_parser.add_argument(
		"-ii", 
		"--instance-id",
		nargs="+",
		required=True,
		help="Instance Id that will be deleted"
	)
	stop_instance_parser.add_argument(
		"-ii", 
		"--instance-id",
		nargs="+",
		required=True,
		help="Instance Id that will be stopped"
	)
	start_instance_parser.add_argument(
		"-ii", 
		"--instance-id",
		nargs="+",
		required=True,
		help="Instance Id that will be started"
	)


	# Create instances
	create_instances_parser = subparsers.add_parser('create-instances', help='Create instances')
	create_instances_parser.add_argument(
		"-ni",
		"--number-instances",
		default=3,
		type=int,
		help='Number of instances that will be created, by default will be create 3'
	)

	create_instances_parser.add_argument(
		"-ns",
		"--new-stack",
		action="store_true",
		help="Create a new stack before create layer, if not, will be necessary put --stack-id argument."
	)
	create_instances_parser.add_argument(
		"-si",
		"--stack-id",
		type=str,
		help=":str Stack id in string type"
	)

	create_parser = subparsers.add_parser(
		'create-stack',
		help='Create a new Stack'
	)

	setup_environment = subparsers.add_parser(
		'setup-environment',
		help='Create instances, stack, layer and security groups by default'
	)

	setup_environment.add_argument(
		"-li",
		"--cidr-ips",
		type=str,
		nargs="+",
		required=True,
		help="Ips list for create a security rule, expected a list with cidr_ips, example: -li 172.0.0.2/32 172.0.0.3/32"
	)
	print parser.parse_args()
