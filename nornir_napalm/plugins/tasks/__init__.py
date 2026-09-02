"""Tasks that drive napalm from nornir.

Every task in here is meant to be handed to ``nr.run``, which supplies the ``task``
argument and calls the function once per host::

    nr.run(task=napalm_get, getters=["facts"])

They all reach the device through the napalm connection of the host, opening it on first
use, so the platform of the host has to name a napalm driver.

The three that change the device, :obj:`napalm_configure`, :obj:`napalm_rollback` and
:obj:`napalm_confirm_commit`, honour dry runs. They take a ``dry_run`` argument and fall
back to the ``dry_run`` of the nornir object when it is left out, so a script started
with ``InitNornir(dry_run=True)`` reports what it would do and touches nothing.
"""

from .napalm_cli import napalm_cli
from .napalm_configure import napalm_configure
from .napalm_get import napalm_get
from .napalm_ping import napalm_ping
from .napalm_validate import napalm_validate
from .napalm_rollback import napalm_rollback
from .napalm_confirm_commit import napalm_confirm_commit

__all__ = (
    "napalm_cli",
    "napalm_configure",
    "napalm_get",
    "napalm_ping",
    "napalm_validate",
    "napalm_rollback",
    "napalm_confirm_commit",
)
