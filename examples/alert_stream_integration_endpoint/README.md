# Alert Stream Integration Endpoint Examples #

This directory has a bunch of code examples showing how you can connect to the alert stream's integration endpoint.
There are a lot of ways to connect to Kafka, both in Python and more generally.
There are examples in here that show how to connect using several of those methods.

The [`confluent_kafka_consumer`](./confluent_kafka_consumer) example shows how to connect using the [`confluent_kafka_python`](https://github.com/confluentinc/confluent-kafka-python) library.
This library has significant long-term support from Confluent, a company that sponsors most of the development work on Kafka.
However, it presents an API that is not very Pythonic, and can be tricky to use.

The [`aiokafka_consumer`](./aiokafka_consumer) example shows how to connect using the [`aiokafka`](https://aiokafka.readthedocs.io/en/stable/) library.
This library has a much more Pythonic API, but a smaller development effort behind it.
It also uses the Python `asyncio` framework which allows for concurrent execution within a Python process.
This can be useful for building high-performance streaming applications in pure Python, but it can be very confusing for newcomers.

The [`java_console_consumer`](./java_console_consumer) example shows how to connect using a command-line script that ships with Kafka which uses Java.
It illustrates the Java `.properties` you'd need to set to connect to the broker.
It also shows how you can connect with just Docker for a minimal test of connectivity.

## Providing credentials

In general, these examples expect credentials to be provided as two environment variables, `KAFKA_USERNAME` and `KAFKA_PASSWORD`.
If you set those to correct values for the integration endpoint, you should be able to run the code examples as-is.
