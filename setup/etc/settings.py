# -*- coding: utf-8 -*-
import json

ACCESS_KEY = ""
SECRET_KEY = ""

OPSWORKS_EC2_DISCOVERY_POLICY = """
	{
	    "Version": "2012-10-17",
	    "Statement": [
	        {
	            "Effect": "Allow",
	            "Action": [
	                "ec2:DescribeInstances",
	                "ec2:DescribeRegions",
	                "ec2:DescribeTags",
	                "ec2:DescribeSecurityGroups",
	                "cloudwatch:PutMetricData"
	            ],
	            "Resource": "*"
	        }
	    ]
	}
"""

OPSWORKS_SERVICES_POLICY = """
	{
	    "Statement": [
	        {
	            "Action": [
	                "ec2:*",
	                "iam:PassRole",
	                "cloudwatch:GetMetricStatistics",
	                "cloudwatch:DescribeAlarms",
	                "elasticloadbalancing:*",
	                "rds:*"
	            ],
	            "Effect": "Allow",
	            "Resource": [
	                "*"
	            ]
	        }
	    ]
	}
"""


CUSTOM_JSON_CHEF = {
	"java": {
		"jdk_version": "7",
		"oracle": {
			"accept_oracle_download_terms": "true"
		},
		"accept_license_agreement": "true",
		"install_flavor": "oracle"
	},
	"opsworks": {
		"data_bags": {
			"plugins": {
				"cloud-aws": {
					"access_key": ACCESS_KEY,
					"secret_key": SECRET_KEY,
				},
				"nginx": {
					"username": "elasticsearch",
					"password": "elasticsearch"
				}
			}
		}
	},
	"elasticsearch": {
		"gateway": {
			"expected_nodes": 3
		},
		"discovery": {
			"type": "ec2",
			"zen": {
				"minimum_master_nodes": 1,
				"ping": {
					"multicast": {
						"enabled": "true"
					}
				}
			},
			"ec2": {
				"tag": {
					"opsworks:stack": "Elasticsearch "
				}
			}
		},
		"custom_config": {
			"cluster.routing.allocation.awareness.attributes": "rack_id"
		}
	}
}

CUSTOM_JSON_CHEF = json.dumps(CUSTOM_JSON_CHEF)

RECIPES = {
	"Setup": [
		'yum',
		'ark',
		'java',
		'elasticsearch::default',
		'layer-custom::esplugins',
		'nginx'
	],
	"Configure": [],
	"Deploy": [],
	"Undeploy": [],
	"Shutdown": []
}


CONFIGURATION_MANAGER = {
	"Name": "Chef",
	"Version": "12"
}

DEFAULT_OS = "Amazon Linux 2016.03"

SERVICE_ROLE_ARN = ""
DEFAULT_INSTANCE_PROFILE_ARN = ""
 
VPC_ID = None

SSH_KEY_NAME_DEFAULT = ''

LAYER_NAME = u'ElasticSearchCluster'
LAYER_SHORT_NAME = u'clusteropswork'

REGION = 'us-west-1'
AVAILABLE_ZONE = 'us-west-1a'

INSTANCE_TYPE = 't2.micro'


EBS_VOLUM = [{
	'MountPoint': '/mnt/elasticsearch-data',
	'Size': 20,
	'VolumnType': 'magnetic',
	'NumberOfDisks': 1
}]

SECURITY_GROUP = {
	u'name': u'AWS-OpsWorks-Default-Server'
}

REPOSITORY_URL = 'https://github.com/Rondineli/cookbooks'

LOGGER_LEVEL = "debug"

try:
    from .local_settings import *
except ImportError:
    pass
