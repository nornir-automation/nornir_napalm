import os

from nornir_napalm.plugins.tasks import napalm_confirm_commit
from nornir_napalm.plugins.connections import CONNECTION_NAME

THIS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/mocked/napalm_confirm_commit"


def connect(task, extras):
    if CONNECTION_NAME in task.host.connections:
        task.host.close_connection(CONNECTION_NAME)
    task.host.open_connection(
        CONNECTION_NAME,
        task.nornir.config,
        extras={"optional_args": extras},
        default_to_host_attributes=True,
    )


def set_pending_commit(task):
    """Create an artificial pending commit."""
    conn = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    conn._pending_commits = True


class Test(object):
    def test_napalm_confirm_commit_no_pending(self, nornir):
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras={})
        result = d.run(napalm_confirm_commit, dry_run=False)

        assert result
        # NAPALM mock driver reports no-pending commits (by default)
        for h, r in result.items():
            assert r.changed is False
            assert "no pending commits" in r.result

    def test_napalm_confirm_commit_pending(self, nornir):
        opt = {"path": f"{THIS_DIR}/test_napalm_confirm_commit"}
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras=opt)
        d.run(set_pending_commit)
        result = d.run(napalm_confirm_commit, dry_run=False)

        assert result
        for h, r in result.items():
            assert r.changed is True
            assert r.result == "Commit confirm completed"

    def test_napalm_confirm_commit_pending_dry_run(self, nornir):
        opt = {"path": f"{THIS_DIR}/test_napalm_confirm_commit"}
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, extras=opt)
        d.run(set_pending_commit)
        result = d.run(napalm_confirm_commit, dry_run=True)

        assert result
        for h, r in result.items():
            assert r.changed is False
            assert r.result == ""
