# encoding: utf8

"""
Created on 2016.01.13

@author: ZoeAllen
"""
import time
from startpro.common.utils.log4py import log
from startpro.core.utils.loader import safe_init_run

print('import mod.hi.py')


@safe_init_run
def run_hi(**kwargs):
    # import sys
    # for r in sys.path:
    #     print(r)
    log.info('hi')
    for i in range(5):
        log.error(i)
    while 1:
        print('hi')
        time.sleep(1)
