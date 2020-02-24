# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:24:05 2020

@author: mberutti
"""

class data:
    """ Class for managing, storing, and broadcasting data
        transmitted from the camera.
        
    """
    
    def __init__(self):
        self.results_path = "results"
        self.results = None
        
        self._purge_results()
        
    def _load_results(self):
        """ Load data from results folder into variable
        """
        pass
    
    def _format_for_trans(self, data):
        """ Reformat data so it is compatible for transmission
        """
        pass
    
    def _purge_results(self):
        """ Delete all from results folder
        """
        pass
    
    def _write_results(self, results):
        """ Write to results folder
        """
        pass
    
    def broadcast(self):
        """ Transmit data to recipient
        """
        data = self._load_results()
        data = self._format_for_trans(data)
        pass
    
    def fetch_data(self):
        """ Fetch data from source (camera)
        """
        data = None
        self._write_results(data)
        pass
        
