__author__ = "Akshay Mane"

import requests
import urllib3


# Disable for insecure connections warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FortiManager:
    def __init__(self, host, username="admin", password="admin", vdom="root", verify=False):
        protocol = "https"
        self.host = host
        self.username = username
        self.password = password
        self.vdom = vdom
        self.sessionid = "null"
        self.verify = verify
        if not self.verify:
            protocol = "http"
        self.base_url = f"{protocol}://{host}/jsonrpc"

    # Login Method
    def login(self):
        """
        Log in to FortiManager with the details provided during object creation of this class
        :return: Session
        """
        session = requests.session()
        payload = \
            {
                "method": "exec",
                "params":
                    [
                        {
                            "data": {
                                "passwd": self.password,
                                "user": self.username
                            },
                            "url": "sys/login/user"
                        }
                    ],
                "session": self.sessionid
            }
        payload = repr(payload)
        login = session.post(url=self.base_url, data=payload, verify=self.verify)
        self.sessionid = login.json()['session']
        return session

    def logout(self):
        """
        Logout from FortiManager
        :return: Response of status code with data in JSON Format
        """
        session = requests.session()
        payload = \
            {
                "method": "exec",
                "params":
                    [
                        {
                            "url": "sys/logout"
                        }
                    ],
                "session": self.sessionid
            }
        payload = repr(payload)
        logout = session.post(url=self.base_url, data=payload, verify=self.verify)
        return logout.json()["result"]

    # Adoms Methods
    def get_admos(self, name=False):
        """
        Get all adoms from the FortiManager
        :param name: Can get specific adom using name as a filter
        :return: Response of status code with data in JSON Format
        """
        url = "dvmdb/adom"
        if name:
            url = f"dvmdb/adom/{name}"
        session = self.login()
        payload = \
            {
                "method": "get",
                "params":
                    [
                        {
                            "url": url,
                            "option": "object member"
                        }
                    ],
                "session": self.sessionid
            }
        payload = repr(payload)
        get_adoms = session.post(url=self.base_url, data=payload, verify=False)
        return get_adoms.json()["result"]

    # Policy Package Methods
    def get_policy_packages(self, name=False):
        """
        Get all the policy packages configured on FortiManager
        :param name: Can get specific package using name as a filter
        :return: Response of status code with data in JSON Format
        """
        url = "pm/pkg/adom/root/"
        if name:
            url = f"pm/pkg/adom/root/{name}"
        session = self.login()
        payload = \
            {
                "method": "get",
                "params":
                    [
                        {
                            "url": url
                        }
                    ],
                "session": self.sessionid
            }
        payload = repr(payload)
        get_packages = session.post(url=self.base_url, data=payload, verify=False)
        return get_packages.json()["result"]

    def add_policy_package(self, name):
        """
        Can add your own policy package in FortiManager
        :param name: Specific the Package Name
        :return: Response of status code with data in JSON Format
        """
        url = "pm/pkg/adom/root/"
        session = self.login()
        payload = \
            {
                "method": "set",
                "params":
                    [
                        {
                            "data": [{
                                "name": name,
                                "type": "pkg"
                            }, ],
                            "url": url
                        }
                    ],
                "session": self.sessionid
            }
        payload = repr(payload)
        add_package = session.post(url=self.base_url, data=payload, verify=False)
        return add_package.json()["result"]

    # Firewall Object Methods
    def get_firewall_address_objects(self, name=False):
        """
        Get all the address objects data stored in FortiManager
        :return: Response of status code with data in JSON Format
        """
        url = f"pm/config/adom/root/obj/firewall/address"
        if name:
            url = f"pm/config/adom/root/obj/firewall/address/{name}"
        session = self.login()
        payload = \
            {
                "method": "get",
                "params": [
                    {
                        "url": url
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        get_address_objects = session.post(url=self.base_url, data=payload, verify=self.verify)
        return get_address_objects.json()["result"]

    def add_firewall_address_object(self, name, associated_interface="any", subnet=list, object_type=0,
                                    allow_routing=0):
        """
        Create an address object using provided info
        :param name: Enter object name that is to be created
        :param associated_interface: Provide interface to which this object belongs if any. {Default is kept any}
        :param subnet: Enter the subnet in a list format eg.["1.1.1.1", "255.255.255.255"]
        :param object_type:
        :param allow_routing: Set routing if needed
        :param comment: Can add your comments
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = {
            "method": "add",
            "params": [
                {
                    "data": {
                        "allow-routing": allow_routing,
                        "associated-interface": associated_interface,
                        "name": name,
                        "subnet": subnet,
                        "type": object_type
                    },
                    "url": f"pm/config/adom/root/obj/firewall/address"
                }
            ],
            "session": self.sessionid
        }
        payload = repr(payload)
        add_address_objects = session.post(url=self.base_url, data=payload, verify=self.verify)
        return add_address_objects.json()["result"]

    def update_firewall_address_object(self, name, **data):
        """
        Get the name of the address object and update it with your data

        :param name: Enter the name of the object that needs to be updated
        :param data: You can get the **kwargs parameters with "show_params_for_object_update()" method
        :return: Response of status code with data in JSON Format
        """
        data = self.make_data(_for="object", **data)
        session = self.login()
        payload = \
            {
                "method": "update",
                "params": [
                    {
                        "data": data,
                        "url": f"pm/config/adom/root/obj/firewall/address/{name}"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        update_firewall_object = session.post(url=self.base_url, data=payload, verify=self.verify)
        return update_firewall_object.json()["result"]

    def delete_firewall_address_object(self, object_name):
        """
        Delete the address object if no longer needed using object name

        :param object_name: Enter the Object name you want to delete
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = \
            {
                "method": "delete",
                "params": [
                    {
                        "url": f"pm/config/adom/root/obj/firewall/address/{object_name}"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        delete_address_object = session.post(url=self.base_url, data=payload, verify=self.verify)
        return delete_address_object.json()["result"]

    # Firewall Address Groups Methods
    def get_address_group(self, name=False):
        """
        Get the address groups created in your FortiManager
        :param name: You can filter out the specific address group which you want to see
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        url = "pm/config/adom/root/obj/firewall/addrgrp"
        if name:
            url = f"pm/config/adom/root/obj/firewall/addrgrp/{name}"
        payload = \
            {
                "method": "get",
                "params": [
                    {
                        "url": url
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        get_address_group = session.post(url=self.base_url, data=payload, verify=self.verify)
        return get_address_group.json()["result"]

    def add_address_group(self, name, members=list):
        """
        Create your own group with just 2 parameters
        :param name: Enter the name of the address group                eg."Test_Group"
        :param members: pass your object names as members in a list     eg. ["LAN_10.1.1.0_24, "INTERNET"]
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = \
            {
                "method": "add",
                "params": [
                    {
                        "data": {
                            "name": name,
                            "member": members,
                        },
                        "url": "pm/config/adom/root/obj/firewall/addrgrp"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        add_address_group = session.post(url=self.base_url, data=payload, verify=self.verify)
        return add_address_group.json()["result"]

    def update_address_group(self, name, object_name, do="add"):
        """
        Update Members of the Address group
        :param name: Specify the name of the Address group you want to update
        :param object_name: Specify name of the object you wish to update(add/remove) in Members List
        :param do: Specify if you want to add or remove the object from the members list
                    do="add"    will add the object in the address group
                    do="remove" will remove the object from address group
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        get_addr_group = self.get_address_group(name=name)
        members = get_addr_group[0]['data']['member']
        if do == "add":
            members.append(object_name)
        elif do == "remove":
            members.remove(object_name)

        payload = \
            {
                "method": "update",
                "params": [
                    {
                        "data": {
                            "member": members,
                        },
                        "url": f"pm/config/adom/root/obj/firewall/addrgrp/{name}"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        update_address_group = session.post(url=self.base_url, data=payload, verify=False)
        return update_address_group.json()["result"]

    def delete_address_group(self, name):
        """
        Delete the Address group if no longer needed
        :param name: Specify the name of the address you wish to delete
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = \
            {
                "method": "delete",
                "params": [
                    {
                        "data": {
                        },
                        "url": f"pm/config/adom/root/obj/firewall/addrgrp/{name}"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        delete_address_group = session.post(url=self.base_url, data=payload, verify=False)
        return delete_address_group.json()["result"]

    # Firewall Policies Methods
    def get_firewall_policies(self, policy_package_name="default", policyid=False):
        """
        Get the firewall policies present in the policy package

        :param policy_package_name: Enter the policy package name
        :param policyid: Can filter and get the policy you want using policyID
        :return: Response of status code with data in JSON Format
        """
        url = f"pm/config/adom/root/pkg/{policy_package_name}/firewall/policy/"
        if policyid:
            url = url + str(policyid)
        session = self.login()
        payload = {
            "method": "get",
            "params": [
                {
                    "url": url
                }
            ],
            "session": self.sessionid
        }
        payload = repr(payload)
        get_firewall_policies = session.post(url=self.base_url, data=payload, verify=self.verify)
        return get_firewall_policies.json()["result"]

    def add_firewall_policy(self, policy_package_name="default", name=str, source_interface=str, source_address=str,
                            destination_interface=str, destination_address=str, service=str, schedule="always",
                            action=1, logtraffic=int, ):
        """
        Create your own policy in FortiManager using the instance parameters.

        :param policy_package_name: Enter the name of the policy package                eg. "default"
        :param name: Enter the policy name in a string format                           eg. "Test Policy"
        :param source_interface: Enter the source interface in a string format          eg. "port1"
        :param source_address: Enter the src. address object name in string format      eg. "LAN_10.1.1.0_24"
        :param destination_interface: Enter the source interface in a string format     eg. "port2"
        :param destination_address: Enter the dst. address object name                  eg. "WAN_100.25.1.63_32"
        :param service: Enter the service you want to permit or deny in string          eg. "ALL_TCP"
        :param schedule: Schedule time is kept 'always' as default.
        :param action: Permit(1) or Deny(0) the traffic. Default is set to Permit.
        :param logtraffic: Specify if you need to log all traffic or specific in int format.
                            logtraffic=0: Means No Log
                            logtraffic=1 Means Log Security Events
                            logtraffic=2 Means Log All Sessions
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = {
            "method": "add",
            "params": [
                {
                    "data": {
                        "dstaddr": destination_address,
                        "dstintf": destination_interface,
                        "logtraffic": logtraffic,
                        "name": name,
                        "schedule": schedule,
                        "service": service,
                        "srcaddr": source_address,
                        "srcintf": source_interface,
                        "action": action
                    },
                    "url": f"pm/config/adom/root/pkg/{policy_package_name}/firewall/policy/"
                }
            ],
            "session": self.sessionid
        }
        payload = repr(payload)
        add_policy = session.post(url=self.base_url, data=payload, verify=self.verify)
        return add_policy.json()["result"]

    def update_firewall_policy(self, policy_package_name, policyid, **data):
        """
        Update your policy with your specific needs

        :param policy_package_name: Enter the policy package name in which you policy belongs
        :param policyid: Enter the Policy ID you want to edit
        :param data: You can get the **kwargs parameters with "show_params_for_policy_update()" method
        :return: Response of status code with data in JSON Format
        """
        data = self.make_data(**data)
        session = self.login()
        payload = \
            {
                "method": "update",
                "params": [
                    {
                        "data": data,
                        "url": f"pm/config/adom/root/pkg/{policy_package_name}/firewall/policy/{policyid}"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        update_policy = session.post(url=self.base_url, data=payload, verify=self.verify)
        return update_policy.json()["result"]

    def delete_firewall_policy(self, policy_package_name, policyid):
        """
        Delete the policy if not is use with the policyID

        :param policy_package_name: Enter the policy package name in which you policy belongs
        :param policyid: Enter the policy ID of the policy you want to delete
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = \
            {
                "method": "delete",
                "params": [
                    {
                        "url": f"pm/config/adom/root/pkg/{policy_package_name}/firewall/policy/{policyid}"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        delete_policy = session.post(url=self.base_url, data=payload, verify=self.verify)
        return delete_policy.json()["result"]

    def move_firewall_policy(self, policy_package_name, move_policyid=int, option="before", policyid=int):
        """
        Move the policy as per your needs

        :param policy_package_name: Enter the policy package name in which you policy belongs
        :param move_policyid: Enter the policy ID of the policy you want to move
        :param option: Specify if you want to move above("before") the target policy or below("after") {default: before}
        :param policyid: Specify the target policy
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = \
            {
                "method": "move",
                "params": [
                    {
                        "url": f"pm/config/adom/root/pkg/{policy_package_name}/firewall/policy/{move_policyid}",
                        "option": option,
                        "target": str(policyid)
                    }
                ],
                "session": self.sessionid
            }
        import json
        print(json.dumps(payload, indent=4))
        payload = repr(payload)
        move_policy = session.post(url=self.base_url, data=payload, verify=self.verify)
        return move_policy.json()["result"]

    def install_policy_package(self, package_name):
        """
        Install the policy package on your Fortigate Firewalls

        :param package_name: Enter the package name you wish to install
        :return: Response of status code with data in JSON Format
        """
        session = self.login()
        payload = \
            {
                "method": "exec",
                "params": [
                    {
                        "data": {
                            "adom": "root",
                            "pkg": f"{package_name}"
                        },
                        "url": "securityconsole/install/package"
                    }
                ],
                "session": self.sessionid
            }
        payload = repr(payload)
        install_package = session.post(url=self.base_url, data=payload, verify=self.verify)
        return install_package.json()["result"]

    @staticmethod
    def make_data(_for="policy", **kwargs):
        object_maps = \
            {
                "allow_routing": "allow-routing",
                "associated_interface": "associated-interface",
                "comment": "comment",
                "object_name": "name",
                "subnet": "subnet",
                "object_type": "type"
            }
        policy_maps = \
            {
                "name": "name",
                "source_interface": "srcintf",
                "source_address": "srcaddr",
                "destination_interface": "dstintf",
                "destination_address": "dstaddr",
                "service": "service",
                "schedule": "schedule",
                "action": "action",
                "logtraffic": "logtraffic",
                "comment": "comments"
            }

        data = {}
        for key, value in kwargs.items():
            if _for == "policy":
                key = key.replace(key, policy_maps[key])
            elif _for == "object":
                key = key.replace(key, object_maps[key])
            data.update({key: value})
        return data

    @staticmethod
    def show_params_for_object_update():
        docs = \
            """
        Parameters to create/update address object:

        PARAMETERS                   FIREWALL OBJECT SETTINGS
        allow_routing(int)          : Static Route Configuration
        associated_interface(str)   : Interface
        comment(str)                : Comments
        object_name(str)            : Address Name
        subnet[list]                : IP/Netmask
        object_type(int)            : Type
        """
        return docs

    @staticmethod
    def show_params_for_policy_update():
        docs = \
            """
        Parameters to create/update Policy:

        PARAMETERS                       FIREWALL POLICY SETTINGS
        name(str)                       : Name
        source_interface(str)           : Incoming Interface
        source_address(str)             : Source Address
        destination_interface(str)      : Destination Interface
        destination_address(str)        : Destination Address
        service(str)                    : Service
        schedule(str)                   : Schedule
        action(int)                     : Action
        logtraffic(int)                 : Log Traffic
        comment(str)                    : Comments
        """
        return docs
