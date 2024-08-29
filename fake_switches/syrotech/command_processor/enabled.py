# Copyright 2015-2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import textwrap

from fake_switches.command_processing.base_command_processor import BaseCommandProcessor


class EnabledCommandProcessor(BaseCommandProcessor):
    def __init__(self, config):
        super(EnabledCommandProcessor, self).__init__()
        self.config_processor = config

    def get_prompt(self):
        return self.switch_configuration.name + "#"

    def do_enable(self, *args):
        pass

    def do_configure(self, *_):
        self.write_line("Enter configuration commands, one per line.  End with CNTL/Z.")
        self.move_to(self.config_processor)

    def do_show(self, *args):
        if "running-config".startswith(args[0]):
            if len(args) < 2:
                self.show_run()
            elif "interface".startswith(args[1]):
                if_name = "".join(args[2:])
                port = self.switch_configuration.get_port_by_partial_name(if_name)

                if port:
                    self.write_line("Building configuration...")
                    self.write_line("")

                    data = ["!"] + build_running_interface(port) + ["end", ""]

                    self.write_line("Current configuration : %i bytes" % (len("\n".join(data)) + 1))
                    [self.write_line(l) for l in data]
                else:
                    self.write_line("                               ^")
                    self.write_line("% Invalid input detected at '^' marker.")
                    self.write_line("")
        elif "version".startswith(args[0]):
            self.show_version()
        elif "onu info".startswith(args[0]):
            self.show_onu_info()
        else:
            self.write_line("                               ^")
            self.write_line("% Invalid input detected at '^' marker.")
            self.write_line("")    

    def do_terminal(self, *args):
        pass

    def do_write(self, *args):
        self.write_line("Building configuration...")
        self.switch_configuration.commit()
        self.write_line("OK")

    def do_exit(self):
        self.is_done = True

    def show_onu_info(self):
        all_data = [
        "GPON0/1:1  unknown              default                sn      GNXS9390051b",
        "GPON0/1:2  unknown              default                sn      GNXSb2b006bd",
        "GPON0/1:3  unknown              default                sn      GNXSb2b006a6",
        "GPON0/1:4  unknown              default                sn      GPON0001c160",
        "GPON0/1:5  unknown              default                sn      GNXS62600911",
        "GPON0/1:6  unknown              default                sn      GNXS22606911",
        "GPON0/3:1  unknown              default                sn      GPON0073b5c6",
        "GPON0/3:2  unknown              default                sn      RLEM4a3bf46e",
        "GPON0/3:3  unknown              default                sn      PPCT924a2fc7",
        "GPON0/3:4  unknown              default                sn      XPON21924586",
        "GPON0/3:5  unknown              default                sn      GNXS93305a8d",
        "GPON0/3:6  unknown              default                sn      GNXS62600911",
        "GPON0/3:7  unknown              default                sn      DBCG1c359a72",
        "GPON0/3:8  unknown              default                sn      XPON495ba7f8",
        "GPON0/3:9  unknown              default                sn      MONU00d5e0d3",
        "GPON0/3:10 unknown              default                sn      GNXS81900db1",
        "GPON0/3:11 unknown              default                sn      XPONd000d770",
        "GPON0/3:12 unknown              default                sn      GNXS23800755",
        "GPON0/3:13 unknown              default                sn      GPON002ef898",
        "GPON0/3:14 unknown              default                sn      GPON0015ff20",
        "GPON0/3:15 unknown              default                sn      PPCT92be0b1c",
        "GPON0/3:16 unknown              default                sn      RLGM4aae98d0",
        "GPON0/3:17 unknown              default                sn      GNXS010c7530",
        "GPON0/3:18 unknown              default                sn      GPON0064bb90",
        "GPON0/3:19 unknown              default                sn      GNXS9290180f",
        "GPON0/3:20 unknown              default                sn      GPON0043ae20",
        "GPON0/3:21 unknown              default                sn      XPON498303a0",
        "GPON0/3:22 unknown              default                sn      GNXSb2b006ac",
        "GPON0/3:23 unknown              default                sn      PPCT92bae492",
        "GPON0/3:24 unknown              default                sn      XPON4939d2e0",
        "GPON0/3:25 unknown              default                sn      XPON0025b9e9",
        "GPON0/3:26 unknown              default                sn      RLGM4a567760",
        "GPON0/3:27 unknown              default                sn      GNXS1631188c",
        "GPON0/3:28 unknown              default                sn      GPON004db127",
        ]
        self.write_line("Onuindex   Model                Profile                Mode    AuthInfo ")
        self.write_line("---------------------------------------------------------------------------------------------")
        for l in all_data:
            self.write_line(l)
            self.write_line("")
        
    def show_run(self):
        all_data = [
        "!",
        "!Software Version      :		V1.4.3RS",
        "!Software Created Time :		Wed, 22 Nov 2023 13:36:52 ",
        "hostname taclab48-syrotech-gpon-8",
        "log trap emergencies",
        "syslog server ip 172.31.251.36 port 514",
        "!",
        "line vty",
        "exit",
        "!",
        "security-dos",
        "dos prevent level off ",
        "exit",
        "!",
        "interface aux",
        "ip address 192.168.25.25 255.255.255.0",
        "ipv6 address fec0::bab7:dbff:fec7:eda9/64",
        "exit",
        "interface loopback",
        "ip address 127.0.0.1 255.0.0.0",
        "ipv6 address ::1/128",
        "exit",
        ]
        for interface in self.switch_configuration.get_physical_ports() + self.switch_configuration.get_vlan_ports():
            all_data = all_data + build_running_interface(interface) + ["!"]
        all_data += ["end", ""]

        self.write_line("Building configuration...")
        self.write_line("")

        self.write_line("Current configuration : %i bytes" % (len("\n".join(all_data)) + 1))
        [self.write_line(l) for l in all_data]

    def show_version(self):
        self.write_line(version_text(
            hostname=self.switch_configuration.name,
        ))


def version_text(**kwargs):
    return textwrap.dedent(u"""
        !
        !Software Version      :		V1.4.3RS
        !Software Created Time :		Wed, 22 Nov 2023 13:36:52 
        hostname taclab48-syrotech-gpon-8
        log trap emergencies
        syslog server ip 172.31.251.36 port 514
        !
        line vty
        exit
        !
        security-dos
        dos prevent level off 
        exit
        !
        interface aux
        ip address 192.168.25.25 255.255.255.0
        ipv6 address fec0::bab7:dbff:fec7:eda9/64
        exit
        interface loopback
        ip address 127.0.0.1 255.0.0.0
        ipv6 address ::1/128
        exit
        """.format(**kwargs))[1:]

def build_running_interface(port):
    data = [
        "interface %s" % port.name
    ]
    if port.description:
        data.append(" description %s" % port.description)
    if port.access_vlan and port.access_vlan != 1:
        data.append(" switchport access vlan %s" % port.access_vlan)
    if port.trunk_encapsulation_mode is not None:
        data.append(" switchport trunk encapsulation %s" % port.trunk_encapsulation_mode)
    if port.trunk_native_vlan is not None:
        data.append(" switchport trunk native vlan %s" % port.trunk_native_vlan)
    if port.trunk_vlans is not None and len(port.trunk_vlans) < 4096 :
        data.append(" switchport trunk allowed vlan %s" % to_vlan_ranges(port.trunk_vlans))
    if port.mode:
        data.append(" switchport mode %s" % port.mode)
    if port.shutdown:
        data.append(" shutdown")
    if port.aggregation_membership:
        data.append(" channel-group %s mode active" % last_number(port.aggregation_membership))
    if port.vrf:
        data.append(" ip vrf forwarding %s" % port.vrf.name)
    if port.ntp is False:
        data.append(" ntp disable")
    return data
