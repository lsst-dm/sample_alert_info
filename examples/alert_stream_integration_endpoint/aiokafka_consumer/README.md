# `aiokafka` Consumer Example

This has an extremely excessively commented script which demonstrates how you can connect to the Rubin alert stream using `aiokafka`.
You can run the script yourself, too.

To do so, first install the dependencies: `aiokafka` and `python-schema-registry-client`.
You can do this with `pip` (probably inside a virtualenv):

```
pip install aiokafka python-schema-registry-client
```

Next, you should be able to run the script.
You need to set two environment variables to get this to work, and then you can call it directly with 'python':

```sh
export KAFKA_USERNAME=rubin-communitybroker-int  # use your actual value!
export KAFKA_PASSWORD=<.....>  # here, too!
python aiokafka_consumer.py
```

You should see output something like this:
```sh
-> % python aiokafka_consumer.py
waiting for messages...
181071633606247047 57095.171263959775 149.15438008865456 2.3102360904670896
181071633606247048 57095.171263959775 149.1556358638395 2.368153232932496
181071633606247049 57095.171263959775 149.15740682390484 2.3670021854244743
181071633606247050 57095.171263959775 149.1557694724021 2.3663503234901566
181071633606247051 57095.171263959775 149.16271153195876 2.3686177132399333
181071633606247052 57095.171263959775 149.1809797661668 2.2713545010864933
181071633606247054 57095.171263959775 149.1822198338826 2.3662603701715366
181071633606247055 57095.171263959775 149.1840972577531 2.3685176110804753
[...]
```


If you see something like this, then you have the wrong credentials:

```sh

-> % python aiokafka_consumer.py
Traceback (most recent call last):
  File "/home/swnelson/code/rubin/sample_alert_info/examples/alert_stream_integration_endpoint/aiokafka_consumer/virtualenv3.8/lib/python3.8/site-packages/aiokafka/conn.py", line 375, in _on_read_task_error
    read_task.result()
  File "/home/swnelson/code/rubin/sample_alert_info/examples/alert_stream_integration_endpoint/aiokafka_consumer/virtualenv3.8/lib/python3.8/site-packages/aiokafka/conn.py", line 518, in _read
    resp = await reader.readexactly(4)
  File "/usr/lib/python3.8/asyncio/streams.py", line 721, in readexactly
    raise exceptions.IncompleteReadError(incomplete, n)
asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 4 expected bytes

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "aiokafka_consumer.py", line 135, in <module>
    asyncio.run(main())
  File "/usr/lib/python3.8/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/usr/lib/python3.8/asyncio/base_events.py", line 616, in run_until_complete
    return future.result()
  File "aiokafka_consumer.py", line 93, in main
    await consumer.start()
  File "/home/swnelson/code/rubin/sample_alert_info/examples/alert_stream_integration_endpoint/aiokafka_consumer/virtualenv3.8/lib/python3.8/site-packages/aiokafka/consumer/consumer.py", line 346, in start
    await self._client.bootstrap()
  File "/home/swnelson/code/rubin/sample_alert_info/examples/alert_stream_integration_endpoint/aiokafka_consumer/virtualenv3.8/lib/python3.8/site-packages/aiokafka/client.py", line 210, in bootstrap
    bootstrap_conn = await create_conn(
  File "/home/swnelson/code/rubin/sample_alert_info/examples/alert_stream_integration_endpoint/aiokafka_consumer/virtualenv3.8/lib/python3.8/site-packages/aiokafka/conn.py", line 96, in create_conn
    await conn.connect()
  File "/home/swnelson/code/rubin/sample_alert_info/examples/alert_stream_integration_endpoint/aiokafka_consumer/virtualenv3.8/lib/python3.8/site-packages/aiokafka/conn.py", line 234, in connect
    await self._do_sasl_handshake()
  File "/home/swnelson/code/rubin/sample_alert_info/examples/alert_stream_integration_endpoint/aiokafka_consumer/virtualenv3.8/lib/python3.8/site-packages/aiokafka/conn.py", line 314, in _do_sasl_handshake
    auth_bytes = await self._send_sasl_token(
  File "/usr/lib/python3.8/asyncio/tasks.py", line 494, in wait_for
    return fut.result()
kafka.errors.KafkaConnectionError: KafkaConnectionError: Connection at alert-stream-int.lsst.cloud:9094 closed
Unclosed AIOKafkaConsumer
consumer: <aiokafka.consumer.consumer.AIOKafkaConsumer object at 0x7f29ff94d850>
```
