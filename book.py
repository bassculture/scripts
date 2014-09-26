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
    parser = argparse.ArgumentParser(description='Merges pages.mei and tunes.mei. \
        NB.: this function should ideally merge the header.mei as well, but \
        due to current libmei issues (FRBR module isn\'t included in the build \
        this has to be done manually. Once the libmei module is recompiled and \
        able to handle the FRBR module, this script should be updated to \
        so that it merges the header.mei too.')
    parser.add_argument('header', help="file containing the mei header")
    parser.add_argument('pages', help="mei containing a facsimile element with the images and pages")
    parser.add_argument('tunes', help="mei containing the encoded tunes as strain incipits and cadences")
    parser.add_argument('--out', dest='out', help="the path of the output file;\
        if not supplied the output will be writted to the standard output")
    set_logging(parser)
    args = parser.parse_args()

    header_doc = pymei.XmlImport.documentFromFile(args.header)
    pages_doc  = pymei.XmlImport.documentFromFile(args.pages)
    tunes_doc  = pymei.XmlImport.documentFromFile(args.tunes)
    
    meiHead     = pymei.MeiElement(header_doc.getElementsByName('meiHead')[0])
    facsimile   = pymei.MeiElement(pages_doc.getElementsByName('facsimile')[0])
    music_group = pymei.MeiElement(tunes_doc.getElementsByName('group')[0])


    music = pymei.MeiElement("music")
    music.addChild(facsimile)
    music.addChild(music_group)

    book_doc = pymei.MeiDocument()
    mei = pymei.MeiElement('mei')
    book_doc.root = mei
    mei.addChild(meiHead)
    mei.addChild(music)

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
        pymei.XmlExport.meiDocumentToFile(book_doc, args.out)
    else:
        meitxt = pymei.XmlExport.meiDocumentToText(book_doc)
        print meitxt
