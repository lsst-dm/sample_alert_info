# Kafka Integration Endpoint Examples #

This directory has a bunch of code examples showing how you can connect to the alert stream's integration endpoint.
There are a lot of ways to connect to Kafka, both in Python and more generally.
There are examples in here that show how to connect using several of those methods.

The [`confluent_kafka_consumer`](./confluent_kafka_consumer) example shows how to connect using the [`confluent_kafka_python`](https://github.com/confluentinc/confluent-kafka-python) library.
This library has significant long-term support from Confluent, a company that sponsors most of the development work on Kafka.
However, it presents an API that is not very Pythonic, and can be tricky to use.

## Providing credentials

In general, these examples expect credentials to be provided as two environment variables, `KAFKA_USERNAME` and `KAFKA_PASSWORD`.
If you set those to correct values for the integration endpoint, you should be able to run the code examples as-is.
