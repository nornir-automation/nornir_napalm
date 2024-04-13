from typing import Any, List

from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_cli(task: Task, commands: List[str], **kwargs: Any) -> Result:
    """
    Run commands on remote devices using napalm

    Arguments:
      commands: commands to execute
      **kwargs: placeholder for user added arguments
    Returns:
      Result object with the following attributes set:
        * result (``dict``): result of the commands execution
    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = device.cli(commands, **kwargs)
    return Result(host=task.host, result=result)
