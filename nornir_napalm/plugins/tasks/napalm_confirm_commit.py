from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_confirm_commit(task: Task, dry_run: bool | None = None) -> Result:
    """Confirm a commit the device is holding as pending.

    Makes permanent a commit made by :obj:`napalm_configure` with ``revert_in`` set.
    Without this the device reverts on its own once the timer runs out, which is what
    stops a change that cuts off your access to the device from becoming permanent. Run
    it once you have checked that the device is still reachable and behaving.

    Whether a commit is pending is state the device holds, not the connection, so this
    works from a later nornir run and does not have to share a session with the
    :obj:`napalm_configure` that made the commit.

    A host with nothing pending is left alone and reported as unchanged, so this is safe
    to point at a whole inventory when only some of it has a commit waiting.

    Arguments:
        task: Task nornir supplies when it runs this, not something you pass yourself
        dry_run: Report what would happen without confirming anything. Left out, the
            ``dry_run`` of the nornir object decides

    Returns:
        Result object with these attributes set

        * result (``str``): ``"Commit confirm completed"`` when a commit was confirmed, a
          note that nothing was pending when there was nothing to do, and empty on a dry
          run
        * changed (``bool``): whether a commit was confirmed

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
