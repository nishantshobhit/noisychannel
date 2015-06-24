# python search.py --index index.csv --query queries/103100.png
# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

def search_results(filename, index_file):
    # load the query image and describe it
    query = cv2.imread(filename)
    features = cd.describe(query)

    # perform the search
    searcher = Searcher(index_file)
    results = searcher.search(features)


# loop over the results
#for (score, resultID) in results:
#    print score, resultID

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--index", required = True,
                    help = "Path to where the computed index will be stored")
    ap.add_argument("-q", "--query", required = True,
                    help = "Path to the query image")
    #ap.add_argument("-r", "--result-path", required = True,	help = "Path to the result path")
    args = vars(ap.parse_args())
    results = search_results(args["query"], args["index"])
    print "\n".join(results)

if __name__ == '__main__':
    main()
