from typing import Any

from nornir.core.task import Result, Task
from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_configure(
    task: Task,
    dry_run: bool | None = None,
    filename: str | None = None,
    configuration: str | None = None,
    replace: bool = False,
    commit_message: str | None = None,
    revert_in: int | None = None,
) -> Result:
    """Load a configuration onto the device and commit it.

    The configuration goes into the candidate of the device, which is then compared
    against the running configuration. The commit only happens if there is something to
    commit and the run is not a dry run; otherwise the candidate is discarded and the
    device is left exactly as it was.

    Pass the configuration either as ``filename`` or as ``configuration``. If you pass
    both, napalm uses the file and ignores the string. ``filename`` is read on the
    machine running nornir, not on the device.

    Arguments:
        task: Task nornir supplies when it runs this, not something you pass yourself
        dry_run: Load and diff the configuration without committing it. Left out, the
            ``dry_run`` of the nornir object decides
        filename: Path to a file holding the configuration to load
        configuration: The configuration to load, as a string
        replace: Replace the running configuration with what is loaded instead of merging
            into it. Merging is the default, so a partial configuration is normally safe
            to send
        commit_message: Message to record on the device alongside the commit. Only the
            drivers that support commit messages do anything with it
        revert_in: Seconds after which the device reverts the commit on its own unless
            :obj:`napalm_confirm_commit` confirms it first, which is what keeps a change
            that locks you out of the device from sticking. ``None`` commits normally.
            Only some drivers support this

    Returns:
        Result object with these attributes set

        * diff (``string``): the difference between the running configuration and the
          candidate. This is where the information is, no ``result`` is set
        * changed (``bool``): whether the loaded configuration differs from what the
          device is running. It describes the diff rather than the commit, so it is
          ``True`` on a dry run too

    Raises:
        napalm.base.exceptions.MergeConfigException: the device rejected the
            configuration while merging it
        napalm.base.exceptions.ReplaceConfigException: the device rejected the
            configuration while replacing with it

    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    if replace:
        device.load_replace_candidate(filename=filename, config=configuration)
    else:
        device.load_merge_candidate(filename=filename, config=configuration)
    diff = device.compare_config()

    dry_run = task.is_dry_run(dry_run)

    commit_kwargs: dict[str, Any] = {}
    if commit_message:
        commit_kwargs["message"] = commit_message
    if revert_in is not None:
        commit_kwargs["revert_in"] = revert_in

    if not dry_run and diff:
        device.commit_config(**commit_kwargs)
    else:
        device.discard_config()
    return Result(host=task.host, diff=diff, changed=len(diff) > 0)
