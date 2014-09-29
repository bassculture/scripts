# Bass Culture Scripts

These scripts have been created to facilitate MEI file production

## Musical Content 

There following three scripts facilitate the production of the musical content (facsimile elements and encoded musical text)

1. pages.py: Initialise MEI facsimile elements from a set of images.
2. tunes.py: Takes a set of MEI files containing music content, and merges together in a music/group structure.
3. book.py: Takes a the output of pages.py and tunes.py. It establishes the connection between the tunes and the facsimile where they were originally transcribed.

### Usage

For detailed description of the arguments run each script with `--help`.

#### pages.py

The following command will write to the standard output an MEI containing the a single facsimile elemenets containing a one surface element for each image
file in the  `/test/Ca11-y-_24` folder. 

`python pages.py /test/Ca11-y-_24/jpeg --filter '.*\.jpg' --index-patter '(\d\d).jpg$' --index-shift 14`

The surface elements will be labeled with the page number. The `index-shift` parameter tells the script that the first page is on `image_15.jpg` (the value of the `image-shift` paramter is substracted from the page index.) The index number is retrieved from the filename. The regular expression `index-pattern` defines the way the index is retrieved from the filename. The regular exression `'(\d\d).jpg$'` tells the script to look for a two-digit (zero-padded) index number followed by the `jpg` extension.

#### tunes.py

The following command merges the music elements found in the MEIs under the given folder into a single MEI file, and writes it to the standard output

`python tunes.py /test/Ca11-y-_24/strains --filter '.*\.mei$'`


#### book.py

The following merges the two MEI files into a single MEI and saves the result into the file `/test/Ca11-y-_24/book.mei`

`python book.py /test/Ca11-y-_24/header.mei /test/Ca11-y-_24/pages.mei /test/Ca11-y-_24/tunes.mei --out /test/Ca11-y-_24/book.mei`

## Metadata

The meimeta module deals with the production of the meiHead.

To see how it works, see the tests in under the meimeta/test folder. 

