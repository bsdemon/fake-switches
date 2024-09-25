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
from fake_switches.syrotech_epon.command_processor.config import ConfigCommandProcessor
from fake_switches.syrotech_epon.command_processor.config_interface import (
    ConfigInterfaceCommandProcessor,
)
from fake_switches.syrotech_epon.command_processor.default import (
    DefaultCommandProcessor,
)
from fake_switches.syrotech_epon.command_processor.enabled import (
    EnabledCommandProcessor,
)
from fake_switches.syrotech_epon.command_processor.piping import PipingProcessor
from fake_switches.syrotech_epon.command_processor.debug import DebugCommandProcessor
from fake_switches.command_processing.shell_session import ShellSession
from fake_switches.switch_configuration import Port
from fake_switches.terminal import LoggingTerminalController


class BaseSyrotechEPONOLTCore(switch_core.SwitchCore):
    def __init__(self, switch_configuration):
        super(BaseSyrotechEPONOLTCore, self).__init__(switch_configuration)
        self.switch_configuration.add_vlan(self.switch_configuration.new("Vlan", 1))
        self.switch_configuration.onu_list = epon_onus_list
        self.logger = None
        self.last_connection_id = 0
        self.switch_configuration.name = "syrotech-epon"

    def launch(self, protocol, terminal_controller):
        self.last_connection_id += 1

        self.logger = logging.getLogger(
            "fake_switches.Syrotech.%s.%s.%s"
            % (self.switch_configuration.name, self.last_connection_id, protocol)
        )

        processor = self.new_command_processor()
        if not self.switch_configuration.auto_enabled:
            processor = DefaultCommandProcessor(processor)

        processor.init(
            self.switch_configuration,
            LoggingTerminalController(self.logger, terminal_controller),
            self.logger,
            PipingProcessor(self.logger),
        )
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
            Port("EPON0/1"),
            Port("EPON0/2"),
            Port("EPON0/3"),
            Port("EPON0/4"),
        ]


class SyrotechEPONOLTCore(BaseSyrotechEPONOLTCore):
    def __init__(self, switch_configuration):
        super(SyrotechEPONOLTCore, self).__init__(switch_configuration)
        self.switch_configuration.add_vlan(self.switch_configuration.new("Vlan", 1))
        self.switch_configuration.onu_list = epon_onus_list
        self.logger = None
        self.last_connection_id = 0
        self.switch_configuration.name = "syrotech-epon"
        # self.reboot_console = self.new_command_processor()

    def new_command_processor(self):
        return EnabledCommandProcessor(
            config=ConfigCommandProcessor(
                config_interface=ConfigInterfaceCommandProcessor(),
                debug=DebugCommandProcessor(),
            )
        )


class SyrotechShellSession(ShellSession):
    def handle_unknown_command(self, line):
        self.command_processor.terminal_controller.write("% Unknown command. \n")


class Syrotech_EPON_OLT_Core(SyrotechEPONOLTCore):
    @staticmethod
    def get_default_ports():
        return (
            [Port("FastEthernet0/{0}".format(p + 1)) for p in range(24)]
            + [Port("GigabitEthernet0/{0}".format(p + 1)) for p in range(2)]
            + [Port("EPON0/{0}".format(p + 1)) for p in range(2)]
        )


epon_onus_list = [
    "EPON0/1:1   offline   08:63:32:64:85:2b    33           116     2024/08/08 11:01:35     2024/08/08 11:04:21     Wire Down         00:02:47     N/A",
    "EPON0/1:2   offline   b4:f9:49:bc:09:98    23           110     2024/07/29 15:32:32     2024/07/30 17:04:23     Wire Down         1 01:31:52   N/A",
    "EPON0/1:3   offline   bc:62:d2:31:18:8c    6            76      2024/07/26 16:53:43     2024/07/29 13:59:11     Wire Down         2 21:05:27   N/A",
    "EPON0/1:26  offline   b4:3d:08:8e:3d:98    24           111     2024/08/07 14:53:40     2024/08/07 14:54:53     Wire Down         00:01:13     N/A",
]
