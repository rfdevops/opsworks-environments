# -*- coding: utf-8 -*-

import sys
import os
import argparse

from utils.utils import Logger, APP_ROOT
from lib.excepetions import * #temporary
from lib.opswork_setup import OpsWorkSetup

__author__ = "Rondineli G. de Araujo"
__copyright__ = "Copyright (C) 2015 Rondineli G. Araujo"

__version__ = "0.0.1"





if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		"-cl",
		"--create-layer",
		action="store_true",
		help="Create a new instance in specific stack or with new stack")
	group.add_argument(
		"-cs",
		"--create-stack",
		action="store_true",
		help="Create a new stack in your environment"
	)
	group.add_argument(
		"-ci",
		"--create-instance",
		action="store_true",
		help="Create a new instance with new layer/stack or existant new stack/layer"
	)
	group.add_argument(
		"-di",
		"--delete-instance",
		action="store_true",
		help="Delete specific instance"
	)
	group.add_argument(
		"-spi",
		"--stop-instance",
		action="store_true",
		help="Stop specific instance"
	)