'''
Created on Aug 8, 2016

@author: klein
'''

import os

class NMR(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        initializes the NMR run program
        '''
        
    def Analyzer(self, Image,CommandArgs):
        """ runs analyzer, where the commandargs have been created by anacontrol"""
        self.FullCommand = Image +' '+CommandArgs
        os.system(self.FullCommand)
        
        
        
        
        
        
    def RunShort(self):
        """runs converter"""
        