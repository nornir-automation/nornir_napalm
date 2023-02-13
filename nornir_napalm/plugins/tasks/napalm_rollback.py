from typing import Optional
from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_rollback(task: Task, dry_run: Optional[bool] = None) -> Result:
    """
    Rollback device configuration using napalm
    Arguments:
        dry_run: whether to rollback the configuration or not
    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    changed = False
    result = ""

    dry_run = task.is_dry_run(dry_run)
    if not dry_run:
        changed = True
        device.rollback()
        result = "Rollback completed"
    return Result(host=task.host, result=result, changed=changed)
