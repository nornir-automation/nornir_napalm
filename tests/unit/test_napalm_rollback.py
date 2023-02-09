import os

from nornir_napalm.plugins.tasks import napalm_rollback
from nornir_napalm.plugins.connections import CONNECTION_NAME

THIS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/mocked/napalm_rollback"


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
    def test_napalm_rollback_commit(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_rollback_commit"}
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras=opt)
        result = d.run(napalm_rollback, dry=False)
        assert result
        for h, r in result.items():
            # Need to figure out what if a diff is returned
            assert r.changed

    def test_napalm_rollback_dry_run(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_rollback_dry_run"}
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras=opt)
        result = d.run(napalm_rollback, dry=True)
        assert result
        for h, r in result.items():
            # Need to figure out what if a diff is returned
            assert not r.changed
