# Logging Microservice Client SDK for Python

This is a Python client SDK for [pip-services-logging](https://github.com/pip-services-infrastructure/pip-services-logging-python) microservice.
It provides an easy to use abstraction over communication protocols:

* HTTP/REST client
* Direct client for monolythic deployments
* Null client to be used in testing

This client SDK also contains Direct, and HTTP loggers that allow to directly log into the microservice.

<a name="links"></a> Quick Links:

* [Development Guide](doc/Development.md)
* [API Version 1](doc/PythonClientApiV1.md)

## Install

If you use Python then you should add dependency to the client SDK into **requirements.txt** file of your project
```text
pip_clients_logging_node>=1.0
```


Then install the dependency using **pip** tool
```bash
# Install new dependencies
pip install -r requirements.txt
```

## Use

Inside your code get the reference to the client SDK
```python
import datetime
from pip_services_commons.log import LogLevel
from pip_services_commons.config import ConfigParams
from pip_services_commons.data import FilterParams, PagingParams
from pip_clients_logging_node.version1 import LoggingHttpClientV1, LoggingMessageV1
```

Define client configuration parameters that match configuration of the microservice external API
```python
# Client configuration
config = ConfigParams.from_tuples(
    "connection.protocol", "http",
    "connection.host", "localhost", 
    "connection.port", 8003
)
```

Instantiate the client and open connection to the microservice
```python
# Create the client instance
client = LoggingHttpClientV1(config)

# Connect to the microservice
try:
    client.open(None)

    # Work with the microservice
    ...
except Exception as ex:
    print('Connection to the microservice failed')
    print(ex)
```

Now the client is ready to perform operations
```python
# Log a message
message = client.write_message(
    None,
    LogMessageV1(LogLevel.Info, None, None, None, "Restarted server")
)
...
```

```python
# Remember: all dates shall be in utc
now = datetime.datetime.utcnow()

# Get the list system activities
page = client.read_messages(
    None,
    FilterParams.from_tuples(
        "from_time", datetime.datetime.utcnow() - datetime.timediff(days=1),
        "to_time": datetime.datetime.utcnow(),
        "search": "server"
    ),
    PagingParams(0, 10, True),
)
...
```

## Acknowledgements

This client SDK was created and currently maintained by *Sergey Seroukhov*.

