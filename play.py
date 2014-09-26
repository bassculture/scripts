import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialise MEI pages from a set of images undera folder')
    parser.add_argument('--index-pattern', dest='index_pattern', help="A regular expression defining\
        the patter of the page numbers; defaults to '(\\d\\d\\d).jpg$'")

    args = parser.parse_args()

    print args.index_pattern