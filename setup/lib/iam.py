# -*- coding: utf-8 -*-
import uuid

from boto import iam

from etc import settings
from connect import KeysAWS


class AWSPolicies(KeysAWS):
	def __init__(self, access_key=None, secret_key=None):
		super(AWSPolicies, self).__init__(access_key, secret_key)
		self.logging.debug(
            "Initiate class for opswork environments: %s" % (self.__class__.__name__)
        )

	def create_instance_profile(self):
		instance_profile = self._iam_connection.create_instance_profile(
			'OpsWorksElasticsearchEC2Discovery{}'.format(str(uuid.uuid4())[:8])
		)
		role = self._iam_connection.create_role(
			'opsworks-ec2-instance_profile_role-{}'.format(str(uuid.uuid4())[:8])
		)
		self._iam_connection.add_role_to_instance_profile(
			instance_profile['create_instance_profile_response']['create_instance_profile_result']['instance_profile']['instance_profile_name'],
			role['create_role_response']['create_role_result']['role']['role_name']
		)
		response_policy = self._iam_connection.put_role_policy(
			instance_profile['create_instance_profile_response']['create_instance_profile_result']['instance_profile']['instance_profile_name'],
			role['create_role_response']['create_role_result']['role']['role_name'],
			settings.OPSWORKS_EC2_DISCOVERY_POLICY
		)
		return {
			'instance_profile': instance_profile,
			'role': role,
			'response_policy': response_policy
		}

	def create_service_profile(self):
		role = self._iam_connection.create_rule(
			'opsworks-ec2-service-role-{}'.format(str(uuid.uuid4())[:8])
		)
		response_policy = self._iam_connection.put_role_policy(
			role['create_role_response']['create_role_result']['role']['role_name'],
			'OWServicePolicy',
			settings.OPSWORKS_SERVICES_POLICY
		)
		return {
			'service_profile': instance_profile,
			'role': role,
			'response_policy': response_policy
		}
