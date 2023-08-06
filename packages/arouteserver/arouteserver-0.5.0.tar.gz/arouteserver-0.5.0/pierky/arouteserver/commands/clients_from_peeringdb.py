# Copyright (C) 2017 Pier Carlo Chiodi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys
import yaml

from .base import ARouteServerCommand
from ..config.program import program_config
from ..peering_db import clients_from_peeringdb

class ClientsFromPeeringDBCommand(ARouteServerCommand):

    COMMAND_NAME = "clients-from-peeringdb"
    COMMAND_HELP = ("Build a list of clients and their AS-SET on the basis "
                    "of PeeringDB records.")
    NEEDS_CONFIG = True

    @classmethod
    def add_arguments(cls, parser):
        super(ClientsFromPeeringDBCommand, cls).add_arguments(parser)

        parser.add_argument(
            "-o", "--output",
            type=argparse.FileType('w'),
            help="Output file. Default: stdout.",
            default=sys.stdout,
            dest="output_file")

        parser.add_argument(
            "netixlanid",
            type=int,
            help="PeeringDB NetIX LAN ID.")

    def run(self):
        data = clients_from_peeringdb(
            self.args.netixlanid,
            program_config.get("cache_dir")
        )
        yaml.safe_dump(data, self.args.output_file, default_flow_style=False)

        return True
