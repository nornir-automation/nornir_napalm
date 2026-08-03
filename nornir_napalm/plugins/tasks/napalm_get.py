import copy
from typing import Any

from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME

GetterOptionsDict = dict[str, dict[str, Any]] | None


def napalm_get(
    task: Task, getters: list[str], getters_options: GetterOptionsDict = None, **kwargs: Any
) -> Result:
    """
    Gather information from network devices using napalm

    Arguments:
        getters: getters to use
        getters_options (dict of dicts): When passing multiple getters you
            pass a dictionary where the outer key is the getter name
            and the included dictionary represents the options to pass
            to the getter
        **kwargs: will be passed as they are to the getters

    Returns:
        Result object with the following attributes set:
          * result (``dict``): dictionary with the result of the getter
    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    getters_options = getters_options or {}

    if isinstance(getters, str):
        getters = [getters]

    result = {}
    for g in getters:
        options = copy.deepcopy(kwargs)
        options.update(getters_options.get(g, {}))
        getter = g if g.startswith("get_") else f"get_{g}"
        method = getattr(device, getter)
        result[g] = method(**options)
    return Result(host=task.host, result=result)
