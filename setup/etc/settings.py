# -*- coding: utf-8 -*-

custom_json_cheff = """{
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
					"access_key": "",
					"secret_key": ""
				}
			}
		}
	},
	"elasticsearch": {
		"nginx": {
			"users": [{
				"username": "elasticsearch",
				"password": "elasticsearch"
			}],
			"allow_cluster_api": "true",
			"port": 80
		},
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
}"""

recipes = {
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


configuration_manager = {
	"Name": "Chef",
	"Version": "12"
}

default_os = "Amazon Linux 2016.03"

service_role_arn = ""
default_instance_profile_arn = ""
 
vpc_id = None

ssh_key_name_default = 'starfood'

layer_name = u'ElasticSearchCluster'
layer_short_name = u'clusteropswork'

region = 'us-west-1'
available_zone = 'us-west-1a'

instance_type = 't2.micro'

access_key = ""
secret_key = ""

ebs_volum = [{
	'MountPoint': '/mnt/elasticsearch-data',
	'Size': 20,
	'VolumnType': 'magnetic',
	'NumberOfDisks': 1
}]

security_group = {
	u'name': u'AWS-OpsWorks-Default-Server'
}

repository_url = 'https://github.com/Rondineli/cookbooks'

logger_level = "debug"

try:
    from .local_settings import *
except ImportError:
    pass
