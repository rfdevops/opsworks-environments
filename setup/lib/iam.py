# -*- coding: utf-8 -*-
from boto import iam

from connect import KeysAWS


class IAM(KeysAWS):
	def __init__(self):
		super(AWSPolicies, self).__init__()
		self.logging.debug("Init IAM class")