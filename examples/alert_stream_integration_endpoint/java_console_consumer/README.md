# Java console consumer #

You can print out alert packets on the command line using the Java console consumer that ships with Kafka.
One simple way to try this out is to call the Java consumer with Docker.

The Java consumer relies upon a configuration file which holds the username and password, so you'll need to make this file by hand.
Make a file called 'consumer.properties' and fill it with this:

```
security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-512

sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
  username="YOUR-USERNAME-HERE"\
  password="YOUR-PASSWORD-HERE";
```

Of course, fill in the username and password values yourself.
It's important that you keep the quotation marks, and the backslashes (`\`), and the semicolon - just change the strings inside the quotes.

Then, from within that same directory, you can run the following docker command.
It will mount the `consumer.properties` file into `/app/consumer.properties` inside the Docker container so that the console consumer script can use it.

Note also that you need to set the `--group` field youself, since groups always must be prefixed with your username!

```sh
docker run -it --rm -v $PWD:/config confluentinc/cp-schema-registry \
    kafka-avro-console-consumer \
      --topic alerts-simulated \
      --group $KAFKA_USERNAME-example-javaconsole \
      --consumer.config /config/consumer.properties \
      --property schema.registry.url=https://usdf-alert-schemas-dev.slac.stanford.edu \
      --bootstrap-server=usdf-alert-stream-dev.lsst.cloud:9094 \
      --timeout-ms=60000
```

If this is working, it will print out enormous JSON objects which flood your terminal, since each alert contains multiple FITS files that are getting printed out byte-by-byte.

Don't get confused by the fact that the alerts appear to be JSON, here.
They are being delivered as Avro, humans can't read raw Avro data, so the `kafka-avro-console-consumer` script deserializes them and then re-encodes them as JSON for printing on the command line.

You can get a tidier output by piping the docker invocation to [jq](https://stedolan.github.io/jq/) and then selecting for a few fields. For example, to print the ID of each alert, you could do this:

```sh
docker run -it --rm -v $PWD:/config confluentinc/cp-schema-registry \
    kafka-avro-console-consumer \
      --topic alerts-simulated \
      --group $KAFKA_USERNAME-example-javaconsole \
      --consumer.config /config/consumer.properties \
      --property schema.registry.url=https://usdf-alert-schemas-dev.slac.stanford.edu\
      --bootstrap-server=usdf-alert-stream-dev.lsst.cloud:9094 \
      --timeout-ms=60000 | jq '.alertId' -r
```
