# -*- coding: utf-8 -*-

import sys
import os
import argparse
import types
import re

from etc import settings

from utils.utils import Logger, APP_ROOT
from lib.exceptions import UnknowCIDRRange
from lib.opswork_setup import OpsWorkSetup
from lib.iam import AWSPolicies

__author__ = "Rondineli G. de Araujo"
__copyright__ = "Copyright (C) 2015 Rondineli G. Araujo"

__version__ = "0.0.1"


logging = Logger("OpsWorks Setup").get_logger()
logging.debug("Lunch opsworks setup with elasticSearch Cluster")


def call(args, parse):
    if args.access_key:
        settings.ACCESS_KEY = args.access_key

    if args.secret_key:
        settings.SECRET_KEY = args.secret_key

    if args.service_role_arn:
        settings.SERVICE_ROLE_ARN = args.service_role_arn

    if args.instance_arn_role:
        settings.DEFAULT_INSTANCE_PROFILE_ARN = args.instance_arn_role

    opsworks = OpsWorkSetup()
    iam = AWSPolicies()


    if args.which == "create_policies":
        result_instance_profile = iam.create_instance_profile()
        result_service_profile = iam.create_service_profile()
        if result_service_profile or result_instance_profile:
            try:
                settings.DEFAULT_INSTANCE_PROFILE_ARN = result_instance_profile['response_policy']['create_role_response']['create_role_result']['role']['arn']
                settings.SERVICE_ROLE_ARN = result_service_profile['response_policy']['create_role_response']['create_role_result']['role']['arn']
            except KeyError:
                self.logging.error("Problems for create policies on AWS, check your credentials or try create manually")

    if args.which == 'setup_environment':
        pattern_ipv4 = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$")
        for arg in args.cidr_ips:
            if not pattern_ipv4.match(arg):
                raise UnknowCIDRRange("Please, provide a valid list with correct ipv4 cidr >>'{}'".format(
                        arg
                    )
                )

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
    parser.add_argument(
        "-ak",
        "--access-key",
        default=os.environ.get("ACCESS_KEY", None),
        help="Access key | export ACCESS_KEY=''"
    )
    parser.add_argument(
        "-sk",
        "--secret-key",
        default=os.environ.get("SECRET_KEY", None),
        help="Secret key | export SECRET_KEY='' "
    )
    parser.add_argument(
        "-sr",
        "--service-role-arn",
        default=os.environ.get("SERVICE_ROLE_ARN", None),
        help="Service ARN Role | export SERVICE_ROLE_ARN=''"
    )
    parser.add_argument(
        "-ir",
        "--instance-arn-role",
        default=os.environ.get("INSTANCE_ARN_PROFILE", None),
        help="Instance Profile ARN | export INSTANCE_ARN_PROFILE=''"
    )

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
    create_iams_parser = subparsers.add_parser('create-policies', help='Create instances')
    create_iams_parser.set_defaults(which='create_policies')

    args = parser.parse_args()
    call(args, parser)

