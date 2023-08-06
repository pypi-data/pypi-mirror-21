# headspin-cli
CLI for the HeadSpin platform API.

Installation/Upgrade:
--
```
pip install --upgrade headspin-cli
```

Usage:
--
```
CLI for the HeadSpin platform API

Usage:
  hs (-h | --help)
  hs auth init <token> [-v]
  hs auth ls
  hs auth set-default <credentials_number>
  hs session ls [<num_sessions>] [-a] [--json] [-v]
  hs session inspect <session_uuid> [--writefiles] [--json] [-v]
  hs session start network_container <device_id> [--json] [-v]
  hs session stop <session_uuid> [--json] [-v]
  hs session mar <session_uuid> [-v]
  hs session har <session_uuid> [-v]
  hs device ls [<selector>] [--json] [-v]
  hs device connect <selector> [--json]
  hs device disconnect <selector> [--json]
  hs device keys [--json]
  hs config add-adb-key [--path=<adb_key_path>] [--json]
  hs config server [<server>]
  hs config connect-method [(requests|curl)]
```

Detailed Description:
--
```
  Note: The --json flag dumps the raw JSON output as returned by the
  sever. The -v flag turns on verbose logging in the requests library,
  showing the HTTP requests and responses (headers-only).


  hs auth init <token>

        Authorizes this device given a one-time token <token>. Contact
        support@headspin.io to request an authorization token.

  hs auth ls

        Prints the current credentials.

  has auth set-default <credentials_number>

        Sets the credentials number <credentials_number> as the default.
        The numbering can be seen via the `hs auth info` command.

  hs session ls [<num_sessions>] [-a]

        Outputs a list of session metadata in reverse-chronological
        order. <num_sessions> is the number of sessions output, 5 by
        default. By default only active sessions are output. The `-a`
        flag will cause inactive sessions to be inclued in the result.

  hs session inspect <session_uuid> [--writefiles]

        Outputs details for a session given the session's UUID. If
        `--writefiles` is given, data associated with session endpoints
        is written to files.

  hs session start network_container <device_id>

        Starts a HeadSpin network container session on a device
        specified by <device_id>. The container's default network
        interface (eth0) is on the device's mobile network. The container
        can be accessed via SSH login. In addition, a device can access
        the remote mobile network by connecting to a VPN.

  hs session stop <session_uuid>

        Stops a session in progress.

  hs session mar <session_id>

        Downloads the captured network traffic from a HeadSpin session
        in HeadSpin's MAR format. MAR is a HAR-like JSON format that
        contains the data in a network capture at a high level.

  hs session har <session_id>

        Downloads the captured network traffic from a HeadSpin session
        in HAR format.

  hs device ls [<selector>]

        Lists all devices, optionally matching a selector.

  hs device connect <selector> [--json]

        Connect a remote device locally. For Android, an `adb connect`
        is performed. The first device that matches the selector is used.

  hs device disconnect <selector> [--json]

        Disconnect all devices matched by the selector.

  hs device keys [--json]

        List keys that can be used in a <selector>, as in
        `hs device connect <selector>` or `hs device disconnect <selector>`.

  hs config add-adb-key [--path=<adb_key_path>] [--json]

        Add an adb key to all remote control hosts. If a path is not
        specified, ~/.android/adbkey.pub is used.

  hs config server <server>

        Set the HeadSpin API server URL.

  hs config connect-method [(requests|curl)]

        Set the method by which requests are issued to the server. The
        "requests" method uses the python requests library. The "curl"
        method uses command-line curl.

```

Version History:
--

0.1
* Add device status to device listing.
* Add `device inspect`.

0.2
* Focus device listing on remote control devices.
* Add adb connect/disconnect/add-adb-keys functionality.
* Support switching between `requests` library and `curl`
  as the underlying method for speaking to the server.

0.3
* Introduce basic support for iOS devices
