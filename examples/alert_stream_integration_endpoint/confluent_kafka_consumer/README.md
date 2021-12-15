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
181071569181737647 57095.171263959775 150.1001782809847 2.7169616477660865
181071569181737648 57095.171263959775 150.1016101673232 2.7396671409521085
181071569181737649 57095.171263959775 150.10233444970808 2.779694853155934
181071676555920289 57095.171263959775 150.25669622877666 2.203518774971655
181071676555920290 57095.171263959775 150.25347480298743 2.2018941609899048
181071676555920291 57095.171263959775 150.25566636066236 2.2020840024871613
181071676555920292 57095.171263959775 150.25643451089186 2.114722489930065
181071676555920293 57095.171263959775 150.25867863575496 2.202416394243328
181071676555920295 57095.171263959775 150.26068589540674 2.0810654751297473
181071676555920296 57095.171263959775 150.26179023648695 2.193512987941067
181071676555920297 57095.171263959775 150.2619746889272 2.1774574036473866
181071676555920298 57095.171263959775 150.2630031777793 2.192676853270568
181071676555920299 57095.171263959775 150.2629011230388 2.1946775210700875
181071676555920300 57095.171263959775 150.2668659791142 2.1033047817421946
```

If you see something like this, then you have the wrong credentials:

```sh
-> % python confluent_kafka_consumer.py
%3|1639075337.563|FAIL|rdkafka#consumer-1| [thrd:sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap]: sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap: SASL authentication error: Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-512 (after 346ms in state AUTH_REQ)
waiting for messages...
%3|1639075338.321|FAIL|rdkafka#consumer-1| [thrd:sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap]: sasl_ssl://alert-stream-int.lsst.cloud:9094/bootstrap: SASL authentication error: Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-512 (after 347ms in state AUTH_REQ, 1 identical error(s) suppressed)
waiting for messages...
```
