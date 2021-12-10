# Kafka Integration Endpoint #

The Rubin Alert Stream is provided over Kafka to community brokers.
In order to facilitate development of community broker systems, and in order to find bugs in the alert stream implementation, you can connect to an "integration" implementation of the alert stream.

The integration environment has a topic named `alerts-simulated` which repeatedly broadcasts a single visit of sample alerts every 37 seconds.

## Getting connected ##

The quickest way to connect is probably to follow an [example](../../examples/kafka_integration_endpoint).

If you already have a Kafka consumer system and just want the short version, here's what you need to know:

### Kafka Cluster

The Kafka cluster's bootstrap URL is `alert-stream-int.lsst.cloud:9094`.

TLS (aka SSL) and SCRAM-SHA-512 are required to connect; the broker is using LetsEncrypt as the CA for its certificates.

In other words, the broker is using `security.protocol=SASL_SSL` and `sasl.mechanisms=SCRAM-SHA-512`.

### Schema Registry

The Schema Registry is available at `https://alert-scheams-int.lsst.cloud`.

All GET requests are permitted without authentication, while all non-GET requests will be denied.

### Topics

The only topic that is accessible is `alerts-simulated`.
This is the topic that receives a complete visit of sample alert data every 37 seconds.

Community brokers have `Read` and `DescribeConfigs` permissions for this topic; see [the Kafka documentation](https://kafka.apache.org/documentation/#operations_resources_and_protocols) for a precises explanation of what this covers.

### Consumer Groups

Community brokers are granted global permissions of consumer groups that are prefixed with their username.

For example, the `alerce-int` community broker can create, update, and delete groups named `alerce-int-testing`, or `alerce-int-somelongsuffix`, or `alerce-int_whateveryoulike`, or anything else starting with `alerce-int`.

## Message Format: Encoding

Messages in the `alerts-simulated` topic are formatted with ["Confluent Wire Format"](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#wire-format), and are Avro-encoded.

This means that:

 - the first byte is always zero
 - the next 4 bytes represent a 32-bit unsigned integer in little endian format, which is the *schema ID* of the Avro schema which was used to encode the alert data.
 - all remaining bytes are binary-encoded Avro data

The schema ID can be used to get the complete Avro schema document from the Schema Registry.
For example, for schema ID '1', a HTTP GET to https://alert-schas-int.lsst.cloud/schemas/ids/1 will provide a description of the schema document:
```sh
-> % curl -L alert-schemas-int.lsst.cloud/schemas/ids/1
{"schema":"{\"type\":\"record\",\"name\":\"alert\",\"namespace\":\"lsst.v4_0\",
<... shortened for brevity ...>
```

The reponse is a JSON object with a key of "schema" and a value which is the Avro schema as a string.
Careful readers may notice that this means the schema is doubly-encoded; this is just a feature of the Confluent Schema Registry.
You can deserialize it like this:

```py
import requests
import json

def get_schema_dict(schema_id):
    response = requests.get(f"https://alert-schemas-int.lsst.cloud/schemas/ids/{schema_id}")
    wrapper = json.loads(response.content)
    schema = json.loads(wrapper["schema"])
    return schema
```

This shouldn't be necessary typically though since most Kafka clients understand the Confluent Wire Format directly and will do this lookup and deserialization in the background for you.

Schemas are immutable under an ID.
This means that the schema with ID 1 (for example) will never change.
Any modifications, even "irrelevant" ones like changes to documentation, will result in a new ID being generated.
This fact means that you can cache the schemas by ID forever.

## Implementation details

The broker cluster has 3 broker nodes.
The `alerts-simulated` topic is configured with a replication factor of 2, meaning that each partition is replicated onto two of those brokers.
It is configured with 8 partitions.

The choice of 8 partitions is something that may change, particularly if community brokers see benefits in wider parallelism.

The complete installation of Rubin's alert system is open source, so you can browse it if you like.
It is defined in a set of Helm charts and operators, and runs on Kubernetes on Google's Cloud:

 - [`alert-stream-broker`](https://github.com/lsst-sqre/charts/tree/master/charts/alert-stream-broker) defines the core broker resources.
   It relies upon [Strimzi](https://strimzi.io/) to handle most of the details; configuration is done through the Kafka, KafkaTopic, and KafkaUser resources.
 - `strimzi-registry-operator` ([chart](https://github.com/lsst-sqre/charts/tree/master/charts/strimzi-registry-operator), [operator](https://github.com/lsst-sqre/strimzi-registry-operator)) is used to configure the Schema Registry application and connect it to the Kafka Broker.
 - [`alert-stream-schema-registry`](https://github.com/lsst-sqre/charts/tree/master/charts/alert-stream-schema-registry) defines the Schema Registry instance which gets created by the strimzi-registry-operator.
   It also configures the ingress which gates access to only permit HTTP GET.
 - [`alert-stream-simulator`](https://github.com/lsst-sqre/charts/tree/master/charts/alert-stream-simulator) sets up the subsystem which injects alerts into the `alerts-simulated` topic.

These charts are reified with concrete values [in Phalanx](https://github.com/lsst-sqre/phalanx/blob/master/services/alert-stream-broker/values-idfint.yaml), which is a configuration system used by Rubin.
