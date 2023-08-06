# Usage

## `watchmaker` from the CLI

Once wathmaker is [installed](installation.md) and a [configuration file](configuration.md)
has been created (or you have decided to use the default configuration), using
watchmaker as a CLI utility is as simple as executing `watchmaker`. Below is
the output of `watchmaker --help`, showing the CLI options.

```shell
# watchmaker --help
usage: watchmaker [-h] [-v] [-c CONFIG_PATH] [-l LOG_LEVEL] [-d LOG_DIR] [-n]
                  [-s SALT_STATES] [--s3-source] [-A ADMIN_GROUPS]
                  [-a ADMIN_USERS] [-t COMPUTER_NAME] [-e ENVIRONMENT]
                  [-p OU_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -v, -V, --version     Print version info.
  -c CONFIG_PATH, --config CONFIG_PATH
                        Path or URL to the config.yaml file.
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Set the log level. Case-insensitive. Valid values
                        include: "critical", "error", "warning", "info", and
                        "debug".
  -d LOG_DIR, --log-dir LOG_DIR
                        Path to the directory where Watchmaker log files will
                        be saved.
  -n, --no-reboot       If this flag is not passed, Watchmaker will reboot the
                        system upon success. This flag suppresses that
                        behavior. Watchmaker suppresses the reboot
                        automatically if it encounters a failure.
  -s SALT_STATES, --salt-states SALT_STATES
                        Comma-separated string of salt states to apply. A
                        value of 'None' will not apply any salt states. A
                        value of 'Highstate' will apply the salt highstate.
  --s3-source           Use S3 utilities to retrieve content instead of http/s
                        utilities. Boto3 must be installed, and boto3
                        credentials must be configured that allow access to
                        the S3 bucket.
  -A ADMIN_GROUPS, --admin-groups ADMIN_GROUPS
                        Set a salt grain that specifies the domain groups that
                        should have root privileges on Linux or admin
                        privileges on Windows. Value must be a colon-separated
                        string. E.g. "group1:group2"
  -a ADMIN_USERS, --admin-users ADMIN_USERS
                        Set a salt grain that specifies the domain users that
                        should have root privileges on Linux or admin
                        privileges on Windows. Value must be a colon-separated
                        string. E.g. "user1:user2"
  -t COMPUTER_NAME, --computer-name COMPUTER_NAME
                        Set a salt grain that specifies the computername to
                        apply to the system.
  -e ENVIRONMENT, --env ENVIRONMENT
                        Set a salt grain that specifies the environment in
                        which the system is being built. E.g. dev, test, or
                        prod
  -p OU_PATH, --ou-path OU_PATH
                        Set a salt grain that specifies the full DN of the OU
                        where the computer account will be created when
                        joining a domain. E.g.
                        "OU=SuperCoolApp,DC=example,DC=com"
```

## `watchmaker` as EC2 userdata

Calling watchmaker via EC2 userdata is a variation on using it as a CLI
utility. The main difference is that you must account for installing watchmaker
first, as part of the userdata. Since the userdata syntax and dependency
installation differ a bit on Linux and Windows, we provide methods for each as
examples.

```eval_rst
.. note::

    The ``pip`` commands in the examples are a bit more complex than
    necessarily needed, depending on your use case. In these examples, we are
    taking into account differences in pip versions available to different
    platforms, as well as limitations in FIPS support in the default PyPi repo.
    This way the same ``pip`` command works for all platforms.
```

### Linux

For **Linux**, you must ensure `pip` is installed, and then you can install
`watchmaker` from PyPi. After that, run `watchmaker` using any option available
on the [CLI](#watchmaker-from-the-cli). Here is an example:

```shell
#!/bin/sh
PYPI_URL=https://pypi.org/simple

# Get the host
PYPI_HOST=$(echo $PYPI_URL |sed -e "s/[^/]*\/\/\([^@]*@\)\?\([^:/]*\).*/\2/")

# Install pip
yum -y --enablerepo=epel install python-pip

# Install watchmaker
pip install --index-url="$PYPI_URL" --trusted-host="$PYPI_HOST" --allow-all-external --upgrade pip setuptools watchmaker

# Run watchmaker
watchmaker --log-level debug --log-dir=/var/log/watchmaker
```

Alternatively, cloud-config directives can also be used on **Linux**:

```yaml
#cloud-config

runcmd:
  - |
    PYPI_URL=https://pypi.org/simple

    # Get the host
    PYPI_HOST=$(echo $PYPI_URL |sed -e "s/[^/]*\/\/\([^@]*@\)\?\([^:/]*\).*/\2/")

    # Install pip
    yum -y --enablerepo=epel install python-pip

    # Install watchmaker
    pip install --index-url="$PYPI_URL" --trusted-host="$PYPI_HOST" --allow-all-external --upgrade pip setuptools watchmaker

    # Run watchmaker
    watchmaker --log-level debug --log-dir=/var/log/watchmaker
```

### Windows

For **Windows**, the first step is to install Python. `Watchmaker` provides a
simple bootstrap script to do that for you. After installing Python, install
`watchmaker` using `pip` and then run it.

```shell
<powershell>
$BootstrapUrl = "https://raw.githubusercontent.com/plus3it/watchmaker/master/docs/files/bootstrap/watchmaker-bootstrap.ps1"
$PythonUrl = "https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe"
$PypiUrl = "https://pypi.org/simple"

# Get the host
$PypiHost="$(([System.Uri]$PypiUrl).Host)"

# Download bootstrap file
$BootstrapFile = "${Env:Temp}\$(${BootstrapUrl}.split('/')[-1])"
(New-Object System.Net.WebClient).DownloadFile("$BootstrapUrl", "$BootstrapFile")

# Install python
& "$BootstrapFile" -PythonUrl "$PythonUrl" -Verbose -ErrorAction Stop

# Install watchmaker
pip install --index-url="$PypiUrl" --trusted-host="$PypiHost" --upgrade pip setuptools watchmaker

# Run watchmaker
watchmaker --log-level debug --log-dir=C:\Watchmaker\Logs
</powershell>
```

## `watchmaker` as a CloudFormation template

Watchmaker can be integrated into a CloudFormation template as well. This
project provides a handful of CloudFormation templates that launch instances or
create autoscaling groups, and that install and execute Watchmaker during the
launch. These templates are intended as examples for you to modify and extend
as you need.

### Cloudformation templates

*   [Linux Autoscale Group][lx-autoscale]
*   [Linux Instance][lx-instance]
*   [Windows Autoscale Group][win-autoscale]
*   [Windows Instance][win-instance]

### Cloudformation parameter-maps

Sometimes it is helpful to define the parameters for a template in a file, and
pass those to CloudFormation along with the template. We call those "parameter
maps", and provide one for each of the templates above.

*   [Linux Autoscale Params][lx-autoscale-params]
*   [Linux Instance Params][lx-instance-params]
*   [Windows Autoscale Params][win-autoscale-params]
*   [Windows Instance Params][win-instance-params]

[lx-autoscale]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/templates/watchmaker-lx-autoscale.template
[lx-instance]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/templates/watchmaker-lx-instance.template
[win-autoscale]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/templates/watchmaker-win-autoscale.template
[win-instance]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/templates/watchmaker-win-instance.template

[lx-autoscale-params]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/parameter-maps/watchmaker-lx-autoscale.params.json
[lx-instance-params]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/parameter-maps/watchmaker-lx-instance.params.json
[win-autoscale-params]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/parameter-maps/watchmaker-win-autoscale.params.json
[win-instance-params]: https://github.com/plus3it/watchmaker/blob/develop/docs/files/cfn/parameter-maps/watchmaker-win-instance.params.json

## `watchmaker` as a library

Watchmaker can also be used as a library, as part of another python
application.

```python
import watchmaker

arguments = watchmaker.Arguments()
arguments.config_path = None
arguments.no_reboot = False
arguments.salt_states = 'None'
arguments.s3_source = False

client = watchhmaker.Client(arguments)
client.install()
```

```eval_rst
.. note::

    This demonstrates only a few of the arguments that are available for the
    ``watchmaker.Arguments()`` object. For details on all arguments, see the
    :any:`API Reference <api>`.
```
