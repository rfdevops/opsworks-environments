# -*- coding: utf-8 -*-

import sys
import os
import argparse
import types
import re

from utils.utils import Logger, APP_ROOT
from lib.exceptions import UnknowCIDRRange
from lib.opswork_setup import OpsWorkSetup

__author__ = "Rondineli G. de Araujo"
__copyright__ = "Copyright (C) 2015 Rondineli G. Araujo"

__version__ = "0.0.1"


logging = Logger(
    "OpsWorks Setup"
).get_logger()
logging.debug(
    "Lunch opsworks setup with elasticSearch Cluster"
)


def call(args, parse):
    opsworks = OpsWorkSetup()
    if args.which == 'setup_environment':
        pattern_ipv4 = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$")
        pattern_ipv6 = re.compile("^s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:)))(%.+)?s*(\/(d|dd|1[0-1]d|12[0-8]))$")
        for arg in args.cidr_ips:
            if not pattern_ipv4.match(arg) and not pattern_ipv6.match(arg):
                raise UnknowCIDRRange("Please, provide a valid list with correct ipv4/ipv6 cidr >>'{}'".format(
                        arg
                    )
                )
        print args.number_instances
        opsworks.create_instances(
            number_instances=args.number_instances,
            cidr_ips=args.cidr_ips,
            new_layer=True,
            new_stack=True,

        )

    if args.which == "create_instances":
        if not args.new_layer:
            logging.debug("Missing parameters ['--new-layer'], by default is False")

        if not args.new_stack:
            logging.debug("Missing parameters ['--new-stack'], by default is False")

        opsworks.create_instances(
            number_instances=args.number_instances,
            new_layer=args.new_layer,
            new_stack=args.new_stack,
            layer_id=args.layer_id,
            stack_id=args.stack_id,
        )

    if args.which == "create_layer":
        if not args.new_stack:
            logging.debug("Missing parameters ['--new-layer'], by default is False")

        opsworks.create_layer(
            new_stack=args.new_stack,
            stack_id=args.stack_id
        )

    if args.which == "create_stack":
        opsworks.create_stack()

    if args.which == "delete_instance":
        opsworks.managament_instance(instance_id=args.instance_id, action="delete")

    if args.which == "stop_instance":
        opsworks.managament_instance(instance_id=args.instance_id, action="stop")

    if args.which == "start_instance":
        opsworks.managament_instance(instance_id=args.instance_id, action="start")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='commands')

    # Management Instances
    delete_instance_parser = subparsers.add_parser('delete-instances', help="Delete specific instances")
    delete_instance_parser.set_defaults(which="delete_instance")

    stop_instance_parser = subparsers.add_parser('stop-instance', help="Stop specific instances")
    stop_instance_parser.set_defaults(which="stop_instance")

    start_instance_parser = subparsers.add_parser('start-instance', help="Start specific instances")
    start_instance_parser.set_defaults(which="start_instance")

    delete_instance_parser.add_argument(
        "-ii", 
        "--instance-id",
        type=str,
        required=True,
        help="Instance Id that will be deleted"
    )
    stop_instance_parser.add_argument(
        "-ii", 
        "--instance-id",
        type=str,
        required=True,
        help="Instance Id that will be stopped"
    )
    start_instance_parser.add_argument(
        "-ii", 
        "--instance-id",
        type=str,
        required=True,
        help="Instance Id that will be started"
    )


    # Create instances
    create_instances_parser = subparsers.add_parser('create-instances', help='Create instances')
    create_instances_parser.set_defaults(which='create_instances')
    group_create_instances_stack = create_instances_parser.add_mutually_exclusive_group(required=True)
    group_create_instances_layer = create_instances_parser.add_mutually_exclusive_group(required=True)

    create_instances_parser.add_argument(
        "-ni",
        "--number-instances",
        default=3,
        type=int,
        help='Number of instances that will be created, by default will be create 3'
    )

    group_create_instances_stack.add_argument(
        "-ns",
        "--new-stack",
        action="store_true",
        help="Create a new stack before create layer, if not, will be necessary put --stack-id argument."
    )
    group_create_instances_layer.add_argument(
        "-nl",
        "--new-layer",
        action="store_true",
        help="Create a new layer before create instance, if not, will be necessary put --layer-id argument."
    )
    group_create_instances_stack.add_argument(
        "-si",
        "--stack-id",
        type=str,
        help=":str Stack id in string type"
    )

    group_create_instances_layer.add_argument(
        "-ly",
        "--layer-id",
        type=str,
        nargs="+",
        help=":str Stack id in string type"
    )

    #Create layer
    create_layer_parser = subparsers.add_parser(
        "create-layer",
        help="Create a new Layer"
    )
    create_layer_parser.set_defaults(which='create_layer')

    group_create_layer_with_stack = create_layer_parser.add_mutually_exclusive_group(required=True)
    group_create_layer_with_stack.add_argument(
        "-ns",
        "--new-stack",
        action="store_true",
        help="Create a new stack before create layer, if not, will be necessary put --stack-id argument."
    )

    group_create_layer_with_stack.add_argument(
        "-si",
        "--stack-id",
        type=str,
        help=":str Stack id in string type"
    )

    #Create Stack
    create_stack_parser = subparsers.add_parser(
        'create-stack',
        help='Create a new Stack'
    )
    create_stack_parser.set_defaults(which='create_stack')


    setup_environment = subparsers.add_parser(
        'setup-environment',
        help='Create instances, stack, layer and security groups by default'
    )

    setup_environment.set_defaults(which='setup_environment')

    setup_environment.add_argument(
        "-li",
        "--cidr-ips",
        type=str,
        nargs="+",
        required=True,
        help="Ips list for create a security rule, expected a list with cidr_ips, example: -li 172.0.0.2/32 172.0.0.3/32"
    )
    setup_environment.add_argument(
        "-ni",
        "--number_instances",
        type=int,
        required=True,
        help="Ips list for create a security rule, expected a list with cidr_ips, example: -li 172.0.0.2/32 172.0.0.3/32"
    )

    args = parser.parse_args()
    call(args, parser)

