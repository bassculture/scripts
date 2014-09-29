'''
'
' book.py 
'
' Merge pages.mei and tunes.mei into a single MEI file. tunes.mei 
' contains the musical text, and pages.mei contains the facsimile 
' elements. The script links the mdiv elements to the graphic elements
' so that every tune points to its facsimile image.
'
'''

import pymei
import sys
import os
import argparse
import re
import logging

from utilities import set_logging, get_descendants

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merges pages.mei and tunes.mei.')
    parser.add_argument('pages', help="mei containing a facsimile element with the images and pages")
    parser.add_argument('tunes', help="mei containing the encoded tunes as strain incipits and cadences")
    parser.add_argument('--out', dest='out', help="the path of the output file;\
        if not supplied the output will be writted to the standard output")
    set_logging(parser)
    args = parser.parse_args()

    logging.info('reading pages from: ' + str(args.pages))
    pages_doc  = pymei.XmlImport.documentFromFile(args.pages)
    logging.info('reading tunes from: ' + str(args.tunes)) 
    tunes_doc  = pymei.XmlImport.documentFromFile(args.tunes)

    logging.info('creating MEI elements.')

    facsimile   = pymei.MeiElement(pages_doc.getElementsByName('facsimile')[0])
    music_group = pymei.MeiElement(tunes_doc.getElementsByName('group')[0])


    music = pymei.MeiElement("music")
    music.addChild(facsimile)
    music.addChild(music_group)

    book_doc = pymei.MeiDocument()
    mei = pymei.MeiElement('mei')
    book_doc.root = mei
    mei.addChild(music)

    logging.info('merging mdivs...')
    mdivs = get_descendants(music_group, 'mdiv')
    for mdiv in mdivs:
        label = mdiv.getAttribute('label')
        if (label):
            target = label.value + '.jpg'        
            logging.debug('linking ' + target)
            graphics = get_descendants(facsimile, 'graphic[target=' + target + ']')
            if len(graphics) > 0:
                graphic = graphics[0]
                mdiv.addAttribute('facs', '#' + graphic.id)
            else:
                logging.warning('graphic with @target=\'' + target + '\' not found')
        else:
            logging.warning('missing label attribute at mdiv#' + mdiv.id)
    if args.out:
        logging.info('writing output...')
        pymei.XmlExport.meiDocumentToFile(book_doc, args.out)
    else:
        meitxt = pymei.XmlExport.meiDocumentToText(book_doc)
        print meitxt
