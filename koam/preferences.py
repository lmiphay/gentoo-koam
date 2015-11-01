#!/usr/bin/python

import os
import pickle
import yaml
import koam

class KoamPreferences:

    KOAMDIR = os.path.expanduser('~/.koam')
    SERVERS = KOAMDIR + '/koam.servers'

    def __init__(self):
        self.servers = set()
        koam.KoamObserver.connect_add(self.add_handler)
        koam.KoamObserver.connect_rem(self.remove_handler)

    def load(self):
        if os.path.exists(self.SERVERS):
            self.yaml_load()
            for server in self.servers:
                koam.KoamObserver.add_server(server)
            return True
        else:
            return False

    def save(self):
        if not os.path.isdir(self.KOAMDIR):
            os.mkdir(self.KOAMDIR)
        self.yaml_save()

    def pickle_load(self):
        self.servers = pickle.load(open(self.SERVERS, 'r'))
        
    def pickle_save(self):
        pickle.dump(self.servers, open(self.SERVERS, 'w'))

    def yaml_load(self):
        self.servers = yaml.load(open(self.SERVERS, 'r'))
        
    def yaml_save(self):
        yaml.dump(self.servers, open(self.SERVERS, 'w'))
        
    def add_handler(self, server):
        self.servers.add(server)

    def remove_handler(self, server):
        if server in self.servers:
            self.servers.remove(server)
