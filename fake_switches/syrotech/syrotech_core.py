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

import logging

from fake_switches import switch_core
from fake_switches.syrotech.command_processor.config import ConfigCommandProcessor
from fake_switches.syrotech.command_processor.config_interface import ConfigInterfaceCommandProcessor
from fake_switches.syrotech.command_processor.default import DefaultCommandProcessor
from fake_switches.syrotech.command_processor.enabled import EnabledCommandProcessor
from fake_switches.syrotech.command_processor.piping import PipingProcessor
from fake_switches.syrotech.command_processor.debug import DebugCommandProcessor
from fake_switches.command_processing.shell_session import ShellSession
from fake_switches.switch_configuration import Port
from fake_switches.terminal import LoggingTerminalController


class BaseSyrotechOLTCore(switch_core.SwitchCore):
    def __init__(self, switch_configuration):
        super(BaseSyrotechOLTCore, self).__init__(switch_configuration)
        self.switch_configuration.add_vlan(self.switch_configuration.new("Vlan", 1))
        self.switch_configuration.onu_list = gpon_onus_list
        self.logger = None
        self.last_connection_id = 0
        self.switch_configuration.name = "syrotech"

    def launch(self, protocol, terminal_controller):
        self.last_connection_id += 1

        self.logger = logging.getLogger(
            "fake_switches.Syrotech.%s.%s.%s" % (self.switch_configuration.name, self.last_connection_id, protocol))

        processor = self.new_command_processor()
        if not self.switch_configuration.auto_enabled:
            processor = DefaultCommandProcessor(processor)

        processor.init(
            self.switch_configuration,
            LoggingTerminalController(self.logger, terminal_controller),
            self.logger,
            PipingProcessor(self.logger))
        return SyrotechShellSession(processor)

    def new_command_processor(self):
        raise NotImplementedError

    def get_netconf_protocol(self):
        return None

    @staticmethod
    def get_default_ports():
        return [
            Port("FastEthernet0/1"),
            Port("FastEthernet0/2"),
            Port("FastEthernet0/3"),
            Port("FastEthernet0/4"),
            Port("FastEthernet0/5"),
            Port("FastEthernet0/6"),
            Port("FastEthernet0/7"),
            Port("FastEthernet0/8"),
            Port("FastEthernet0/9"),
            Port("FastEthernet0/10"),
            Port("FastEthernet0/11"),
            Port("FastEthernet0/12"),
            Port("GPON0/1"),
            Port("GPON0/2"),
            Port("GPON0/3"),
            Port("GPON0/4"),
        ]


class SyrotechGPONOLTCore(BaseSyrotechOLTCore):
    def __init__(self, switch_configuration):
        super(SyrotechGPONOLTCore, self).__init__(switch_configuration)
        self.switch_configuration.add_vlan(self.switch_configuration.new("Vlan", 1))
        self.switch_configuration.onu_list = gpon_onus_list
        self.logger = None
        self.last_connection_id = 0
        self.switch_configuration.name = "syrotech-gpon"
        # self.reboot_console = self.new_command_processor()
    
    def new_command_processor(self):
        return EnabledCommandProcessor(
            config=ConfigCommandProcessor(
                config_interface=ConfigInterfaceCommandProcessor(),
                debug=DebugCommandProcessor()
            )
        )


SyrotechOLTCore = SyrotechGPONOLTCore  # Backward compatibility


class SyrotechShellSession(ShellSession):
    def handle_unknown_command(self, line):
        self.command_processor.terminal_controller.write("% Unknown command. \n")


class Syrotech_GPON_OLT_Core(SyrotechOLTCore):
    @staticmethod
    def get_default_ports():
        return [Port("FastEthernet0/{0}".format(p + 1)) for p in range(24)] + \
               [Port("GigabitEthernet0/{0}".format(p + 1)) for p in range(2)] + \
               [Port("GPON0/{0}".format(p + 1)) for p in range(2)]


class Syrotech_EPON_OLT_Core(SyrotechOLTCore):
    @staticmethod
    def get_default_ports():
        return [Port("FastEthernet0/{0}".format(p + 1)) for p in range(48)] + \
               [Port("GigabitEthernet0/{0}".format(p + 1)) for p in range(2)] + \
               [Port("EPON0/{0}".format(p + 1)) for p in range(2)]
               
# GPON0/1:1\n\x1b[11C2K05X\n\x1b[32Cdefault\n\x1b[55Csn\n\x1b[63CPPCT924A9747\n\n
gpon_onus_list = [
        "GPON0/1:1\n\x1b[11C2K05X\n\x1b[32Cdefault\n\x1b[55Csn\n\x1b[63CPPCT924A9747\n\n",
        "GPON0/1:3\n\x1b[11unknown\n\x1b[32Cdefault\n\x1b[55Csn\n\x1b[63CPPCT92467809\n\n"]