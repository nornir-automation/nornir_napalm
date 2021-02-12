from typing import Optional
from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_traceroute(
    task: Task,
    destination: str,
    source: Optional[str] = "",
    ttl: Optional[int] = 255,
    timeout: Optional[int] = 2,
    vrf: Optional[str] = None,
) -> Result:
    """
    Executes traceroute on the device and returns a dictionary with the result.

    Arguments:
      destination(str) – Host or IP Address of the destination.
      source(str, optional) – Source address of echo request.
      ttl(int, optional) – Max number of hops.
      timeout(int, optional) – Max seconds to wait after sending final packet.
      vrf(str, optional) - Name of vrf.

    Returns:
       Result object with the following attributes set:
       * result (``dict``): list of dictionary with the result of the traceroute response.
         Output dictionary has one of following keys "success or error"


    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = device.traceroute(
        destination=destination, source=source, ttl=ttl, timeout=timeout, vrf=vrf,
    )
    return Result(host=task.host, result=result)
