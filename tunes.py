'''
'
' tunes.py
' 
' Go throuhg the incipit MEI files in a given folder. Each MEI file
' represents a tune in a book. Merge these files together to a single
' MEI file containing a <group> of <music> elements.
'
'''

import pymei
import sys
import os
import argparse
import re
import logging
import string

from utilities import set_logging, get_descendants

def process_tune(args, filename, music_group, index):
    logging.info("Processing file: " + filename)
    doc = pymei.XmlImport.documentFromFile(filename)
    music = doc.getElementsByName('music')[0]
    fileDesc = doc.getElementsByName('fileDesc')[0]
    subtitles = get_descendants(fileDesc, 'title[type=subtitle]')
    title = get_descendants(fileDesc, 'title')[0]
    if (music):
        music_copy = pymei.MeiElement(music)
        music_copy.addAttribute('n', 'tune-' + str(index))
        music_copy.addAttribute('label', title.getValue())
        music_group.addChild(music_copy)
        mdiv = get_descendants(music_copy, 'mdiv')[0]
        if (len(subtitles)>0):
            mdiv.addAttribute('label', subtitles[0].getValue())
        filename_tokens = string.split(os.path.basename(filename), '.')
        if filename_tokens != None and len(filename_tokens)>0:
            mdiv.addAttribute('label', filename_tokens[0])
    return music_group


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialise tunes.mei \
        from a set of MEI files.')
    parser.add_argument('dir', help="The path to the folder where the MEI files are located.")
    parser.add_argument('--out', dest='out', help="The path to the output file;\
        if not supplied the output will be written to the standard output")
    parser.add_argument('--filter', dest='filter', help="A regular expression filter;\
        only the matching files will be included")
    parser.add_argument('--ignore', dest='filter_ignore', help="A regular expression filter;\
        the matching files will be exluded")
    parser.add_argument('-R', dest='recursive', action='store_true', 
        help="Indicates that the iteration over the directory\
         will be recusrsive recursive")

    set_logging(parser)
    args = parser.parse_args()

    if args.filter:
        prog = re.compile(args.filter)

    if args.filter_ignore:
        prog_ignore = re.compile(args.filter_ignore)

    logging.debug('creating mei document...')
    doc = pymei.MeiDocument()
    music = pymei.MeiElement("music")
    group = pymei.MeiElement("group")
    music.addChild(group)
    doc.root = music

    
    tune_index = 0
    if args.recursive:
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                    logging.debug('processing file')
                    process_tune(args, os.path.join(args.dir, file), group)
                    tune_index += 1
    else:
        for file in os.listdir(args.dir):
            if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                logging.debug('processing file')
                process_tune(args, os.path.join(args.dir, file), group, tune_index)
                tune_index += 1

    if args.out:
        pymei.XmlExport.meiDocumentToFile(doc, args.out)
    else:
        meitxt = pymei.XmlExport.meiDocumentToText(doc)
        print meitxt

