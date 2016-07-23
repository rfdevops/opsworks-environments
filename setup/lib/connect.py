# -*- coding: utf-8 -*-

from boto import ec2, opsworks, vpc

from utils.utils import Logger
from etc import settings
from exceptions import ExpectedAWSKeys


class KeysAWS(object):
    _ec2_connection = None
    _opsworks_conection = None
    _iam_connection = None
    _vpc_connection = None

    def __init__(self, access_key=None, secret_key=None):
        self.logging = Logger(
            self.__class__.__name__
        ).get_logger()
        self.logging.debug(
            "Initiate class for opswork environments: %s" % (self.__class__.__name__)
        )
        if settings.ACCESS_KEY is None or settings.SECRET_KEY is None:
            self.access_key = access_key
            self.secret_key = secret_key
        else:
            self.access_key = settings.ACCESS_KEY
            self.secret_key = settings.SECRET_KEY

        if self.access_key is None or self.secret_key is None:
            raise ExpectedAWSKeys(
                "Please, provide a secret key and acces key aws, see: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html"
            )

    def __name__(self):
        return "{}-{}".format(self.access_key, self.secret_key)

    @property
    def _vpc_connection(self):
        _vpc_connection = vpc.connect_to_region(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=settings.REGION
        )
        self.logging.debug(
            "The connection with vpc was been succesfully"
        )
        return _vpc_connection


    @property
    def _ec2_connection(self):
        _ec2_connection = ec2.connect_to_region(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=settings.REGION
        )
        self.logging.debug(
            "The connection with ec2 was been succesfully"
        )
        return _ec2_connection

    @property
    def _opsworks_conection(self):
        _opsworks_conection = opsworks.connect_to_region(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='us-east-1'
        )
        self.logging.debug(
            "The connection with opsworks was been succesfully"
        )
        return _opsworks_conection

    def __del__(self):
        self._ec2_connection.close()
        self._opsworks_conection.close()
        self._iam_connection.close()
        self._vpc_connection.close()
