from nornir.core.task import Result, Task

from nornir_napalm.plugins.connections import CONNECTION_NAME


def napalm_ping(
    task: Task,
    dest: str,
    source: str | None = "",
    ttl: int | None = 255,
    timeout: int | None = 2,
    size: int | None = 100,
    count: int | None = 5,
    vrf: str | None = None,
) -> Result:
    """
    Executes ping on the device and returns a dictionary with the result.

    Arguments:
      dest(str) – Host or IP Address of the destination.
      source(str, optional) – Source address of echo request.
      ttl(int, optional) – Max number of hops.
      timeout(int, optional) – Max seconds to wait after sending final packet.
      size(int, optional) – Size of request in bytes.
      count(int, optional) – Number of ping request to send.
      vrf(str, optional) - Name of vrf.

    Returns:
       Result object with the following attributes set:
       * result (``dict``): list of dictionary with the result of the ping response.
         Output dictionary has one of following keys "success or error"


    """
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    result = device.ping(
        destination=dest,
        source=source,
        ttl=ttl,
        timeout=timeout,
        size=size,
        count=count,
        vrf=vrf,
    )
    return Result(host=task.host, result=result)
