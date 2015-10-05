import sys
sys.path.append(".")
import pprint
import ipaddr
import json
import unittest
import logging
import os
import time
import xmlrunner
from SimpleBalancer import SimpleBalancer
from SciPass import SciPass
from mock import Mock



class TestPrefix(unittest.TestCase):

    def setUp(self):
        self.api = SciPass( logger = logging.getLogger(__name__),
                            config = str(os.getcwd()) + "/t/etc/SciPass.xml" )
        self.datapath = Mock(id=1)        
        self.api.switchJoined(self.datapath)
        self.file = "%016x" % self.datapath.id +  "R&E" + ".json"
        
    def tearDown(self):
        #os.remove(self.file)
        pass

    def test_initial_config(self):
        assert(os.path.isfile(self.file) == 1)
        with open(self.file) as data_file:    
            data = json.load(data_file)
        data = data[0]
        switches = data["switch"].keys()
        assert(switches[0] == "%016x" % self.datapath.id)      
        domain = data["switch"]["%016x" % self.datapath.id]["domain"].keys()
        assert(domain[0] == "R&E")
        groups = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"].keys()
        for group in groups:
            assert(group in ["group1", "group2", "group3", "group4"])         
            sensors = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"][group]["sensors"]
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["prefixes"]
        for prefix in prefixes:
            assert(prefix in ["10.0.17.0/24","10.0.18.0/24","10.0.19.0/24","10.0.20.0/24","::/128"])
        priorities = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["priorities"].keys()
        for priority in priorities:
            assert(priority in ["10.0.17.0/24","10.0.18.0/24","10.0.19.0/24","10.0.20.0/24","::/128"])
            
            
    def test_sensor_prefix_split(self):
        self.api.getBalancer("%016x" % self.datapath.id, "R&E").splitSensorPrefix("group1",ipaddr.IPv4Network("10.0.18.0/24"))
        assert(os.path.isfile(self.file) == 1)
        with open(self.file) as data_file:
            data = json.load(data_file)
        data = data[0]
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"]["group1"]["prefixes"]
        for prefix in prefixes:
            assert(prefix in ["10.0.18.0/25", "10.0.18.128/25"])
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["prefixes"]
        assert("10.0.18.0/25" in prefixes)
        assert("10.0.18.0/25" in prefixes)
        assert("10.0.18.0/24" not in prefixes)

    def test_move_prefix(self):
        self.api.getBalancer("%016x" % self.datapath.id, "R&E").splitSensorPrefix("group1",ipaddr.IPv4Network("10.0.18.0/24"))
        self.api.getBalancer("%016x" % self.datapath.id, "R&E").moveGroupPrefix("group1","group2",ipaddr.IPv4Network("10.0.18.128/25"))
        with open(self.file) as data_file:
            data = json.load(data_file)
        data = data[0]
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"]["group2"]["prefixes"]
        assert("10.0.18.128/25" in prefixes)
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"]["group1"]["prefixes"]
        assert("10.0.18.128/25" not in prefixes)

    def test_add_prefix(self):
        self.api.getBalancer("%016x" % self.datapath.id, "R&E").addGroupPrefix("group1",ipaddr.IPv4Network("10.0.20.0/24"),bw=0)
        with open(self.file) as data_file:
            data = json.load(data_file)
        data = data[0]
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"]["group1"]["prefixes"]
        assert("10.0.20.0/24" in prefixes)
        
    def test_del_prefix(self):
        self.api.getBalancer("%016x" % self.datapath.id, "R&E").addGroupPrefix("group1",ipaddr.IPv4Network("10.0.20.0/24"),bw=0)
        with open(self.file) as data_file:
            data = json.load(data_file)
        data = data[0]
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"]["group1"]["prefixes"]
        assert("10.0.20.0/24" in prefixes)
        self.api.getBalancer("%016x" % self.datapath.id, "R&E").delGroupPrefix("group1",ipaddr.IPv4Network("10.0.20.0/24"))
        with open(self.file) as data_file:
            data = json.load(data_file)
        data = data[0]
        prefixes = data["switch"]["%016x" % self.datapath.id]["domain"]["R&E"]["groups"]["group1"]["prefixes"]
        assert("10.0.20.0/24" not in prefixes)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPrefix)
    return suite



