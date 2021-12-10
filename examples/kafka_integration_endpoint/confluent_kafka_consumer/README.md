# `confluent_kafka` Consumer Example

This has an extremely excessively commented script which demonstrates how you can connect to the Rubin alert stream using `confluent_kafka`.
You can run the script yourself, too.

To do so, first install the `confluent_kafka` Python package, including the `schemaregistry` and `avro` extra features.
You can do this with `pip` (probably inside a virtualenv):

```
pip install 'confluent_kafka[schemaregistry,avro]'
```

Next, you should be able to run the script.
You need to set two environment variables to get this to work, and then you can call it directly with 'python':

```sh
export KAFKA_USERNAME=rubin-communitybroker-int  # use your actual value!
export KAFKA_PASSWORD=<.....>  # here, too!
python confluent_kafka_consumer.py
```

You should see output something like this:

```
-> % python confluent_kafka_consumer.py
waiting for messages...
waiting for messages...
waiting for messages...
waiting for messages...
waiting for messages...
waiting for messages...
waiting for messages...
waiting for messages...
```

If you see something like this, then you have the wrong credentials:

```sh
-> % python confluent_kafka_consumer.py
%3|1639075337.563|FAIL|rdkafka#consumer-1| [thrd:sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap]: sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap: SASL authentication error: Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-512 (after 346ms in state AUTH_REQ)
waiting for messages...
%3|1639075338.321|FAIL|rdkafka#consumer-1| [thrd:sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap]: sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap: SASL authentication error: Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-512 (after 347ms in state AUTH_REQ, 1 identical error(s) suppressed)
waiting for messages...
```
