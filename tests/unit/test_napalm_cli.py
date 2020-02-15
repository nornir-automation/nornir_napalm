import os

from nornir_napalm.tasks import napalm_cli
from nornir_napalm.connections import CONNECTION_NAME


THIS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/mocked/napalm_cli"


def connect(task, extras):
    if CONNECTION_NAME in task.host.connections:
        task.host.close_connection(CONNECTION_NAME)
    task.host.open_connection(
        CONNECTION_NAME,
        task.nornir.config,
        extras={"optional_args": extras},
        default_to_host_attributes=True,
    )


class Test(object):
    def test_napalm_cli(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_cli"}
        d = nornir.filter(name="dev3.group_2")
        r = d.run(connect, extras=opt)
        result = d.run(napalm_cli, commands=["show version", "show interfaces"])
        assert result
        for h, r in result.items():
            assert r.result["show version"]
            assert r.result["show interfaces"]
