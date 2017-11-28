from os import path as os_path
import os
import csv

class CsvFile:

    def __init__(self, fname):
        self.fname = fname
        self.data = None

    def read_data(self, skip_first_line = False, ignore_first_column = False):
        '''
        Function juste for NLNOG data
        to load data from .log file and returns the corresponding list.
        @param filename: log file name.
        @type filename: str
        @param skip_first_line: if True, the first line is not read. Default value: False.
        @type skip_first_line: boolean
        @param ignore_first_column: if True, the first column is ignored. Default value: False.
        @type ignore_first_column: boolean
        @return: a list of lists, each list being a row in the data file. Rows are returned in the same order as in the file.
        '''
        f = open(self.fname,'r')
        if skip_first_line:
            f.readline()
        data = []
        for line in f:
            line = line.split(" ")
            line[0:] = [ float(x) for x in line[0:] ]
            if ignore_first_column:
                line = line[1:]
            data.append(line)
        f.close()
        self.data = data
        return data

    def write_data(self, data):
        '''
        Writes data in a csv file where first line is the Id (begins with 0) and first column is the number of line (begins with 0).
        @param data: a list of lists
        @param filename: the path of the file in which data is written.
            The file is created if necessary; if it exists, it is overwritten.
        '''
        rrt = data
        self.data = data
        f = open(self.fname, 'w')
        #add first line of numbers in the file 
        ls = []
        ls.append('Probes')
        for i in range(0,len(rrt[0])):
            ls.append(i)
        spamwriter = csv.writer(f, delimiter=",")
        spamwriter.writerow(ls)
        #add data in the file
        i=0
        for item in rrt:
            # add a number in the beginning of every line
            # write every line in the file
            f.write(','.join([str(i)]+[repr(x) for x in item]))
            f.write('\n')
            i = i + 1
        f.close()

    def read_dataCsv(self, skip_first_line = True, ignore_first_column = True):
        '''
        Loads data from a csv file and returns the corresponding list.
        All data are expected to be floats, except in the first column and the first row.
        @param filename: csv file name.
        @param skip_first_line: if True, the first line is not read. Default value: True.
        @param ignore_first_column: if True, the first column is ignored. Default value: True.
        @return: a list of lists, each list being a row in the data file. Rows are returned in the same order as in the file.
        '''
        f = open(self.fname,'r')
        if skip_first_line:
            f.readline()
        data = []
        for line in f:
            line = line.split(",")
            line[0:] = [ float(x) for x in line[0:] ]
            if ignore_first_column:
                line = line[1:]
            data.append(line)
        f.close()
        self.data = data
        return data




if __name__ == "__main__":
    path = '/'.join(os_path.abspath(os_path.split(__file__)[0]).split('/')[:-1])
    os.chdir(path)
    print (path)
    f = csvFile('RTT_RipeAtlas2/oneTimedata.csv')
    data =  f.read_dataCsv()
    f2 = csvFile('oneTimeData.csv')
    f2.write_data(f.data)




    
