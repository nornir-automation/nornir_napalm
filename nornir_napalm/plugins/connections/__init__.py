"""Connection plugin that lets nornir hosts talk to devices through napalm."""

from typing import Any

from napalm import get_network_driver

from nornir.core.configuration import Config


CONNECTION_NAME = "napalm"


class Napalm:
    """Connect to a device with napalm and expose the napalm driver as the connection.

    The driver is picked from the ``platform`` of the host, so that has to be a napalm
    driver name such as ``ios``, ``eos``, ``junos`` or ``nxos``, and not one of the
    netmiko or scrapli spellings of the same platform.

    Whatever is in ``extras`` is passed to the napalm driver constructor as keyword
    arguments, which is how you reach the settings nornir has no host attribute for::

        connection_options:
          napalm:
            extras:
              timeout: 120
              optional_args:
                global_delay_factor: 2

    ``optional_args`` is napalm's own passthrough to the library underneath, netmiko for
    the drivers built on it, so per platform tuning goes in there rather than next to
    ``timeout``.
    """

    def open(
        self,
        hostname: str | None,
        username: str | None,
        password: str | None,
        port: int | None,
        platform: str | None,
        extras: dict[str, Any] | None = None,
        configuration: Config | None = None,
    ) -> None:
        """Connect to the device and store the napalm driver in ``self.connection``.

        Nornir calls this the first time a task asks a host for a napalm connection, so
        there is normally no reason to call it yourself. The arguments arrive already
        resolved by nornir from the attributes of the host, its groups, the defaults and
        the ``connection_options`` of the napalm connection.

        Two things are worth knowing about how those arguments reach napalm:

        * The napalm constructor takes no ``port``, so ``port`` is handed over inside
          ``optional_args``. A port set in ``extras["optional_args"]`` therefore wins
          over the port of the host.
        * ``extras`` is merged into the constructor arguments key by key, so supplying
          ``optional_args`` replaces the whole dictionary instead of adding to it. The
          ``ssh_config_file`` taken from ``config.ssh.config_file`` lives in there, so
          it is dropped as soon as you supply your own ``optional_args`` and has to be
          repeated if you want both.

        Arguments:
            hostname: Address to connect to
            username: Username to authenticate with
            password: Password to authenticate with
            port: Port to connect to, passed to napalm as ``optional_args["port"]``
            platform: Name of the napalm driver to use
            extras: Keyword arguments for the napalm driver constructor
            configuration: Nornir configuration, read for ``ssh.config_file``

        Raises:
            napalm.base.exceptions.ModuleImportError: no napalm driver goes by the name
                in ``platform``, or none is installed
            napalm.base.exceptions.ConnectionException: the device could not be reached
                or rejected the credentials

        """
        extras = extras or {}

        parameters: dict[str, Any] = {
            "hostname": hostname,
            "username": username,
            "password": password,
            "optional_args": {},
        }

        try:
            parameters["optional_args"]["ssh_config_file"] = configuration.ssh.config_file  # type: ignore
        except AttributeError:
            pass

        parameters.update(extras)

        if port and "port" not in parameters["optional_args"]:
            parameters["optional_args"]["port"] = port

        network_driver = get_network_driver(platform)
        connection = network_driver(**parameters)
        connection.open()
        self.connection = connection

    def close(self) -> None:
        """Close the session with the device.

        Nornir calls this for you when a host closes its connections, which includes
        using the nornir object as a context manager, so a script that goes through
        ``InitNornir`` does not have to close anything by hand.
        """
        self.connection.close()
