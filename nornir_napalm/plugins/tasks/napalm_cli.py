from typing import List

from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_cli(task: Task, commands: List[str], encoding: 'text') -> Result:
    """
    Run commands on remote devices using napalm

    Arguments:
      commands: commands to execute

    Returns:
      Result object with the following attributes set:
        * result (``dict``): result of the commands execution
    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    if task.host.platform == 'eos':
      result = device.cli(commands, encoding=encoding)
    else:
      result = device.cli(command)
    return Result(host=task.host, result=result)
