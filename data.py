# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:24:05 2020

@author: mberutti
"""

class Data:
    """ Class for managing, storing, and broadcasting data
        transmitted from the camera.
    """
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.results = None
        
        self._purge_results()
        
    def _load_results(self):
        """ Load data from results folder into variable
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
    
    def pepare_broadcast(self):
        """ Prepare data for transmission
        """
        data = self._load_results()
        data = self._format_for_trans(data)
        
        return data
    
    def fetch_data(self):
        """ Fetch data from source (camera)
        """
        data = None
        self._write_results(data)
        pass
    

class Broadcast:
    """ Class for connecting to a peer and transmitting data.
    """
    
    def __init__(self, peer):
        self.peer = peer

        self._connect()

    def _connect(self):
        """ Connect to peer
        """
        if not self._verify_connection():
            raise RuntimeError("Could not connect to peer.")

    def _verify_connection(self):
        """ Check if connected to peer
        """
        connected = False

        return connected

    def broadcast_data(self, data):
        """ Transmit data to peer
        """
        if not self._verify_connection():
            self._connect()
        pass

    def read_data(self):
        """ Accept data from peer
        """
        pass
