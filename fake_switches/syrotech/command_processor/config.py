# Copyright 2015 Internap.
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

import re

from fake_switches.command_processing.base_command_processor import BaseCommandProcessor
from fake_switches.switch_configuration import VlanPort, AggregatedPort


class ConfigCommandProcessor(BaseCommandProcessor):
    interface_separator = ""

    def __init__(self, config_interface):
        super(ConfigCommandProcessor, self).__init__()
        self.config_interface_processor = config_interface

    def get_prompt(self):
        return f"{self.switch_configuration.name}(config)#"


    def do_exit(self):
        self.is_done = True

    def show_unknown_interface_error_message(self):
        self.write_line("              ^")
        self.write_line("% Invalid input detected at '^' marker (not such interface)")
        self.write_line("")

    def do_show(self, *args):
        if "onu info".startswith(args[0]):
            self.show_onu_info()
        else:
            self.write_line("                               ^")
            self.write_line("% Invalid input detected at '^' marker.")
        self.write_line("")
        return
    
    def show_onu_info(self):
        all_data = self.switch_configuration.onu_list
        self.write_line("Onuindex   Model                Profile                Mode    AuthInfo ")
        self.write_line("---------------------------------------------------------------------------------------------")
        for l in all_data:
            self.write_line(l)
            self.write_line("")

    def do_interface(self, *args):
        interface_name = self.interface_separator.join(args)
        for p in self.switch_configuration.ports:
            print("Port: ", p.name)
            
        port = self.switch_configuration.get_port_by_partial_name(interface_name)
        if port:
            self.move_to(self.config_interface_processor, port)
        else:
            m = re.match("vlan{separator}(\d+)".format(separator=self.interface_separator), interface_name.lower())
            if m:
                vlan_id = int(m.groups()[0])
                new_vlan_interface = self.make_vlan_port(vlan_id, interface_name)
                self.switch_configuration.add_port(new_vlan_interface)
                self.move_to(self.config_interface_processor, new_vlan_interface)
            elif interface_name.lower().startswith('port-channel'):
                new_int = self.make_aggregated_port(interface_name)
                self.switch_configuration.add_port(new_int)
                self.move_to(self.config_interface_processor, new_int)
            else:
                self.show_unknown_interface_error_message()