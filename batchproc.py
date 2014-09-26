
'''
'
' batchproc.py
' 
' Go throuhg the files in a given folder and perform a task on each of them.
'
'''

import pymei
import sys
import os
import argparse
import re
import logging

from utilities import set_logging, get_descendants


def batchproc(args, proc):
    parser = argparse.ArgumentParser(description='Initialise MEI pages from a set of images undera folder')
    parser.add_argument('dir')
    parser.add_argument('--out', dest='out')
    parser.add_argument('--filter', dest='filter')
    parser.add_argument('-R', dest='recursive', action='store_true')
    parser.add_argument('--ignore', dest='filter_ignore')

    set_logging(parser)
    args = parser.parse_args()

    if args.filter:
        prog = re.compile(args.filter)

    if args.filter_ignore:
        prog_ignore = re.compile(args.filter_ignore)

    if args.recursive:
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                    proc(args, os.path.join(args.dir, file))
    else:
        for file in os.listdir(args.dir):
            if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                proc(args, os.path.join(args.dir, file))

    if args.out:
        pymei.XmlExport.meiDocumentToFile(doc, args.out)
    else:
        meitxt = pymei.XmlExport.meiDocumentToText(doc)
        print meitxt



mei-batch.py