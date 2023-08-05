# Logging Microservice

This is a logging microservice from Pip.Services library. 
It collects execution logs from distributed microservices, stores 
and provides a single entry point to read all of them.

The microservice currently supports the following deployment options:
* Deployment platforms: Standalone Process, Seneca Plugin
* External APIs: HTTP/REST, Seneca
* Persistence: Memory

This microservice has no dependencies on other microservices.

<a name="links"></a> Quick Links:

* [Download Links](doc/Downloads.md)
* [Development Guide](doc/Development.md)
* [Configuration Guide](doc/Configuration.md)
* [Deployment Guide](doc/Deployment.md)
* Implementations in other languages
  - [Node.js](https://github.com/pip-services-infrastructure/pip-services-logging-node)
* Client SDKs
  - [Node.js SDK](https://github.com/pip-services/pip-clients-logging-node)
  - [Python SDK](https://github.com/pip-services/pip-clients-logging-python)
* Communication Protocols
  - [HTTP Version 1](doc/HttpProtocolV1.md)

## Download

Right now the only way to get the microservice is to check it out directly from github repository
```bash
git clone git@github.com:pip-services-infrastructure/pip-services-logging-python.git
```

Pip.Service team is working to implement packaging and make stable releases available for your 
as zip downloadable archieves.

## Run

Add **config.yaml** file to the root of the microservice folder and set configuration parameters.
As the starting point you can use example configuration from **config.example.yaml** file. 

Example of microservice configuration
```yaml
- descriptor: "pip-services-container:container-info:default:default:1.0"
  name: "pip-services-logging"
  description: "Logging microservice"

- descriptor: "pip-services-commons:logger:console:default:1.0"
  level: "trace"

- descriptor: "pip-services-logging:persistence:memory:default:1.0"

- descriptor: "pip-services-logging:controller:default:default:1.0"

- descriptor: "pip-services-logging:service:http:default:1.0"
  connection:
    protocol: "http"
    host: "0.0.0.0"
    port: 3000
```
 
For more information on the microservice configuration see [Configuration Guide](Configuration.md).

Start the microservice using the command:
```bash
node run
```

## Use

The easiest way to work with the microservice is to use client SDK. 
The complete list of available client SDKs for different languages is listed in the [Quick Links](#links)

If you use Python then you should add dependency to the client SDK into **requirements.txt** file of your project
```text
pip_clients_logging_node>=1.0
```

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

This microservice was created and currently maintained by *Sergey Seroukhov*.

