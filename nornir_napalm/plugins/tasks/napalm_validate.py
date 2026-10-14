from typing import Any

from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME

ValidationSourceData = dict[str, dict[str, Any]] | None


def napalm_validate(
    task: Task,
    src: str | None = None,
    validation_source: ValidationSourceData = None,
) -> Result:
    """Check the state of the device against a set of expectations.

    The rules name napalm getters and the values those getters ought to return. Napalm
    calls each one and compares, so this is how you assert that a device is in the state
    you think it is in rather than reading getter output yourself. See
    https://napalm.readthedocs.io/en/latest/validate/index.html for how to write them.

    A device that does not comply is not a failed task. The host succeeds either way and
    the verdict is the ``complies`` key of the result, so a run that looks entirely
    green can still be sitting on a device that is out of compliance. Read ``complies``,
    and remember that getters the driver does not implement are skipped rather than
    counted as failures.

    Pass either ``src`` or ``validation_source``. If you pass both, the file wins.

    Arguments:
        task: Task nornir supplies when it runs this, not something you pass yourself
        src: Path to a YAML file holding the rules, read on the machine running nornir
        validation_source: The same rules as data instead of a file: a list of single
            entry mappings of getter name to the expected result, for instance
            ``[{"get_interfaces": {"Ethernet1": {"description": ""}}}]``

    Returns:
        Result object with these attributes set

        * result (``dict``): the compliance report. One entry per rule, keyed by getter
          name, plus ``complies`` (``bool``) saying whether every rule passed and
          ``skipped`` (``list``) naming the getters the driver does not implement

    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    r = device.compliance_report(validation_file=src, validation_source=validation_source)
    return Result(host=task.host, result=r)
