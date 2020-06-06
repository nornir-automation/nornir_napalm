from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME

def napalm_rollback(task: Task, dry_run: bool = None) -> Result:
    """
    Rollback device configuration using napalm
    Arguments:
        dry_run: whether to rollback the configuration or not
    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    if not dry_run:
        device.rollback()

    return Result(host=task.host, result=result))
