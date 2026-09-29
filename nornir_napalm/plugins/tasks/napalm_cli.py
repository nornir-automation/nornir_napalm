from typing import Any

from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_cli(task: Task, commands: list[str], **kwargs: Any) -> Result:
    """Run commands on the device and collect their output.

    The commands are sent as they are and nothing is parsed on the way back, so what you
    get is the text the device printed. Reach for :obj:`napalm_get` instead when you want
    structured data, as parsing screen output tends to break on the next software
    upgrade.

    Whether a command the device rejects raises or has its error message handed back as
    the output of that command depends on the driver, so do not rely on a failed host to
    tell you that a command was wrong.

    Arguments:
        task: Task nornir supplies when it runs this, not something you pass yourself
        commands: Commands to run, in order
        **kwargs: Passed on to napalm's ``cli``. ``encoding="json"`` asks the drivers
            that support it for parsed output rather than text

    Returns:
        Result object with these attributes set

        * result (``dict``): the output of each command, keyed by the command exactly
          as it was given

    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = device.cli(commands, **kwargs)
    return Result(host=task.host, result=result)
