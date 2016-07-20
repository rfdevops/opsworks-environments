# opsworks-environments
Simple task for run opsworks environment with elasticsearch and kopf plugin. (BUILDING)

* first of all, you need to create a user, in AWS with AdministratorAccess, for build a environment,
this rule its necessary for create all stacks, layers, security groups, so you need a power access in your environment.

For create a IAM role, go to console, choose your region, then go to Services > IAM.

click on Users, then click on Create New Users.

On first one, put your user name, in this case, i put 'elasticsearch', so check if "Generate an access key for each user" is flagged, if so, click on create.
in the next page, click on 'Show user security credentials', and get your `access_key` and your `secret_key`, and put on
`"access_key": ""` and `"secret_key": ""` in `./etc/settings.py`.
After it, click on close twice.


in the next one, click about your user that was created, so go to `Permissions`, and click on `Attach policy` and choice `AdministratorAccess`.

After did it, go to the `Roles` and create a new role called `aws-opsworks-ec2-role`, in the next one, choice `Aws Services Roles` and `Amazon EC2`, then not select anything, and save role.

Repeat it with the role with `aws-opsworks-service-role`.

After did it, you need to go on details of the `aws-opsworks-ec2-role`, go to `Inline Policies`, and select `Custom Policy`, the name, put `OpsWorksElasticsearchEC2Discovery`, and put below the json.

```
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
```
Save this rule, so, go to IAM dashboard in `Roles`, get describle to `aws-opsworks-ec2-role`, and copy `Instance Profile ARN(s)` and past in `./etc/settings.py` on variable `default_instance_profile_arn`, go back and select `aws-opsworks-service-role` copy `Role ARN ` and paste in `./etc/settings.py` on variable `service_role_arn`.


So, right now, install the requirements of the project:

```
pip install -r requirements.txt
```

Lunch the cluster of the elasticsearchs with one master and how many cluster would you like. It`s simple, run:
```
python start.py setup-environment --cidr-ips ipv4/mask ipv4/mask --number-instances 3
```


I bit more about the script:

Help for usage the script:
```
usage: start.py [-h]
                {delete-instances,stop-instance,start-instance,create-instances,create-layer,create-stack,setup-environment}
                ...

positional arguments:
  {delete-instances,stop-instance,start-instance,create-instances,create-layer,create-stack,setup-environment}
                        commands
    delete-instances    Delete specific instances
    stop-instance       Stop specific instances
    start-instance      Start specific instances
    create-instances    Create instances
    create-layer        Create a new Layer
    create-stack        Create a new Stack
    setup-environment   Create instances, stack, layer and security groups by
                        default

optional arguments:
  -h, --help            show this help message and exit
```

* Setup environment [setup-environment]:

```
usage: start.py setup-environment [-h] -li CIDR_IPS [CIDR_IPS ...] -ni
                                  NUMBER_INSTANCES

optional arguments:
  -h, --help            show this help message and exit
  -li CIDR_IPS [CIDR_IPS ...], --cidr-ips CIDR_IPS [CIDR_IPS ...]
                        Ips list for create a security rule, expected a list
                        with cidr_ips, example: -li 172.0.0.2/32 172.0.0.3/32
  -ni NUMBER_INSTANCES, --number_instances NUMBER_INSTANCES
                        Ips list for create a security rule, expected a list
                        with cidr_ips, example: -li 172.0.0.2/32 172.0.0.3/32
```

* Delete Instances [delete-instances]:
```
usage: start.py delete-instances [-h] -ii INSTANCE_ID

optional arguments:
  -h, --help            show this help message and exit
  -ii INSTANCE_ID, --instance-id INSTANCE_ID
                        Instance Id that will be deleted
```

* Stop Instances [stop-instance]
```
usage: start.py stop-instance [-h] -ii INSTANCE_ID

optional arguments:
  -h, --help            show this help message and exit
  -ii INSTANCE_ID, --instance-id INSTANCE_ID
                        Instance Id that will be stopped
```

* Start Instances [start-instance]
```
usage: start.py start-instance [-h] -ii INSTANCE_ID

optional arguments:
  -h, --help            show this help message and exit
  -ii INSTANCE_ID, --instance-id INSTANCE_ID
                        Instance Id that will be started
```

* Create instances [create-instances ]

```
usage: start.py create-instances [-h] [-ni NUMBER_INSTANCES] [-ns] [-nl]
                                 [-si STACK_ID] [-ly LAYER_ID [LAYER_ID ...]]

optional arguments:
  -h, --help            show this help message and exit
  -ni NUMBER_INSTANCES, --number-instances NUMBER_INSTANCES
                        Number of instances that will be created, by default
                        will be create 3
  -ns, --new-stack      Create a new stack before create layer, if not, will
                        be necessary put --stack-id argument.
  -nl, --new-layer      Create a new layer before create instance, if not,
                        will be necessary put --layer-id argument.
  -si STACK_ID, --stack-id STACK_ID
                        :str Stack id in string type
  -ly LAYER_ID [LAYER_ID ...], --layer-id LAYER_ID [LAYER_ID ...]
                        :str Stack id in string type
```

* Create layer [create-layer]
```
usage: start.py create-layer [-h] (-ns | -si STACK_ID)

optional arguments:
  -h, --help            show this help message and exit
  -ns, --new-stack      Create a new stack before create layer, if not, will
                        be necessary put --stack-id argument.
  -si STACK_ID, --stack-id STACK_ID
                        :str Stack id in string type
```

* Create Stack [create-stack]
```
usage: start.py create-stack [-h]

optional arguments:
  -h, --help  show this help message and exit
```

