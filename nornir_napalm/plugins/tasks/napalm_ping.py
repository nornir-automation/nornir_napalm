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
    """Ping a destination from the device.

    The ping runs on the device itself, so ``dest`` has to be reachable from there and
    what comes back is the view the device has of the network, not the view of the
    machine running nornir. That is the point of the task: it tells you whether the
    device can reach something, which is rarely the same question as whether you can.

    A ping that fails is not a failed task. The host succeeds either way and the result
    carries an ``error`` key instead of a ``success`` one, so check the keys of the
    result rather than ``result.failed``.

    Arguments:
        task: Task nornir supplies when it runs this, not something you pass yourself
        dest: Host or IP address to ping
        source: Address to send the echo requests from. Empty lets the device pick
        ttl: Maximum number of hops
        timeout: Seconds to wait after the last request was sent
        size: Size of each request, in bytes
        count: Number of requests to send
        vrf: VRF to send the requests from. ``None`` uses the routing table the device
            would reach for on its own

    Returns:
        Result object with these attributes set

        * result (``dict``): a single key dictionary, either ``error`` holding a message
          from the device, or ``success`` holding ``probes_sent``, ``packet_loss``,
          ``rtt_min``, ``rtt_max``, ``rtt_avg``, ``rtt_stddev`` and a ``results`` list
          of one ``ip_address`` and ``rtt`` pair per reply

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
