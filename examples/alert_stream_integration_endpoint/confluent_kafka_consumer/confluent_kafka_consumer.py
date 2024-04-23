import os
import sys
import time

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer


# Load input parameters from environment variables:
#
# $KAFKA_USERNAME should be the username of the community broker.
# $KAFKA_PASSWORD should be the password; this doesn't have a default and must
USERNAME = os.environ.get("KAFKA_USERNAME")
PASSWORD = os.environ.get("KAFKA_PASSWORD")

# These are the URLs for the integration environment of the alert stream on the
# US data facility (aka the "USDF" environment).
SERVER = "usdf-alert-stream-dev.lsst.cloud:9094"
SCHEMA_REG_URL = "https://usdf-alert-schemas-dev.slac.stanford.edu"


def main():
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
    consumer_group_id = USERNAME + "-example-ck"

    # Make a client which connects to the Schema Registry. This doesn't do
    # anything immediately; it is only called once the Consumer starts
    # receiving (and deserializing) messages.
    #
    # It uses a thread-safe cache to make sure that it only gets schema data
    # once. Schemas are kept in the cache as long as the process is running;
    # this is completely safe since schema data is immutable: the schema under
    # a particular ID will *never* change.
    sr_client = SchemaRegistryClient({"url": SCHEMA_REG_URL})

    # Make a deserializer to parse the Avro bytes, backed by the
    # SchemaRegistryClient we just made.
    deserializer = AvroDeserializer(sr_client)

    # confluent_kafka configures all of its classes with dictionaries. This one
    # sets up the bare minimum that is needed.
    config = {
        # This is the URL to use to connect to the Kafka cluster.
        "bootstrap.servers": SERVER,
        # These next two properties tell the Kafka client about the specific
        # authentication and authorization protocols that should be used when
        # connecting.
        "security.protocol": "SASL_PLAINTEXT",
        "sasl.mechanisms": "SCRAM-SHA-512",
        # The sasl.username and sasl.password are passed through over
        # SCRAM-SHA-512 auth to connect to the cluster. The username is not
        # sensitive, but the password is (of course) a secret value which
        # should never be committed to source code.
        "sasl.username": USERNAME,
        "sasl.password": PASSWORD,
        # The Consumer Group ID, as described above.
        "group.id": consumer_group_id,
        # Finally, we pass in the deserializer that we created above,
        # configuring the consumer so that it automatically does all the Schema
        # Registry and Avro deserialization work.
        "value.deserializer": deserializer
    }
    # We create a DeserializingConsumer, which is a specialized confluent_kafka
    # consumer class which communicates with the SchemaRegistry and
    # deserializes the Avro data in the stream.
    #
    # This is labeled in the confluent_kafka docs as having an "unstable API"
    # as of version 1.7.0 of confluent_kafka, so it's maybe a little dangerous
    # to use this (or even to write an example based on it!) because it might
    # change in the future. But it does seem to be the simplest valid way to do
    # this.
    consumer = DeserializingConsumer(config)

    # We tell the Consumer to listen to ("subscribe" to) a single topic, the
    # "alerts-simulated" one. Once Rubin is producing real data, this would
    # need to change to a new topic name that holds non-simulated real
    # observational data.
    #
    # This subscribe call makes sure the consumer is querying all 8 of the
    # partitions in the alerts-simulated topic.
    consumer.subscribe(["alerts-simulated"])

    # In an infinite loop, check for new messages in the stream, and print out
    # a few of their fields.
    while True:
        # consumer.poll checks for any new messages in the topic. The parameter
        # is a timeout, so this means "check for messages, but if there are no
        # messages after 1 second, just return None."
        msg = consumer.poll(1)
        if msg is None:
            # We can get None if the timeout elapses. If this is the case, just
            # print a message so the user knows that we're working and it
            # doesn't look like the process has stalled.
            print("waiting for messages...")
            time.sleep(3)
        else:
            # The message is a low-level wrapper. Full docs are available here:
            #
            #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.Message
            #
            # The short version is that it has a msg.value() method which gets
            # the deserialized data as a Python dictionary.
            deserialized = msg.value()

            # The deserialized dict has fields which map directly to the fields
            # in the Avro schema for alert packets, which is fully laid out in
            # the github.com/lsst/alert_packet repository.
            alert_id = deserialized["alertId"]
            timestamp = deserialized["diaSource"]["midpointMjdTai"]
            ra = deserialized["diaSource"]["ra"]
            decl = deserialized["diaSource"]["dec"]
            alert_timestamp = msg.timestamp()


if __name__ == "__main__":
    main()
