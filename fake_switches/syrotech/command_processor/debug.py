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


class DebugCommandProcessor(BaseCommandProcessor):
    interface_separator = ""

    def __init__(self):
        super(DebugCommandProcessor, self).__init__()

    def get_prompt(self):
        return f"{self.switch_configuration.name}(debug)# "


    def do_exit(self):
        self.is_done = True

    def show_unknown_command_error_message(self):
        self.write_line("% Unknown command")

    def do_upload_tftp_configuration(self, file, ip):
        self.write_line(f"Trying to upload {file} to server {ip}, please wait...")
        self.write_line("2024/09/04 12:58:16   Upload File Success      upload syro-g-test-telent.cfg success")
        self.write_line("")
    
    def do_download_tftp_configuration(self, file, ip):
        self.write_line(f"Trying to download configuration {file} from TFTP server {ip}")
        self.write_line("Flashing configuration...")
        self.write_line("")