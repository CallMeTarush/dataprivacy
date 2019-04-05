import argparse
import csv
import itertools
import time

class Anonymizer:

    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.checkColumns = None
        print "Input:",self.inputFile
        print "Output:",self.outputFile

    def parseColRange(self, rangeStr):
        result = set()
        for part in rangeStr.split(','):
            x = part.split('-')
            result.update(range(int(x[0]), int(x[-1])+1))
        self.checkColumns = sorted(result)
        if len(self.checkColumns) == 0:
            raise Exception("Please enter column index!")

    def anonymize(self):
        
        csvInputFile = open(self.inputFile, 'rb')
        csvInputFileReader = csv.reader(csvInputFile, dialect='excel')
        csvOutputFile = open(self.outputFile, 'wb')
        csvOutputWriter = csv.writer(csvOutputFile, dialect='excel')
        header = csvInputFileReader.next()
        cols = zip(*csvInputFileReader)
        randz = []
        for i in self.checkColumns:
            unique_entry = sorted(set(cols[i]))

            print(unique_entry, "unique_entry")
        
            cleanCol = []
        
            for j,item in enumerate(cols[i]):
                try:
                    uid = unique_entry.index(item)
                    cleanCol.append('user' + str(uid))
                except ValueError:
                    cleanCol.append(self.noUser)
            cols[i] = cleanCol
    
        csvOutputWriter.writerow(header)
        csvOutputWriter.writerows(itertools.izip_longest(*cols, fillvalue=''))
        csvInputFile.close()
        csvOutputFile.close()

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="Please input file")
    parser.add_argument("-c", required=True, help="Please enter comma seperated values")
    parser.add_argument("-o", "--output", required=True, help="Please enter output files")
    args = parser.parse_args()
    
    startTime = time.time()
    anon = Anonymizer(args.i, args.output)
    anon.parseColRange(args.c)
    anon.anonymize()
    print "Done in ", time.time() - startTime, " secs"

if __name__ == "__main__":
    main()