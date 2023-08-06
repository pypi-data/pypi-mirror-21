#!/usr/bin/env python3
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from bts.http_rpc import HTTPRPC
from btsbots.config import service_account
import json


class ProfileOP(object):
    def __init__(self, config):
        if "service_account" in config:
            self.service_account = config["service_account"]
        else:
            self.service_account = service_account
        self.account = config["account"]
        cli_wallet = config["cli_wallet"]
        self.password = cli_wallet["wallet_unlock"]
        if 'uri' in cli_wallet:
            uri = cli_wallet["uri"]
        else:
            uri = "http://%s:%s" % (cli_wallet["host"], cli_wallet["port"])
        self.rpc = HTTPRPC(uri)

    def wallet_transfer(self, trx):
        _from_account, _to_account, _amount, _asset, _memo = trx
        try:
            self.rpc.transfer(
                _from_account, _to_account,
                "%s" % _amount, _asset, _memo, True)
        except Exception:
            print("[failed] transfer: %s" % trx)
            return

    def update_profile(self, _profile):
        profile = json.dumps({"profile": _profile})
        trx = [
            self.account, self.service_account, 1, "BTS", profile]
        self.wallet_transfer(trx)
