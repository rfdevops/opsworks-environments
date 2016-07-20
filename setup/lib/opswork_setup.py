# -*- coding: utf-8 -*-

import boto
import uuid
import json

from boto import ec2, vpc, opsworks
from boto.exception import EC2ResponseError

from utils.utils import Logger
from etc import settings
from exceptions import (
    ExpectedAWSKeys,
    ExpectedAWSRoles,
    ExpectedSubnetsAndVPC,
    ParameterProblems
)

class OpsWorkSetup(object):

    def __init__(self, access_key=None, secret_key=None):
        self.logging = Logger(
            self.__class__.__name__
        ).get_logger()
        self.logging.debug(
            "Initiate class for opswork environments: %s" % (self.__class__.__name__)
        )
        if not settings.access_key or not settings.secret_key:
            self.access_key = access_key
            self.secret_key = secret_key
        else:
            self.access_key = settings.access_key
            self.secret_key = settings.secret_key

        if self.access_key is None or self.secret_key is None:
            raise ExpectedAWSKeys(
                "Please, provide a secret key and acces key aws, see: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html"
            )

    @property
    def conn(self):
        _conn = opsworks.connect_to_region(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='us-east-1'
        )
        self.logging.debug(
            "The connection with opsworks was been succesfully"
        )
        return _conn

    @property
    def security_groups(self):
        _security_groups = ec2.connect_to_region(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=settings.region
        )
        self.logging.debug(
            "The connection with ec2 was been succesfully"
        )
        return _security_groups
    
    @property
    def describe_subnets(self):
        _describe_subnets = vpc.connect_to_region(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=settings.region
        )
        self.logging.debug(
            "The connection with vpc was been succesfully"
        )
        return _describe_subnets
    

    def create_stack(self):
        """ create stack for modeling environment """
        stack_name = 'ElasticSearchStack-{}'.format(str(uuid.uuid4())[:8])
        if (not settings.default_instance_profile_arn or settings.default_instance_profile_arn is None
            or not settings.service_role_arn or settings.service_role_arn is None):
            raise ExpectedAWSRoles("Please, provide the correct services roles, see http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html and check README.md about the access required for this roles.")

        self.stack = self.conn.create_stack(
            name=stack_name,
            region=settings.region,
            default_availability_zone=settings.available_zone,
            custom_json="{}".format(settings.custom_json_cheff),
            use_custom_cookbooks=True,
            hostname_theme='Europe_Cities',
            use_opsworks_security_groups=True,
            custom_cookbooks_source={"Type": "git", "Url": settings.repository_url},
            default_instance_profile_arn=settings.default_instance_profile_arn,
            service_role_arn=settings.service_role_arn,
            default_ssh_key_name=settings.ssh_key_name_default,
            default_os=settings.default_os,
            configuration_manager=settings.configuration_manager
        )
        self.logging.debug(
            "The stack: {!r} has been created with successfull".format(
                stack_name
            )
        )
        return self.stack

    def create_security_group(self, network_policies=[]):
        """ get security groups and modeling template for security groups:
        :network_policies (list)
            e.g: [{
                'protocol': 'http',
                'from_port': '80',
                'to_port': '80',
                'cidr_ip': '172.0.0.1/16'
            }, {
                'protocol': 'tcp',
                'from_port': '9201',
                'to_port': '9201',
                'cidr_ip': '172.16.0.1/16'
            }]

        ** Observation **
            Don't accepet rules with 0.0.0.0/0"""
        security_groups = self.security_groups.get_all_security_groups()
        for sg_attributes in security_groups:
            if u"AWS-OpsWorks-Default-Server" == sg_attributes.name:
                for new_rule in network_policies:
                    print new_rule
                    try:
                        sg_attributes.authorize(
                            new_rule['protocol'],
                            new_rule['from_port'],
                            new_rule['to_port'],
                            new_rule['cidr_ip']
                        )
                        self.logging.info(
                            "The new rule: {!r}, {!r}, {!r}, {!r} has been created on security group: {!r}".format(
                                new_rule['protocol'],
                                new_rule['from_port'],
                                new_rule['to_port'],
                                new_rule['cidr_ip'],
                                sg_attributes.name
                            )
                        )
                    except EC2ResponseError:
                        self.logging.info(
                            "Specified Rule already exists...skipped"
                        )
                        pass

                # If put rule with "0.0.0.0/0" will be deleted.
                # I decided put this code here, just to force no to have world rule for anywhere
                for rule in sg_attributes.rules:
                    for grant in rule.grants: 
                        if u"0.0.0.0/0" == grant.cidr_ip:
                            sg_attributes.revoke(
                                rule.ip_protocol,
                                rule.from_port,
                                rule.to_port,
                                grant.cidr_ip
                            )
                            self.logging.info(
                                "The rule: {!r}, {!r}, {!r}, {!r} has been deleted on security group: {!r}.".format(
                                    rule.ip_protocol,
                                    rule.from_port,
                                    rule.to_port,
                                    grant.cidr_ip,
                                    sg_attributes.name
                                )
                            )

    def vpc_data_network(self, protocol='tcp', cidr_ips=[]):
        """ This method is just for get and management vpc informcations:
        :protocol (string):
        :cidr_ips (list): 
            e.g: [{
                'protocol': 'http',
                'from_port': '80',
                'to_port': '80',
                'cidr_ip': '172.0.0.1/16'
            }, {
                'protocol': 'tcp',
                'from_port': '9200',
                'to_port': '9200',
                'cidr_ip': '172.1.0.1/16'
            }]"""
        network_policies = []
        if not cidr_ips:
            # Get default subnets on defauilt VPC (my case)
            subnets = self.describe_subnets.get_all_subnets()
            for subnet in subnets:
                cidr_ips.append(subnet.cidr_block)
            network_policies = [{
                'protocol': 'tcp',
                'from_port': 9300,
                'to_port': 9300,
                'cidr_ip': [cidr_ips[0], cidr_ips[1]]
            }, {
                'protocol': 'tcp',
                'from_port': 9201,
                'to_port': 9201,
                'cidr_ip': [cidr_ips[0], cidr_ips[1]]
            }, {
                'protocol': 'tcp',
                'from_port': 80,
                'to_port': 80,
                'cidr_ip': [cidr_ips[0], cidr_ips[1]]
            }]
        else:
            for cidr_ip in cidr_ips:
                network_policies.append({
                    'protocol': cidr_ip['protocol'],
                    'from_port': cidr_ip['from_port'],
                    'to_port': cidr_ip['to_port'],
                    'cidr_ip': cidr_ip['cidr_ip']
                })
        if not network_policies:
            raise ExpectedSubnetsAndVPC("Well, in this case, it's necessary to create one VPC and two subnets for this region")
        self.logging.debug("will be created network policies and adjusted with parameters: {}".format(
            network_policies
            )
        )
        self.create_security_group(network_policies=network_policies)

    def create_layer(self, new_stack=False, stack_id=None):
        """ The method is just for create layer:
        :new_stack (booblean): 
        :stack_id (string):"""
        layer_name = 'ElasticSearchLayer-{}'.format(str(uuid.uuid4())[:8])
        if new_stack and stack_id is None:
            new_stack_id = self.create_stack()['StackId']
        if stack_id:
            new_stack_id = stack_id

        self.stack['StackId'] = new_stack_id

        self.layer_created = self.conn.create_layer(
            stack_id=self.stack['StackId'],
            type='custom',
            name=layer_name,
            volume_configurations=settings.ebs_volum,
            shortname='elasticsearchlayer',
            custom_instance_profile_arn=settings.default_instance_profile_arn,
            auto_assign_elastic_ips=True,
            custom_recipes=settings.recipes
        )
        self.logging.debug(
            "The layer: {!r} has been created with successfull".format(
                layer_name
            )
        )
        self.vpc_data_network()
        return self.layer_created

    def create_instances(self, number_instances=3, subnets_list=[], new_layer=True, new_stack=True, layer_id=[], cidr_ips=[], **kwargs):
        """The method is just for create instances:
        :number_instances (int): Number of the instances you want create
        :subnets_list (list): list with the subnets for input your instances, example:
            [ 172.0.0.1/16, 172.1.0.1/16 ]
        :new_layer (boolean): If you want create a new layer before or input in specific layer, expected LayerId
        :new_stack (boolean): if you want create a new stack before or input in specific stack, expected StackId
        :layer_id (list): If new_layer is False, i need a list with layer ids, example: [ 'foor', 'bar' ]
        :cidr_ips (list): Set the ips list with arbitrary cidr_ips
        :**kwargs (dict): dict with another increments for boto.opsworks method
        """
        if new_layer and not layer_id:
            new_layer_id = [self.create_layer(new_stack=new_stack)['LayerId']]
        if layer_id:
            new_layer_id = layer_id

        if subnets_list:
            if len(subnets_list) != number_instances:
                raise ParameterProblems("number instances and subnets_list needed the same lenght.")
        else:
            subnets_list=None

        for loop in range(0, number_instances):
            if subnets_list:
                new_subnets_list = subnets_list[loop]
            else:
                new_subnets_list = None

            instance_created = self.conn.create_instance(
                stack_id=self.stack['StackId'],
                layer_ids=new_layer_id,
                root_device_type='ebs',
                instance_type=settings.instance_type,
                subnet_id=new_subnets_list,
                **kwargs
            )
            self.logging.debug(
                "The {!r} instance(s) has been created with successfull: stack_id: {!r}, layer_id: {!r}, instance_type: {!r}, subnets: {!r}".format(
                    number_instances,
                    self.stack['StackId'],
                    new_layer_id,
                    settings.instance_type,
                    new_subnets_list
                )
            )
            self.conn.start_instance(instance_created['InstanceId'])

        if cidr_ips:
            rules=[]
            for cidr_ip in cidr_ips:
                rules.append({
                    'protocol': 'tcp',
                    'from_port': 80,
                    'to_port': 80,
                    'cidr_ip': cidr_ip
                })
                rules.append({
                    'protocol': 'tcp',
                    'from_port': 9201,
                    'to_port': 9201,
                    'cidr_ip': cidr_ip
                })
                rules.append({
                    'protocol': 'tcp',
                    'from_port': 9300,
                    'to_port': 9300,
                    'cidr_ip': cidr_ip
                })
            self.vpc_data_network(cidr_ips=rules)

    def managament_instance(self, instance_id, action='stop'):
        """ This class, is just for management instances (stop, start etc...)
        :instance_id (string):
        :action (string) - specific strings expected, are options:
            'stop', 'start', 'delete'
        """
        status = None
        if action == 'stop':
            status = self.conn.stop_instance(instance_id)
        if action == 'start':
            status = self.conn.start_instance(instance_id)
        if action == 'delete':
            status = self.conn.delete_instance(instance_id=instance_id, delete_elastic_ip=True, delete_volumns=True)

        if not status:
            raise UnrecognizedComand("Plase, try again with: 'stop', 'start', or 'delete' command.")
        return status