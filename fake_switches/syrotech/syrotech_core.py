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
    def new_command_processor(self):
        return EnabledCommandProcessor(
            config=ConfigCommandProcessor(
                config_interface=ConfigInterfaceCommandProcessor()
            )
        )


SyrotechOLTCore = SyrotechGPONOLTCore  # Backward compatibility


class SyrotechShellSession(ShellSession):
    def handle_unknown_command(self, line):
        self.command_processor.terminal_controller.write("No such command : %s\n" % line)


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
               

gpon_onus_list = [
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