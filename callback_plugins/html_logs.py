# Adapted from https://github.com/ansible/ansible/blob/devel/plugins/callbacks/log_plays.py
# And https://gist.github.com/cliffano/9868180

import os
import time
import json
from json import JSONEncoder
from datetime import datetime

datenow = datetime.now()
datenow = datenow.strftime('%Y-%m-%d-%h-%m-%s')
report_dir = "./report/"

FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout', 'stderr']

report = {
    "project": {"name": "RDHI"},
    "environment": {"values": ["Execution Date/Time: 2014-12-04-17:39:05", "Execution Environment: ST",
                               "TestMachine: harikrishna-ThinkPad-T410",
                               "Results: results/archieve/rdhi_20141204-173905"]},
    "signOffSuccessThreshold": 80,
    "signOffCommentsNegative": "Build Rejected. Build is not stable and Passed Test cases count is less than Accptable number/percentage",
    "signOffCommentsPositive": "Build Accepted",
    "features": [
        {
            "name": "RDHI Tests",
            "description": "@TODO.",
            "tags": ["Regression"],
            "scenarios": [
                {
                    "name": "tc_user_launchrequest",
                    "description": "Usecase type: tc_user_launchrequest",
                    "tags": ["Smoke", ""],
                    "status": "Passed",
                    "automated": True,
                    "cases":
                        [{
                             "name": "custom_LQ_noPrilim_888",
                             "status": "Passed"
                         },
                         {
                             "name": "custom_LQ_noPrilim_000",
                             "status": "Failed"
                         }
                        ]
                }
            ]
        }
    ]
}


def record_step(res, host, status):
    if type(res) == type(dict()):
        if "cmd" in res.keys():
            step = {"name": res["cmd"], "status": status, "scenario": os.getenv('scenario')}
            report["features"][0]["scenarios"][0]["cases"].append(step)
            print(JSONEncoder().encode(report))


def write_report():
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    filnename = (report_dir + '/' + datenow + ".html")
    path = os.path.join(filnename)
    reportFile = open(path, "a")
    reportFile.write(JSONEncoder().encode(report))
    reportFile.close()


class CallbackModule(object):
    """
      logs playbook results, per host, as a basic html file in /var/log/ansible/hosts/html/
    """
    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        record_step(res, host, "Failed")

    def runner_on_ok(self, host, res):
        record_step(res, host, "Passed")

    def runner_on_error(self, host, msg):
        record_step(res, host, "Failed")
        pass

    def runner_on_skipped(self, host, item=None):
        record_step(res, host, "Skipped")
        pass

    def runner_on_unreachable(self, host, res):
        record_step(res, host, "Failed")

    def runner_on_no_hosts(self):
        record_step(res, host, "Skipped")
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        record_step(res, host, "Passed")

    def runner_on_async_ok(self, host, res, jid):
        record_step(res, host, "Passed")

    def runner_on_async_failed(self, host, res, jid):
        record_step(res, host, "Failed")

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None,
                                salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass

    def playbook_on_play_start(self, pattern):
        pass

    def playbook_on_stats(self, stats):
        write_report()
