from os import path as os_path
import os
import numpy as np
import codecs
import json 
import copy



MASKED_VALUE = -9999

class JsonFile:
    
    
    def __init__(self, fname):
        self.fname = fname
        self.data = None

    def write_data(self, data):
        print ('enter write')
        self.data = copy.deepcopy(data)
        if type(data) is np.ndarray or type(data) is np.ma.core.MaskedArray:
            self.data = self.data.tolist(MASKED_VALUE) # nested lists with same data, indices. Replace masked values by MASKED_VALUE = -9999
        with codecs.open(self.fname, 'w', encoding='utf-8') as fp:
            json.dump(self.data, fp, separators=(',', ':'), sort_keys=True, indent=4)
    
    def read_data(self):
        print ('enter read')
        with codecs.open(self.fname, 'r', encoding='utf-8') as fp:
            obj_text = fp.read()
            data = json.loads(obj_text)
            dataNew = np.ma.masked_equal(data, MASKED_VALUE)
            self.data = dataNew
        return dataNew

            
if __name__ == "__main__":
    data = np.ma.array(np.arange(9).reshape(3, 3), mask=np.eye(3))
    print (type (data))
    file_path = "path.json" ## your path variable
    f = JsonFile(file_path)
    f.write_data(data)
    dataNew = f.read_data()
    print (data)
    print (type(data))
    print (dataNew)
    print (type(dataNew))


