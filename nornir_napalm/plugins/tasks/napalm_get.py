import copy
from typing import Any

from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME

GetterOptionsDict = dict[str, dict[str, Any]] | None


def napalm_get(
    task: Task, getters: list[str], getters_options: GetterOptionsDict = None, **kwargs: Any
) -> Result:
    """Gather structured data from the device with napalm getters.

    Getter names work with or without the ``get_`` prefix, so ``facts`` and
    ``get_facts`` both call ``get_facts``. The spelling you use is the key you get back
    and the key you have to use in ``getters_options``, so stay consistent between the
    two.

    Everything in ``kwargs`` is sent to every getter, which only works when all of them
    accept it. Use ``getters_options`` to reach a single getter. Where both apply to the
    same getter, ``getters_options`` wins.

    The getters run one after the other over the same connection, and one that raises
    fails the host and takes the data the earlier getters already returned with it. That
    is what a driver does for a getter it does not implement, so ask for the getters you
    are unsure about in a run of their own if losing everything to one unsupported
    getter would hurt.

    Arguments:
        task: Task nornir supplies when it runs this, not something you pass yourself
        getters: Getters to call, for instance ``["facts", "interfaces"]``
        getters_options: Options for individual getters, keyed by getter name, such as
            ``{"config": {"retrieve": "candidate"}}``
        **kwargs: Options sent to every getter

    Returns:
        Result object with these attributes set

        * result (``dict``): what each getter returned, keyed by getter name

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
