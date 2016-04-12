#! /usr/bin/env python

# Copyright (c) 2016 IBM Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
import httplib
import json
import yaml

DEBUG = False

class MoltenIron(object):

    def __init__(self):
        self.conf = self.read_conf()
        # Parse the arguments and generate a request
        parser = argparse.ArgumentParser()
        parser.add_argument('command', help='Subcommand to run')
        args=parser.parse_args(sys.argv[1:2])

        request = getattr(self, args.command)()

        # Send the request and print the response
        response = self.send(request)
        print response

    def add(self):
        """
        Generate a request to add a node to the MoltenIron database
        """
        parser = argparse.ArgumentParser(
            description='Add a node to the micli')
        parser.add_argument('name', help="Name of the baremetal node")
        parser.add_argument('ipmi_ip', help="IP for issuing IPMI commands to this node")
        parser.add_argument('ipmi_user', help="IPMI username used when issuing IPMI commands to this node")
        parser.add_argument('ipmi_password', help="IPMI password used when issuing IPMI commands to this node")
        parser.add_argument('allocation_pool', help="Comma separated list of IPs to be used in deployment")
        parser.add_argument('port_hwaddr', help="MAC address of port on machine to use during deployment")
        parser.add_argument('cpu_arch', help="Architecture of the node")
        parser.add_argument('cpus', type=int, help="Number of CPUs on the node")
        parser.add_argument('ram_mb', type=int, help="Amount of RAM (in MiB) that the node has")
        parser.add_argument('disk_gb', type=int, help="Amount of disk (in GiB) that the node has")

        args = parser.parse_args(sys.argv[2:])
        request = vars(args)
        request['method']='add'
        return request

    def allocate(self):
        """
        Generate a request to checkout a node from the MoltenIron database
        """
        parser = argparse.ArgumentParser(
            description="Checkout a node in molteniron. Returns the node's info")
        parser.add_argument('owner_name', help="Name of the requester")
        parser.add_argument('number_of_nodes', type=int, help="How many nodes to reserve")

        args = parser.parse_args(sys.argv[2:])
        request =  vars(args)
        request['method']='allocate'
        return request

    def release(self):
        """
        Generate a request to release an allocated node from the MoltenIron database
        """
        parser = argparse.ArgumentParser(
            description='Given an owner name, release allocated node, returning it to the available state')
        parser.add_argument('owner_name', help='Name of the owner who currently owns the nodes to be released')
        args = parser.parse_args(sys.argv[2:])

        request =  vars(args)
        request['method']='release'
        return request

    def get_field(self):
        """
        Generate a request to return a field of data from an owned node from the MoltenIron database
        """
        parser = argparse.ArgumentParser(
            description='Given an owner name and the name of a field, get the value of the field')

        parser.add_argument('owner_name', help='Name of the owner who currently owns the nodes to get the field from')
        parser.add_argument('field_name', help='Name of the field to retrieve the value from')

        args = parser.parse_args(sys.argv[2:])
        request =  vars(args)
        request['method']='get_field'
        return request

    def status(self):
        """
        """
        parser = argparse.ArgumentParser(
            description='Return a list of current MoltenIron Node database entries')

        args = parser.parse_args(sys.argv[2:])
        request =  vars(args)
        request['method']='status'
        return request

    def send(self, request):
        """
        Send the generated request
        """
        node = {'name': 'test'}
        connection = httplib.HTTPConnection(str(self.conf['serverIP']),
                                            int(self.conf['mi_port']))
        connection.request('POST', '/', json.dumps(request))

        response      = connection.getresponse()
        response_str  = response.read()
        response_json = json.loads(response_str)

        if DEBUG:
            print response_json

        return response_str

    def read_conf(self):
        """
        Read ./conf.yaml in
        """
        path = sys.argv[0]
        dirs = path.split("/")
        newPath = "/".join(dirs[:-1]) + "/"

        fobj = open(newPath + "conf.yaml", "r")
        conf = yaml.load(fobj)
        return conf

if __name__=="__main__":
    MoltenIron()
