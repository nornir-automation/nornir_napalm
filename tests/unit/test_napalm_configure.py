import os

from napalm.base import exceptions

from nornir_napalm.plugins.tasks import napalm_configure
from nornir_napalm.plugins.connections import CONNECTION_NAME


THIS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/mocked/napalm_configure"


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
    def test_napalm_configure_change_dry_run(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_dry_run"}
        configuration = "hostname changed-hostname"
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras=opt)
        result = d.run(napalm_configure, dry_run=True, configuration=configuration)
        assert result
        for h, r in result.items():
            assert "+hostname changed-hostname" in r.diff
            assert r.changed

    def test_napalm_configure_change_commit(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_commit/step1"}
        configuration = "hostname changed-hostname"
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras=opt)
        result = d.run(napalm_configure, dry_run=False, configuration=configuration)
        assert result
        for h, r in result.items():
            assert "+hostname changed-hostname" in r.diff
            assert r.changed
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_commit/step2"}
        d.run(connect, extras=opt)
        result = d.run(napalm_configure, dry_run=True, configuration=configuration)
        assert result
        for h, r in result.items():
            assert "+hostname changed-hostname" not in r.diff
            assert not r.changed

    def test_napalm_configure_change_error(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_error"}
        configuration = "hostname changed_hostname"

        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras=opt)
        results = d.run(napalm_configure, configuration=configuration)
        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, exceptions.MergeConfigException)
        assert processed
