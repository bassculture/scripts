'''
'
' pages.py
' 
' Create an MEI file that contains all the facsimile images of a book
'
' Go throuhg the image files in a given folder. Each image file
' represents a page in a book. Perform per-page tasks, such as create a
' surface elements for the page, etc. 
'
'''

import pymei
import sys
import os
import argparse
import re
import logging


from utilities import set_logging, get_descendants

def process_img(args, img):
    try:
        logging.info("Processing file: " + img)
        surface = pymei.MeiElement('surface')
        # extract image index from the filename, then set n:
        # surface.setAttribute('n', n)
        index_tokens = re.search(args.index_pattern, img)
        if index_tokens != None:
            index_str = index_tokens.group(1)
            index = int(index_str)
            surface.addAttribute('n', str(index))
            surface.addAttribute('label', args.label_base + str(index - args.index_shift) )
            graphic = pymei.MeiElement('graphic')
            graphic.addAttribute('target', os.path.basename(img))
            surface.addChild(graphic)
        else:
            logging.warning('no index can be derived from the file name')
        # set label according to image index and index_shift
        return surface
    except Exception as ex:
        logging.critical(ex)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialise MEI pages from a set of images.')
    parser.add_argument('dir', help="The path to the folder where the image files are located")

    parser.add_argument('--out', dest='out', help="The path to the output file;\
        if not supplied the output will be written to the standard output")
    parser.add_argument('--filter', dest='filter', help="A regular expression filter;\
        only the matching files will be included")
    parser.add_argument('--ignore', dest='filter_ignore', help="A regular expression filter;\
        the matching files will be exluded")
    parser.add_argument('-R', dest='recursive', action='store_true', 
        help="Indicates that the iteration over the directory\
         will be recusrsive")
    parser.add_argument('--label-base', dest='label_base', help="Prefix of the page label;\
        defaults to 'page_'")
    parser.add_argument('--index-pattern', dest='index_pattern', help="A regular expression defining\
        the patter of the page numbers; The group of digits (the index number with leading zeros)\
        has to be marked by surrounding brackets, e.g.:\
        (\\d\\d\\d).jpg$. Make sure to escape the \\ character with another \\ or use single \
        (') or double (\") quotation marks around the pattern to prevent the command line \
        interpret a single \\ as an escape character.\
        For example if you want the pattern to be (\\d\\d).jpg$ use the following syntax:\
        --index-pattern '(\\d\\d).jpg$' or --index-pattern (\\\\d\\\\d).jpg$\
        The default value is '(\\d\\d\\d).jpg$'.")
    parser.add_argument('--index-shift', dest='index_shift', type=int, help="An integer number,\
        defines how the facsimile images will be labeld.\
        If not supplied, the first facsimile will be labeled as 'page_1'. If supplied, the value will\
        be subtracted from the image's index number. For example if index-shift is set to 10\
        facsimile_001.jpg will be labeled 'page_-9' and facsimile_011 will be 'page_1'")
    parser.add_argument('--uri-base', dest='uri_base', help="Base of the image file URIs; defaults \
        to 'http://hms.scot/facsimiles/'")
    set_logging(parser)

    args = parser.parse_args()

    # if not args.out:
    #     args.out = "pages.mei"

    if not args.label_base:
        args.label_base = 'page_'

    if not args.index_pattern:
        args.index_pattern = '(\d\d\d).jpg$'

    if args.filter:
        prog = re.compile(args.filter)

    if args.filter_ignore:
        prog_ignore = re.compile(args.filter_ignore)

    if not args.index_shift:
        args.index_shift = 0

    if not args.uri_base:
        args.uri_base = 'http://hms.scot/facsimiles/'

    doc = pymei.MeiDocument()
    mus = pymei.MeiElement("music")
    facs = pymei.MeiElement('facsimile')
    mus.addChild(facs)
    doc.root = mus

    xml_namespace = pymei.MeiNamespace('xml', 'http://www.w3.org/XML/1998/namespace')
    xml_base = pymei.MeiAttribute(xml_namespace, 'base', 'http://hms.scot/facsimiles/')
    facs.addAttribute(xml_base)

    if args.recursive:
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                    surf = process_img(args, os.path.join(args.dir, file))
                    facs.addChild(surf)
    else:
        logging.debug('list of files: \n')
        for file in os.listdir(args.dir):
            logging.debug(str(file))
            if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                surf = process_img(args, os.path.join(args.dir, file))
                facs.addChild(surf)

    if args.out:
        pymei.XmlExport.meiDocumentToFile(doc, args.out)
    else:
        meitxt = pymei.XmlExport.meiDocumentToText(doc)
        print meitxt


