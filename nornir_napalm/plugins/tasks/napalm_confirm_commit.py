from typing import Optional
from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_confirm_commit(task: Task, dry_run: Optional[bool] = None) -> Result:
    """
    Confirm a commit that has a "pending" commit via the revert_in argument to
    napalm_config.

    Arguments:
        dry_run: whether to confirm_commit or not
    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    changed = False
    result = ""

    # Check for a pending commit
    has_pending = device.has_pending_commit()

    # Nothing to do:
    if not has_pending:
        result = "There are no pending commits. No action taken."
        return Result(host=task.host, result=result, changed=changed)

    dry_run = task.is_dry_run(dry_run)
    if not dry_run:
        changed = True
        device.confirm_commit()
        result = "Commit confirm completed"

    return Result(host=task.host, result=result, changed=changed)
