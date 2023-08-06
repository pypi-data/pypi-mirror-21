#
# (C) ITculate, Inc. 2015-2017
# All rights reserved
# Licensed under MIT License (see LICENSE)
#

__version__ = "0.12.3"

import six
import logging
import collections
# noinspection PyPackageRequirements
from unix_dates import UnixDate
from .exceptions import SDKError
from .graph import Vertex, Edge
from .dictionary import Dictionary
from .sample import TimeSeriesSample
from .types import *
from .uploader import Provider, TopologyPayloadGenerator, GlobalPayloadGenerator
import statsd

logger = logging.getLogger(__name__)

_tenant_id = None
_provider = None
_topologies = {}  # type: dict[str, TopologyPayloadGenerator]
_data = None  # type: GlobalPayloadGenerator


def _get_topology_provider(collector_id):
    global _topologies

    assert _topologies is not None and isinstance(_topologies, dict), "SDK was not initialized!"

    payload_generator = _topologies.get(collector_id)

    if payload_generator is None:
        payload_generator = TopologyPayloadGenerator(tenant_id=_tenant_id, collector_id=collector_id)

        _topologies[collector_id] = payload_generator

    return payload_generator


class Flusher(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Make sure all changes are flushed
        flush_all()


def init(provider=None, host=None, tenant_id=None, **kwargs):
    """
    Initialize a global uploader that will be used to upload data to ITculate.

    The API key provided must have the 'upload' role (and associated with a single tenant).

    Possible providers are:
        'SynchronousApiUploader' (default) - Upload straight to the ITculate API server
        'AgentForwarder' - Forwards payload to an ITculate agent
        'InMemory' - Accumulates latest status in memory

    :param str provider: Name of the provider class to use (defaults to 'SynchronousApiUploader')
    :param str host: Identifier of host reporting (defaults to hostname)
    :param str tenant_id: optional tenant to report (if not provided, tenant is derived from user login data)
    :param kwargs: Provider-specific settings

    :return A flusher instance (to be able to use with the 'with' statement)
    """
    global _tenant_id, _provider, _topologies, _data

    provider = provider or "SynchronousApiUploader"

    if host is None:
        import socket
        host = socket.gethostname()

    provider_settings = {
        "provider": provider,
        "host": host,
    }

    # Only take values that are not None
    provider_settings.update({k: v for k, v in six.iteritems(kwargs) if v is not None})

    _tenant_id = tenant_id

    # Create the provider (will assert if provider not supported)
    _provider = Provider.factory(provider_settings)

    _topologies = {}  # Topologies by collector_id

    _data = GlobalPayloadGenerator(tenant_id=tenant_id)  # All other data will be sent together in a single payload

    # Initialize the statsd
    if provider == "AgentForwarder":
        statsd.init(port=int(provider_settings.get("statsd_port", 8125)))

    return Flusher()


def add_vertex(collector_id,
               vertex_type,
               name,
               keys,
               counter_types=None,
               data=None,
               **kwargs):
    """
    Adds a vertex to the uploader

    :param str collector_id: Unique name identifying the reporter of this topology
    :param str vertex_type: Vertex type
    :param dict[str,str]|str keys: A set of unique keys identifying this vertex. If str, 'pk' will be used as key
    :param str name: Name for vertex
    :param dict[str,DataType] counter_types: (optional) mapping of the different counters reported by this vertex
    :param dict data: Set of initial values to assign to vertex (optional)
    :param kwargs: Any additional key:value pairs that should be assigned to vertex.
    :rtype: Vertex
    """

    return _get_topology_provider(collector_id).add_vertex(vertex_type=vertex_type,
                                                           name=name,
                                                           keys=keys,
                                                           counter_types=counter_types,
                                                           data=data,
                                                           **kwargs)


def connect(source, target, topology, collector_id):
    """
    Connect (create an edge between) two (or two sets of) vertices.
    Vertices are identified by either providing the Vertex object or only their keys.

    If source / target is a list of vertices (or keys), this will create a set of edges between all sources and all
    targets

    :param str collector_id: Unique name identifying the reporter of this topology
    :param source: Identify source/s
    :type source: str|dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex]|collections.Iterable[str]
    :param target: Identify target/s
    :type target: str|dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex]|collections.Iterable[str]
    :param str topology: Topology (edge type) to use
    """

    _get_topology_provider(collector_id).connect(source=source, target=target, topology=topology)


def add_sample(vertex, counter, value, timestamp=None):
    """
    Add a single sample for a counter

    :param Vertex|str vertex: Vertex object or vertex key
    :param str counter: Counter name
    :param float|TypedValue value: Value for counter
    :param float timestamp: A unix timestamp (seconds since epoch). If None, current time is taken.
    """
    if timestamp is None:
        timestamp = UnixDate.now()

    add_samples(vertex=vertex, counter=counter, timestamp_to_value=((timestamp, value),))


def add_samples(vertex, counter, timestamp_to_value):
    """
    Add a series of samples for a single counter

    :param Vertex|str vertex: Vertex object or vertex key
    :param str counter: Counter name
    :param collections.Iterable[(float, float|TypedValue)] timestamp_to_value: An iterable of pairs of timestamp, value
    """
    assert isinstance(vertex, Vertex) or isinstance(vertex, str), "Bad class type fpr vertex - {}".format(
        vertex.__class__.__name__)

    _data.add_counter_samples(vertex=vertex, counter=counter, timestamp_to_value=timestamp_to_value)


def enable_grouper_algorithm(group_vertex_type, member_vertex_type, topology):
    """
    Configure the grouping algorithm to group together vertices of type 'member_vertex_type' under group vertices
    of type 'group_vertex_type' by adding group edges of type 'topology'.

    Once configured, the algorithm will run periodically, adding new edges for the group, while keeping the original
    edges intact.

    :param str group_vertex_type: Vertex type
    :param str member_vertex_type: Vertex type
    :param str topology: Topology (edge type) to use
    """

    meta_data = Dictionary.lookup_algorithm_meta_data(vertex_type=member_vertex_type, name="grouper")
    meta_data = meta_data if meta_data else {"groups_info": []}
    for info in meta_data["groups_info"]:
        if info["group_edge_type"] == topology and info["group_vertex_type"] == group_vertex_type:
            # meta_data already contains this, do nothing
            return

    meta_data["groups_info"].append({"group_vertex_type": group_vertex_type, "group_edge_type": topology})

    Dictionary.update_algorithm(vertex_type=member_vertex_type, name="grouper", meta_data=meta_data)


def vertex_event(vertex, message, event_type="MESSAGE", severity="INFO", timestamp=None):
    """
    Generic event

    :param Vertex|str vertex: Vertex (or vertex key) associated with event
    :param str severity: One of CRITICAL / ERROR / WARNING / INFO / SUCCESS
    :param str event_type: A free text with event type
    :param str message: A free text describing the event
    :param float timestamp: An optional time of event (defaults to now)
    """
    _data.vertex_event(vertex=vertex, message=message, event_type=event_type, severity=severity, timestamp=timestamp)


def vertex_healthy(vertex, message=None, timestamp=None):
    """
    Health (up) event - indicates a vertex is healthy.

    Under the hood, this Will generate an event of type "HEALTHY" with severity "SUCCESS".
    If message is not provided, the default message would be: "{Vertex type} {Vertex name} is healthy"

    :param Vertex|str vertex: Vertex (or vertex key) associated with event
    :param str message: A free text describing the event
    :param float timestamp: An optional time of event (defaults to now)
    """
    vertex_event(vertex=vertex, message=message, event_type="HEALTHY", severity="SUCCESS", timestamp=timestamp)


def vertex_unhealthy(vertex, message=None, timestamp=None):
    """
    Health (down) event - indicates a vertex is unhealthy.

    Under the hood, this Will generate an event of type "HEALTHY" with severity "SUCCESS".
    If message is not provided, the default message would be: "{Vertex type} {Vertex name} is unhealthy"

    :param Vertex|str vertex: Vertex (or vertex key) associated with event
    :param str message: A free text describing the event
    :param float timestamp: An optional time of event (defaults to now)
    """
    vertex_event(vertex=vertex, message=message, event_type="UNHEALTHY", severity="ERROR", timestamp=timestamp)


def flush_topology(collector_id):
    """
    Flush a topology collected by the given collector id

    :param collector_id:
    :return: True if any data was flushed
    :rtype: bool
    """
    assert collector_id in _topologies, "Collector ID '{}' not recognized".format(collector_id)

    topology_provider = _get_topology_provider(collector_id=collector_id)
    return _provider.flush_now((topology_provider, _data,)) > 0


def flush_all():
    """
    Flushes all unsent data without waiting for the next interval
    :return: number of payloads flushed
    """

    def all_payload_providers():
        for topology_provider in six.itervalues(_topologies):
            yield topology_provider

        yield _data

    return _provider.flush_now(all_payload_providers())
