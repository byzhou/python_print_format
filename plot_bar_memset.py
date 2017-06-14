import sys, os, re, random
import numpy as np
import scipy.stats as scpstats
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_calloc_time(data_set):
    data_base           = {}
    for times in np.arange(1,11):
        memset_file     = "malloc_time_in_calloc_" + str(times) + "/" + data_set + ".csv"
        calloc_file     = "spec_" + str(times) + "/" + data_set + "_calloc.log" 
        # print "Reading file " + calloc_file + " ..."
        # print "Reading file " + memset_file + " ..."

        read_calloc_file    = open(calloc_file, 'r')
        read_memset_file    = open(memset_file, 'r')
        
        for lines in read_calloc_file:
            bm_name         = lines.split(' ')[0]
            data_base[bm_name]  = {}
            if 'total_time' not in data_base[bm_name]:
                data_base[bm_name]['total_time']    = []
            data_base[bm_name]['total_time']        = float(lines.split(' ')[2]) - float(lines.split(' ')[1])
        for lines in read_memset_file:
            bm_name         = lines.split(' ')[0].split('_')[0]
            if bm_name not in data_base:
                data_base[bm_name]                  = {}
            if 'memset_time' not in data_base[bm_name]:
                data_base[bm_name]['memset_time']   = 0
            data_base[bm_name]['memset_time']       += float(lines.split(' ')[1].split('\n')[0])
        read_calloc_file.close()
        read_memset_file.close()

        
        for bm_name in data_base:
            if 'list_of_total_time' not in data_base[bm_name]:
                data_base[bm_name]['list_of_total_time']    = []
            else:
                if 'total_time' not in data_base[bm_name]:
                    sys.exit("Total time has not been read properly!")
            data_base[bm_name]['list_of_total_time'].append(data_base[bm_name]['total_time'])

            if 'list_of_memset_time' not in data_base[bm_name]:
                data_base[bm_name]['list_of_memset_time']    = []
            else:
                if 'memset_time' not in data_base[bm_name]:
                    sys.exit("Memset time has not been read properly!")
            data_base[bm_name]['list_of_memset_time'].append(data_base[bm_name]['memset_time'])
            
    for bm_name in data_base:
        data_base[bm_name]['average_total_time']    = np.average(data_base[bm_name]['list_of_total_time'])
        data_base[bm_name]['average_memset_time']   = np.average(data_base[bm_name]['list_of_memset_time'])
        data_base[bm_name]['percentage_of_memset']  = data_base[bm_name]['average_memset_time']/data_base[bm_name]['average_total_time'] * 100
    
    print '|{0:16}| {1:10}|'.format('Benchmark(' + data_set + ')','Init Time')
    print '|{0:16}| {1:10}|'.format('---', '---')
    
    for bm_name in data_base:
        print '|{0:16}|{1:10.3f}%|'.format(bm_name, data_base[bm_name]['percentage_of_memset'])
    
    print 'Arith mean is {0:.3f}%'.format(np.average([data_base[bm_name]['percentage_of_memset'] for bm_name in data_base]))
    #print 'Geo mean is   {0:.3f}%'.format(scpstats.gmean([data_base[bm_name]['percentage_of_memset'] for bm_name in data_base]))

plot_calloc_time('test')
plot_calloc_time('train')
plot_calloc_time('ref')
