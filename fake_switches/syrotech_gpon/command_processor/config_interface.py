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

from netaddr import IPNetwork
from netaddr.ip import IPAddress

from fake_switches.command_processing.base_command_processor import BaseCommandProcessor
from fake_switches.switch_configuration import VlanPort

from fake_switches.utils.ip_validator import (
    InvalidIpError,
    IncompleteIpError,
    valid_ip_v4,
)


class ConfigInterfaceCommandProcessor(BaseCommandProcessor):
    def init(
        self, switch_configuration, terminal_controller, logger, piping_processor, *args
    ):
        super(ConfigInterfaceCommandProcessor, self).init(
            switch_configuration, terminal_controller, logger, piping_processor
        )
        self.description_strip_chars = '"'
        self.port = args[0]

    def get_prompt(self):
        return f"{self.switch_configuration.name}(config-if)#"

    def do_description(self, *args):
        self.port.description = " ".join(args).strip(self.description_strip_chars)

    def do_no_description(self, *_):
        self.port.description = None

    def do_shutdown(self, *_):
        self.port.shutdown = True

    def do_no_shutdown(self, *_):
        self.port.shutdown = False

    def do_exit(self):
        self.is_done = True

    def do_no_onu(self, cmd: str, *args) -> None:
        self.write_line(f"{self.port.name}:{cmd}")

        # for l in self.switch_configuration.onu_list:
        #     print(l)
        # onu_id = f"{self.port.name}:{cmd}"
        # print("ONU ID FULL ======>", onu_id)
        # onu_found = None
        # for onu in self.switch_configuration.onu_list:
        #     if onu_id in onu:
        #         onu_found = onu
        #         break
        # if onu_found:
        #     self.switch_configuration.onu_list.remove(onu_found)
        #     self.write_line(f"ONU {onu_id} removed")
        # else:
        #     self.write_line(f"ONU {onu_id} not found")
        # for l in self.switch_configuration.onu_list:
        #     print(l)
        self.write_line("")
