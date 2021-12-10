import json
import asyncio
import os
import sys

from schema_registry.client import SchemaRegistryClient
from schema_registry.serializers import AvroMessageSerializer

from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context


# Load input parameters from environment variables:
#
# $KAFKA_USERNAME should be the username of the community broker.
# $KAFKA_PASSWORD should be the password; this doesn't have a default and must
USERNAME = os.environ.get("KAFKA_USERNAME")
PASSWORD = os.environ.get("KAFKA_PASSWORD")

# These are the URLs for the integration environment of the alert stream on the
# interim data facility (aka the "IDF INT" environment).
SERVER = "alert-stream-int.lsst.cloud:9094"
SCHEMA_REG_URL = "https://alert-schemas-int.lsst.cloud"


async def main():
    # Validate the input parameters, exiting if we're missing them.
    if PASSWORD is None:
        print("ERROR: The $KAFKA_PASSWORD environment variable must be set")
        sys.exit(1)
    if USERNAME is None:
        print("ERROR: The $KAFKA_USERNAME environment variable must be set")
        sys.exit(1)

    # This is a Kafka Consumer Group name to use. You can use any group name
    # that is prefixed with your username.
    #
    # The Kafka consumer client requires that you pass a Group ID. This
    # Group ID is used by Kafka to keep track of your group's position in
    # the alert stream.
    consumer_group_id = USERNAME + "-example-aiokafka"

    # Make a client which connects to the Schema Registry. This doesn't do
    # anything immediately; it is only called once the Consumer starts
    # receiving (and deserializing) messages.
    schema_registry_client = SchemaRegistryClient(SCHEMA_REG_URL)

    # Create a Deserializer to parse the Avro bytes, backed by the
    # SchemaRegistryClient we just made.
    serializer = AvroMessageSerializer(schema_registry_client)

    # Create a Kafka consumer which will do all the work of communicating with
    # kafka.
    consumer = AIOKafkaConsumer(
        # The first argument to AIOKafkaConsumer is the topic which the
        # consumer should subscribe to.
        "alerts-simulated",
        # The bootstrap server is the URL to use to connect to the Kafka cluster.
        bootstrap_servers=SERVER,
        # The Consumer Group ID, as described above.
        group_id=consumer_group_id,
        # These next two properties tell the Kafka client about the specific
        # authentication and authorization protocols that should be used when
        # connecting.
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-512",
        # The sasl.username and sasl.password are passed through over
        # SCRAM-SHA-512 auth to connect to the cluster. The username is not
        # sensitive, but the password is (of course) a secret value which
        # should never be committed to source code.
        sasl_plain_username=USERNAME,
        sasl_plain_password=PASSWORD,
        # The Kafka broker is using SSL to encrypt the connection. When this is
        # the case, aiokafka requires that you provide a "SSL Context" which
        # bundles together SSL certificate data. It uses this context to verify
        # that the broker is trustworthy.
        #
        # The Rubin broker uses a certificate provided by LetsEncrypt, a
        # commonly known "certificate authority". This will be trusted by
        # default, typically, so we can create a SSL context without any
        # special configuration.
        ssl_context=create_ssl_context(),
        # Finally, we pass in the deserializer that we created above,
        # configuring the consumer so that it automatically does all the Schema
        # Registry and Avro deserialization work.
        value_deserializer=serializer.decode_message,
    )

    # We can now turn on the consumer. This will fetch topic metadata and
    # establish a subscription. It can take a bit, so we "await" here to yield
    # to any other asynchronous routines that want to do work while we get set
    # up.
    await consumer.start()

    # In an infinite loop, check for new messages in the stream, and print out
    # a few of their fields.
    while True:
        # consumer.getmany checks for a batch of new messages in the topic.
        # Retrieving a batch with getmany is much more efficient than
        # retrieving them one at a time with the consumer.getone method, but
        # both would work.
        data = await consumer.getmany(timeout_ms=1000)

        # We can get an empty data object if the timeout elapses. If this is
        # the case, just print a message so the user knows that we're working
        # and it doesn't look like the process has stalled.
        if len(data) == 0:
            print("waiting for messages...")
        for tp, messages in data.items():
            for message in messages:
                # The message is a low-level wrapper with attributes indicating
                # its offset, topic, partition, and so on.
                #
                # We're just interested in the deserialized alert data payload,
                # which is held in message.value. The alert data is provided as
                # a Python dictionary.
                deserialized = message.value

                # The deserialized dict has fields which map directly to the
                # fields in the Avro schema for alert packets, which is fully
                # laid out in the github.com/lsst/alert_packet repository.
                alert_id = deserialized["alertId"]
                timestamp = deserialized["diaSource"]["midPointTai"]
                ra = deserialized["diaSource"]["ra"]
                decl = deserialized["diaSource"]["decl"]
                print(alert_id, timestamp, ra, decl)

    # We won't ever reach this in this code, since the while loop runs forever.
    # But if you wanted to gracefully shut down, you should call
    # consumer.stop() to close up shop.
    await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
