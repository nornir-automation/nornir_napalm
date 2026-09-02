from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_rollback(task: Task, dry_run: bool | None = None) -> Result:
    """Revert the last commit on the device.

    This is napalm's ``rollback``, which undoes the most recent commit rather than
    stepping back through a history of them, and how far back that reaches is up to the
    platform. Run it twice and you do not get two commits back.

    On a device with a commit confirm pending, from :obj:`napalm_configure` with
    ``revert_in`` set, this cancels the pending commit and reverts straight away instead
    of waiting for the timer to run out.

    Arguments:
        task: Task nornir supplies when it runs this, not something you pass yourself
        dry_run: Report what would happen without rolling anything back. Left out, the
            ``dry_run`` of the nornir object decides

    Returns:
        Result object with these attributes set

        * result (``str``): ``"Rollback completed"``, or empty on a dry run
        * changed (``bool``): whether the rollback was run. It says nothing about whether
          the device had anything to revert, only that it was asked to

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
