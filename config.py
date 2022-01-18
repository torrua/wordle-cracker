# -*- coding: utf-8 -*-

import logging

# set logging variables
logging.basicConfig(
    format='%(filename)s [LINE:%(lineno)d]\t[%(asctime)s] %(levelname)-s\t%(funcName)s() \t\t%(message)s',
    level=logging.DEBUG,
    datefmt="%y-%m-%d %H:%M:%S")
log = logging.getLogger(__name__)
