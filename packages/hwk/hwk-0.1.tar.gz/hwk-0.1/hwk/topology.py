# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import sys

from hwk import cpu
from hwk import units
from hwk import utils

_LINUX_SYS_DEVICES_SYSTEM_NODE_DIR = '/sys/devices/system/node/'
_INFO_HELP = """Topology information
===============================================================================
`hwk.topology.Info` attributes:

architecture (string)

  A string indicating the overall architecture of the system topology (e.g.
  'NUMA' or 'SMP')

nodes (list of `hwk.topology.Node` objects)

  A list of objects representing one or more processors, memory banks (caches)
  and the bus/interconnect between them

  `hwk.topology.Node` attributes:

  id (int)

    0-based index of the node within the system

  processor_set (set of int)

    A set of integers representing the logical processors that are associated
    with this node. For example, assume a dual Intel® Xeon® Processor E5-4650
    v2 system. Each E5-4650 processor has 10 cores with 2 hardware threads per
    core, giving 40 total logical processors in the system.  Suppose the system
    reported the second Xeon processor's (NUMA node) cores (and their thread
    siblings) as logical processors 10-19 and 31-39, the value of processor_set
    would be set([10,11,12,13,14,15,16,17,18,19,31,32,33,34,35,36,37,38,39])

  cores (list of `hwk.topology.Core` objects)

    A list of objects representing the physical processing cores in the node

    `hwk.topology.Core` attributes:

    id (int)

      0-based index of the core within the system as a whole

    threads (int)

      Number of hardware threads in the core

    processor_set (set of int)

      The set of logical processor IDs for all threads in the core

    caches (list of `hwk.topology.Cache` objects)

      The memory caches that are associated with processors on this core

  caches (list of `hwk.topology.Cache` objects)

    A list of objects representing one or more memory caches associated with
    the node

    `hwk.topology.Cache` attributes:

    level (int)

      1-based number representing the "distance" or "cost to access"
      from the processor. L1 cache would have 1, L3 would have 3, etc

    type (string)

      String representing the type of information that is stored in the cache.
      May be 'unified', 'instruction' or 'data'

    size_bytes (int)

      Size in bytes of the cache

    processor_set (int)

      Set of logical processor IDs for all threads having access to the cache
"""


class Info(object):
    """Object describing the physical topology of a system."""

    def __init__(self):
        self.architecture = None
        self.nodes = None

    def __repr__(self):
        return "topology %s (%d nodes)" % (
            self.architecture,
            len(self.nodes),
        )

    def describe(self):
        return _INFO_HELP


class Node(object):

    def __init__(self, node_id):
        self.id = int(node_id)
        self.processor_set = set()
        self.cores = []
        self.caches = []

    def __repr__(self):
        return "Node %d (%d cores)" % (
            self.id,
            len(self.cores),
        )


class Core(object):

    def __init__(self, core_id):
        self.id = int(core_id)
        self.processor_set = set()
        self.caches = []

    @property
    def threads(self):
        return len(self.processor_set)

    def __repr__(self):
        return "Core %d (%d hardware threads)" % (
            self.id,
            self.threads,
        )


class Cache(object):

    def __init__(self):
        self.level = None
        self.size_bytes = None
        self.processor_set = set()

    def __repr__(self):
        size_kb = self.size_bytes // units.KB
        type_str = ''
        if self.type == 'instruction':
            type_str = 'i'
        elif self.type == 'data':
            type_str = 'd'
        cache_id_str = 'L%d%s' % (self.level, type_str)
        return "%s cache (%d KB)" % (
            cache_id_str,
            size_kb,
        )


def node_processor_set(node_id):
    """Returns a set of ints representing the logical processor IDs associated
    with the supplied NUMA node.
    """
    try:
        return {
            "linux2": _linux_node_processor_set,
        }[sys.platform](node_id)
    except KeyError:
        return None


@utils.memoize
def _linux_node_processor_set(node_id):
    # The /sys/devices/node/nodeX/cpumask file contains a hexadecimal string
    # that indicates which of the logical processors on the system are
    # associated with node X
    path = os.path.join(
        _LINUX_SYS_DEVICES_SYSTEM_NODE_DIR,
        'node' + str(node_id),
        'cpumap',
    )
    cpumap = utils.hextoi(open(path, 'rb').read())
    num_cpus = cpu.total_threads()
    return set(x for x in range(num_cpus) if cpumap & (1 << x))


def node_cores(node_id):
    """Returns a list of `hwk.topology.Core` objects representing the physical
    cores contained in the supplied NUMA node.
    """
    try:
        return {
            "linux2": _linux_node_cores,
        }[sys.platform](node_id)
    except KeyError:
        return None


@utils.memoize
def _linux_node_cores(node_id):
    # The /sys/devices/node/nodeX directory contains a subdirectory called
    # 'cpuX' for each logical processor assigned to the node. Each of those
    # subdirectories containers a topology subdirectory which has a core_id
    # file that indicates the 0-based identifier of the physical core the
    # logical processor (hardware thread) is on.
    path = os.path.join(
        _LINUX_SYS_DEVICES_SYSTEM_NODE_DIR,
        'node' + str(node_id),
    )
    cores = {}
    for filename in os.listdir(path):
        if not filename.startswith('cpu'):
            continue
        cpu_path = os.path.join(path, filename)
        if not os.path.isdir(cpu_path):
            # There are two files in the node directory that start with 'cpu'
            # but are not subdirectories ('cpulist' and 'cpumap'). Ignore these
            # files.
            continue
        # Grab the logical processor ID by cutting the integer from the
        # filename of the CPU
        lp_id = int(filename[3:])
        core_id_path = os.path.join(cpu_path, 'topology', 'core_id')
        core_id = int(open(core_id_path, 'rb').read())
        if core_id in cores:
            core = cores[core_id]
        else:
            core = Core(core_id)
            cores[core_id] = core
        core.processor_set.add(lp_id)

    cores = cores.values()
    caches = _linux_node_caches(node_id)
    # Map the cache to the core, depending on intersection of core's
    # processor_set and cache's processor_set.
    for cache in caches:
        for core in cores:
            if core.processor_set & cache.processor_set:
                core.caches.append(cache)
    return cores


def node_caches(node_id):
    """Returns a list of `hwk.topology.Cache` objects representing the physical
    varius memory caches associated to cores/threads in the supplied NUMA node.
    """
    try:
        return {
            "linux2": _linux_node_caches,
        }[sys.platform](node_id)
    except KeyError:
        return None


@utils.memoize
def _linux_node_caches(node_id):
    # The /sys/devices/node/nodeX directory contains a subdirectory called
    # 'cpuX' for each logical processor assigned to the node. Each of those
    # subdirectories containers a 'cache' subdirectory which contains a number
    # of subdirectories beginning with 'index' and ending in the cache's
    # internal 0-based identifier. Those subdirectories contain a number of
    # files, including 'shared_cpu_list', 'size', and 'type' which we use to
    # determine cache characteristics.
    path = os.path.join(
        _LINUX_SYS_DEVICES_SYSTEM_NODE_DIR,
        'node' + str(node_id),
    )
    caches = {}
    for filename in os.listdir(path):
        if not filename.startswith('cpu'):
            continue
        cpu_path = os.path.join(path, filename)
        if not os.path.isdir(cpu_path):
            # There are two files in the node directory that start with 'cpu'
            # but are not subdirectories ('cpulist' and 'cpumap'). Ignore these
            # files.
            continue
        # Grab the logical processor ID by cutting the integer from the
        # filename of the CPU
        lp_id = int(filename[3:])
        cache_path = os.path.join(cpu_path, 'cache')
        for cpu_filename in os.listdir(cache_path):
            if not cpu_filename.startswith('index'):
                continue
            type_path = os.path.join(cache_path, cpu_filename, 'type')
            type = open(type_path, 'rb').read().strip().lower()
            level_path = os.path.join(cache_path, cpu_filename, 'level')
            level = int(open(level_path, 'rb').read().strip())
            size_path = os.path.join(cache_path, cpu_filename, 'size')
            size = open(size_path, 'rb').read().strip()
            scpu_path = os.path.join(
                cache_path,
                cpu_filename,
                'shared_cpu_map',
            )
            shared_cpu_map = open(scpu_path, 'rb').read().strip()
            cache_key = (level, type, shared_cpu_map)
            if cache_key in caches:
                cache = caches[cache_key]
            else:
                cache = Cache()
                cache.level = level
                cache.type = type
                cache.size_bytes = int(size[:-1]) * units.KB
                caches[cache_key] = cache
            cache.processor_set.add(lp_id)

    return caches.values()


def info():
    """Returns a `hwk.topology.Info` object containing information on the
    physical topology in the system, or None if the information could not be
    determined.
    """
    try:
        return {
            "linux2": _linux_info,
        }[sys.platform]()
    except KeyError:
        return None


@utils.memoize
def _linux_info():
    nodes = []
    for filename in os.listdir(_LINUX_SYS_DEVICES_SYSTEM_NODE_DIR):
        if filename.startswith('node'):
            node_id = filename[4:]
            node = Node(node_id)
            node.processor_set = _linux_node_processor_set(node_id)
            node.caches = _linux_node_caches(node_id)
            node.cores = _linux_node_cores(node_id)
            nodes.append(node)

    res = Info()
    res.architecture = 'NUMA' if len(nodes) > 1 else 'SMP'
    res.nodes = nodes
    return res
