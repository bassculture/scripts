'''
'
' metadata.py 
'
' input: metadata.txt
' output: series of header MEI files (MEI files containing the meiHead)
'
'''

import pymei
import sys
import os
import argparse
import re
import logging
from meimeta.metadatadocument import *
from utilities import *

from utilities import set_logging, get_descendants

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compiles the metadata information from a tab-delimited text file to MEI headers. \
        The ouput is a series of MEI files.')
    parser.add_argument('metafile', help="file containing the metadata information for all headers")
    parser.add_argument('outdir', help="the output directory where the header files will be created")

    set_logging(parser)
    args = parser.parse_args()

    filename = args.metafile
    doc = MetadataDocument(filename = filename, exportPath = args.outdir)
    status = doc.exportHeaders()
