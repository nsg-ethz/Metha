import os

from utils import *
from RouterConfiguration.Juniper.juniper_config_features import *
from network_features import *

feature_config = {
    ProtocolIndependentFeatures.STATIC_ROUTE: lambda network,
                                                       interface: f'set routing-options static route {int_to_ip(network.address)}/{network.prefix} next-hop {interface.name}',

    OSPFFeatures.AREA_RANGE: lambda area, network, override_metric,
                                    restrict: f'set protocols ospf area {area} area-range {int_to_ip(network.address)}/{network.prefix} {override_metric} {restrict}',
    OSPFFeatures.AREA_LABEL_SWITCHED_PATH: lambda area, path,
                                                  metric: f'set protocols ospf area {area} label-switched-path {path} metric {metric}',
    OSPFFeatures.NSSA_DEFAULT_LSA: lambda area, metric, metric_type,
                                          type_7: f'set protocols ospf area {area} nssa default-lsa default-metric {metric} {metric_type} {type_7}',
    OSPFFeatures.NSSA_NO_SUMMARIES: lambda area: f'set protocols ospf area {area} nssa no-summaries',
    OSPFFeatures.STUB_DEFAULT_METRIC: lambda area,
                                             metric: f'set protocols ospf area {area} stub default-metric {metric}',
    OSPFFeatures.STUB_NO_SUMMARIES: lambda area: f'set protocols ospf area {area} stub no-summaries',
    OSPFFeatures.EXTERNAL_PREFERENCE: lambda preference: f'set protocols ospf external-preference {preference}',
    OSPFFeatures.NO_RFC_1583: lambda: f'set protocols ospf no-rfc-1583',
    OSPFFeatures.REFERENCE_BANDWIDTH: lambda bandwidth: f'set protocols ospf reference-bandwidth {bandwidth}',
    OSPFFeatures.INTERFACE_LDP_SYNCHRONIZATION: lambda interface,
                                                       disable: f'set protocols ospf area {interface.area} interface {interface.name} ldp-sychronization {disable}',
    OSPFFeatures.INTERFACE_LINK_PROTECTION: lambda
        interface: f'set protocols ospf area {interface.area} interface {interface.name} link-protection',
    OSPFFeatures.INTERFACE_METRIC: lambda interface,
                                          metric: f'set protocols ospf area {interface.area} interface {interface.name} metric {metric}',
    OSPFFeatures.INTERFACE_PASSIVE: lambda
        interface: f'set protocols ospf area {interface.area} interface {interface.name} passive',
    OSPFFeatures.INTERFACE_PRIORITY: lambda interface,
                                            priority: f'set protocols ospf area {interface.area} interface {interface.name} priority {priority}',
    OSPFFeatures.INTERFACE_TE_METRIC: lambda interface,
                                             metric: f'set protocols ospf area {interface.area} interface {interface.name} te-metric {metric}',
    OSPFFeatures.REDISTRIBUTE_DIRECT: lambda: f'set protocols ospf export send-direct',
    OSPFFeatures.REDISTRIBUTE_STATIC: lambda: f'set protocols ospf export send-static',
    OSPFFeatures.REDISTRIBUTE_BGP: lambda: f'set protocols ospf export send-bgp',
    OSPFFeatures.EXPORT: lambda: f'set protocols ospf export export-ospf',
    OSPFFeatures.IMPORT: lambda: f'set protocols ospf import import-ospf',

    BGPFeatures.ACCEPTED_PREFIX_LIMIT: lambda
        limit: f'set protocols bgp family inet any accepted-prefix-limit maximum {limit}',
    BGPFeatures.ADVERTISE_EXTERNAL: lambda group: f'set protocols bgp group {group} advertise-external',
    BGPFeatures.ADVERTISE_INACTIVE: lambda: f'set protocols bgp advertise-inactive',
    BGPFeatures.ADVERTISE_PEER_AS: lambda: f'set protocols bgp advertise-peer-as',
    BGPFeatures.AS_OVERRIDE: lambda group: f'set protocols bgp group {group} as-override',
    BGPFeatures.CLUSTER: lambda: f'',
    BGPFeatures.DAMPING: lambda: f'set protocols bgp damping',
    BGPFeatures.ENFORCE_FIRST_AS: lambda: f'set protocols bgp group EBGP enforce-first-as',
    BGPFeatures.LOCAL_AS: lambda AS, option: f'set protocols bgp local-as {AS.num} {option}',
    BGPFeatures.METRIC_OUT: lambda metric: f'set protocols bgp metric-out {metric}',
    BGPFeatures.MULTIHOP: lambda: f'',
    BGPFeatures.NO_CLIENT_REFLECT: lambda: f'set protocols bgp no-client-reflect',
    BGPFeatures.PASSIVE: lambda: f'set protocols bgp passive',
    BGPFeatures.PATH_SELECTION: lambda option: f'set protocols bgp path-selection {option}',
    BGPFeatures.REMOVE_PRIVATE: lambda: f'set protocols bgp remove-private',
    BGPFeatures.TCP_MSS: lambda size: f'set protocols bgp tcp-mss {size}',
    BGPFeatures.ADD_PATH: lambda group,
                                 options: f'set protocols bgp group {group} family inet unicast add-path {options}',
    BGPFeatures.LOOPS: lambda loops: f'set protocols bgp family inet unicast loops {loops}',
    BGPFeatures.PREFIX_LIMIT: lambda limit: f'set protocols bgp family inet any prefix-limit maximum {limit}',
    BGPFeatures.REDISTRIBUTE_DIRECT: lambda: f'set protocols bgp export send-direct',
    BGPFeatures.REDISTRIBUTE_STATIC: lambda: f'set protocols bgp export send-static',
    BGPFeatures.REDISTRIBUTE_OSPF: lambda: f'set protocols bgp export send-ospf',
    BGPFeatures.IMPORT: lambda: f'set protocols bgp import import-bgp',
    BGPFeatures.EXPORT: lambda: f'set protocols bgp export export-bgp',
    BGPFeatures.LOCAL_PREFERENCE: lambda pref: f'set protocols bgp local-preference {pref}',

    BGPFeatures.NEIGHBOUR_POLICY_EXPORT: lambda neighbour, policy: f'set protocols bgp group {neighbour.group} neighbor {int_to_ip(neighbour.address)} export {policy.name}',
    BGPFeatures.NEIGHBOUR_POLICY_IMPORT: lambda neighbour, policy: f'set protocols bgp group {neighbour.group} neighbor {int_to_ip(neighbour.address)} import {policy.name}',

    PolicyFeatures.FROM_AREA: lambda policy, term, area: f'set policy-options policy-statement {policy.name} term {term} from area {area}',
    PolicyFeatures.FROM_AS_PATH: lambda policy, term, as_path: f'set policy-options policy-statement {policy.name} term {term} from as-path {as_path}',
    PolicyFeatures.FROM_AS_PATH_GROUP: lambda policy, term, group: f'set policy-options policy-statement {policy.name} term {term} from as-path-group {group}',
    PolicyFeatures.FROM_COLOR: lambda policy, term, color: f'set policy-options policy-statement {policy.name} term {term} from color {color}',
    PolicyFeatures.FROM_COMMUNITY: lambda policy, term, community: f'set policy-options policy-statement {policy.name} term {term} from community {community}',
    PolicyFeatures.FROM_FAMILY: lambda policy, term, family: f'set policy-options policy-statement {policy.name} term {term} from family {family}',
    PolicyFeatures.FROM_INSTANCE: lambda: f'',
    PolicyFeatures.FROM_INTERFACE: lambda policy, term, interface: f'set policy-options policy-statement {policy.name} term {term} from interface {interface.name}',
    PolicyFeatures.FROM_LEVEL: lambda: f'',
    PolicyFeatures.FROM_LOCAL_PREFERENCE: lambda policy, term, preference: f'set policy-options policy-statement {policy.name} term {term} from local-preference {preference}',
    PolicyFeatures.FROM_METRIC: lambda policy, term, metric: f'set policy-options policy-statement {policy.name} term {term} from metric {metric}',
    PolicyFeatures.FROM_NEIGHBOUR: lambda policy, term, neighbour: f'set policy-options policy-statement {policy.name} term {term} from neighbor {int_to_ip(neighbour.address)}',
    PolicyFeatures.FROM_ORIGIN: lambda policy, term, origin: f'set policy-options policy-statement {policy.name} term {term} from origin {origin}',
    PolicyFeatures.FROM_POLICY: lambda policy, term, policy2: f'set policy-options policy-statement {policy.name} term {term} from policy {policy2}',
    PolicyFeatures.FROM_PREFIX_LIST: lambda policy, term, prefix_list: f'set policy-options policy-statement {policy.name} term {term} from prefix-list {prefix_list}',
    PolicyFeatures.FROM_PREFIX_LIST_FILTER: lambda policy, term, prefix_list, match_type: f'set policy-options policy-statement {policy.name} term {term} from prefix-list-filter {prefix_list} {match_type}',
    PolicyFeatures.FROM_PROTOCOL: lambda policy, term, protocol: f'set policy-options policy-statement {policy.name} term {term} from protocol {protocol}',
    PolicyFeatures.FROM_RIB: lambda policy, term, rib: f'set policy-options policy-statement {policy.name} term {term} from rib {rib}',
    PolicyFeatures.FROM_ROUTE_FILTER: lambda policy, term, net, match_type: f'set policy-options policy-statement {policy.name} term {term} from route-filter {int_to_ip(net.address)}/{net.prefix} {match_type}',
    PolicyFeatures.FROM_ROUTE_TYPE: lambda policy, term, route_type: f'set policy-options policy-statement {policy.name} term {term} from route-type {route_type}',
    PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER: lambda policy, term, source_filter, match_type: f'set policy-options policy-statement {policy.name} term {term} from source-address-filter {source_filter} {match_type}',
    PolicyFeatures.FROM_TAG: lambda policy, term, tag: f'set policy-options policy-statement {policy.name} term {term} from tag {tag}',
    PolicyFeatures.FROM_NEXT_HOP: lambda policy, term, next_hop: f'set policy-options policy-statement {policy.name} term {term} from next-hop {int_to_ip(next_hop)}',
    PolicyFeatures.TO_LEVEL: lambda: f'',
    PolicyFeatures.TO_RIB: lambda: f'',
    PolicyFeatures.THEN_ACCEPT: lambda policy, term: f'set policy-options policy-statement {policy.name} term {term} then accept',
    PolicyFeatures.THEN_AS_PATH_EXPAND: lambda policy, term, n: f'set policy-options policy-statement {policy.name} term {term} then as-path-expand last-as count {n}',
    PolicyFeatures.THEN_AS_PATH_PREPEND: lambda policy, term, as_path: f'set policy-options policy-statement {policy.name} term {term} then as-path-prepend {as_path}',
    PolicyFeatures.THEN_COLOR: lambda policy, term, add, color: f'set policy-options policy-statement {policy.name} term {term} then color {add} {color}',
    PolicyFeatures.THEN_COLOR2: lambda policy, term, add, color: f'set policy-options policy-statement {policy.name} term {term} then color2 {add} {color}',
    PolicyFeatures.THEN_COMMUNITY_ADD: lambda policy, term, community: f'set policy-options policy-statement {policy.name} term {term} then community add {community}',
    PolicyFeatures.THEN_COMMUNITY_DELETE: lambda policy, term, community: f'set policy-options policy-statement {policy.name} term {term} then community delete {community}',
    PolicyFeatures.THEN_COMMUNITY_SET: lambda policy, term, community: f'set policy-options policy-statement {policy.name} term {term} then community set {community}',
    PolicyFeatures.THEN_COS_NEXT_HOP_MAP: lambda policy, term, cos_map: f'set policy-options policy-statement {policy.name} term {term} then cos-next-hop-map {cos_map}',
    PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT: lambda policy, term: f'set policy-options policy-statement {policy.name} term {term} then default-action accept',
    PolicyFeatures.THEN_DEFAULT_ACTION_REJECT: lambda policy, term: f'set policy-options policy-statement {policy.name} term {term} then default-action reject',
    PolicyFeatures.THEN_EXTERNAL: lambda policy, term, metric_type: f'set policy-options policy-statement {policy.name} term {term} then external type {metric_type}',
    PolicyFeatures.THEN_FORWARDING_CLASS: lambda policy, term, fwd_class: f'set policy-options policy-statement {policy.name} term {term} then forwarding-class {fwd_class}',
    PolicyFeatures.THEN_INSTALL_NEXTHOP: lambda: f'',
    PolicyFeatures.THEN_LOCAL_PREFERENCE: lambda policy, term, pref: f'set policy-options policy-statement {policy.name} term {term} then local-preference {pref}',
    PolicyFeatures.THEN_METRIC: lambda policy, term, metric: f'set policy-options policy-statement {policy.name} term {term} then metric {metric}',
    PolicyFeatures.THEN_METRIC_ADD: lambda policy, term, metric: f'set policy-options policy-statement {policy.name} term {term} then metric add {metric}',
    PolicyFeatures.THEN_METRIC_EXPRESSION: lambda: f'',
    PolicyFeatures.THEN_METRIC_IGP: lambda policy, term, offset: f'set policy-options policy-statement {policy.name} term {term} then metric igp {offset}',
    PolicyFeatures.THEN_METRIC2: lambda policy, term, metric: f'set policy-options policy-statement {policy.name} term {term} then metric2 {metric}',
    PolicyFeatures.THEN_METRIC2_EXPRESSION: lambda: f'',
    PolicyFeatures.THEN_NEXT_HOP: lambda policy, term, next_hop: f'set policy-options policy-statement {policy.name} term {term} then next-hop {int_to_ip(next_hop)}',
    PolicyFeatures.THEN_NEXT_HOP_SELF: lambda policy, term: f'set policy-options policy-statement {policy.name} term {term} then next-hop self',
    PolicyFeatures.THEN_NEXT_POLICY: lambda: f'',
    PolicyFeatures.THEN_NEXT_TERM: lambda: f'',
    PolicyFeatures.THEN_ORIGIN: lambda policy, term, origin: f'set policy-options policy-statement {policy.name} term {term} then origin {origin}',
    PolicyFeatures.THEN_PREFERENCE: lambda policy, term, pref: f'set policy-options policy-statement {policy.name} term {term} then preference {pref}',
    PolicyFeatures.THEN_PRIORITY: lambda policy, term, priority: f'set policy-options policy-statement {policy.name} term {term} then priority {priority}',
    PolicyFeatures.THEN_REJECT: lambda policy, term: f'set policy-options policy-statement {policy.name} term {term} then reject',
    PolicyFeatures.THEN_TAG: lambda policy, term, tag: f'set policy-options policy-statement {policy.name} term {term} then tag {tag}',

    PolicyFeatures.POLICY_MATCH_FEATURE_BGP_OUT: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args),
    PolicyFeatures.POLICY_MATCH_FEATURE_BGP_IN: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args),
    PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_OUT: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args),
    PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_IN: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_BGP_OUT: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_BGP_IN: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_OSPF_OUT: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_OSPF_IN: lambda policy, term, feature, *args: feature_config[feature](policy, term, *args)
}

feature_disable = {
    ProtocolIndependentFeatures.STATIC_ROUTE: lambda network,
                                                       interface: f'delete routing-options static route {int_to_ip(network.address)}/{network.prefix} next-hop {interface.name}',

    OSPFFeatures.AREA_RANGE: lambda area, network, override_metric,
                                    restrict: f'delete protocols ospf area {area} area-range {int_to_ip(network.address)}/{network.prefix}',
    OSPFFeatures.AREA_LABEL_SWITCHED_PATH: lambda area, path,
                                                  metric: f'delete protocols ospf area {area} label-switched-path {path} metric {metric}',
    OSPFFeatures.NSSA_DEFAULT_LSA: lambda area, metric, metric_type,
                                          type_7: f'delete protocols ospf area {area} nssa default-lsa',
    OSPFFeatures.NSSA_NO_SUMMARIES: lambda area: f'delete protocols ospf area {area} nssa no-summaries',
    OSPFFeatures.STUB_DEFAULT_METRIC: lambda area,
                                             metric: f'delete protocols ospf area {area} stub default-metric {metric}',
    OSPFFeatures.STUB_NO_SUMMARIES: lambda area: f'delete protocols ospf area {area} stub no-summaries',
    OSPFFeatures.EXTERNAL_PREFERENCE: lambda preference: f'delete protocols ospf external-preference {preference}',
    OSPFFeatures.NO_RFC_1583: lambda: f'delete protocols ospf no-rfc-1583',
    OSPFFeatures.REFERENCE_BANDWIDTH: lambda bandwidth: f'delete protocols ospf reference-bandwidth {bandwidth}',
    OSPFFeatures.INTERFACE_LDP_SYNCHRONIZATION: lambda interface,
                                                       disable: f'delete protocols ospf area {interface.area} interface {interface.name} ldp-sychronization',
    OSPFFeatures.INTERFACE_LINK_PROTECTION: lambda
        interface: f'delete protocols ospf area {interface.area} interface {interface.name} link-protection',
    OSPFFeatures.INTERFACE_METRIC: lambda interface,
                                          metric: f'delete protocols ospf area {interface.area} interface {interface.name} metric {metric}',
    OSPFFeatures.INTERFACE_PASSIVE: lambda
        interface: f'delete protocols ospf area {interface.area} interface {interface.name} passive',
    OSPFFeatures.INTERFACE_PRIORITY: lambda interface,
                                            priority: f'delete protocols ospf area {interface.area} interface {interface.name} priority {priority}',
    OSPFFeatures.INTERFACE_TE_METRIC: lambda interface,
                                             metric: f'delete protocols ospf area {interface.area} interface {interface.name} te-metric {metric}',
    OSPFFeatures.REDISTRIBUTE_DIRECT: lambda: f'delete protocols ospf export send-direct',
    OSPFFeatures.REDISTRIBUTE_STATIC: lambda: f'delete protocols ospf export send-static',
    OSPFFeatures.REDISTRIBUTE_BGP: lambda: f'delete protocols ospf export send-bgp',
    OSPFFeatures.EXPORT: lambda: f'delete protocols ospf export export-ospf',
    OSPFFeatures.IMPORT: lambda: f'delete protocols ospf import import-ospf',

    BGPFeatures.ACCEPTED_PREFIX_LIMIT: lambda
        limit: f'delete protocols bgp family inet any accepted-prefix-limit maximum {limit}',
    BGPFeatures.ADVERTISE_EXTERNAL: lambda group: f'delete protocols bgp group {group} advertise-external',
    BGPFeatures.ADVERTISE_INACTIVE: lambda: f'delete protocols bgp advertise-inactive',
    BGPFeatures.ADVERTISE_PEER_AS: lambda: f'delete protocols bgp advertise-peer-as',
    BGPFeatures.AS_OVERRIDE: lambda group: f'delete protocols bgp group {group} as-override',
    BGPFeatures.CLUSTER: lambda: f'',
    BGPFeatures.DAMPING: lambda: f'delete protocols bgp damping',
    BGPFeatures.ENFORCE_FIRST_AS: lambda: f'delete protocols bgp group EBGP enforce-first-as',
    BGPFeatures.LOCAL_AS: lambda AS, option: f'delete protocols bgp local-as {AS.num}',
    BGPFeatures.METRIC_OUT: lambda metric: f'delete protocols bgp metric-out {metric}',
    BGPFeatures.MULTIHOP: lambda: f'',
    BGPFeatures.NO_CLIENT_REFLECT: lambda: f'delete protocols bgp no-client-reflect',
    BGPFeatures.PASSIVE: lambda: f'delete protocols bgp passive',
    BGPFeatures.PATH_SELECTION: lambda option: f'delete protocols bgp path-selection',
    BGPFeatures.REMOVE_PRIVATE: lambda: f'delete protocols bgp remove-private',
    BGPFeatures.TCP_MSS: lambda size: f'delete protocols bgp tcp-mss {size}',
    BGPFeatures.ADD_PATH: lambda group, options: f'delete protocols bgp group {group} family inet unicast add-path',
    BGPFeatures.LOOPS: lambda loops: f'delete protocols bgp family inet unicast loops {loops}',
    BGPFeatures.PREFIX_LIMIT: lambda limit: f'delete protocols bgp family inet any prefix-limit maximum {limit}',
    BGPFeatures.REDISTRIBUTE_DIRECT: lambda: f'delete protocols bgp export send-direct',
    BGPFeatures.REDISTRIBUTE_STATIC: lambda: f'delete protocols bgp export send-static',
    BGPFeatures.REDISTRIBUTE_OSPF: lambda: f'delete protocols bgp export send-ospf',
    BGPFeatures.IMPORT: lambda: f'delete protocols bgp import import-bgp',
    BGPFeatures.EXPORT: lambda: f'delete protocols bgp export export-bgp',
    BGPFeatures.LOCAL_PREFERENCE: lambda pref: f'delete protocols bgp local-preference {pref}',

    BGPFeatures.NEIGHBOUR_POLICY_EXPORT: lambda neighbour, policy: f'delete protocols bgp group {neighbour.group} neighbor {int_to_ip(neighbour.address)} export {policy.name}',
    BGPFeatures.NEIGHBOUR_POLICY_IMPORT: lambda neighbour, policy: f'delete protocols bgp group {neighbour.group} neighbor {int_to_ip(neighbour.address)} import {policy.name}',

    PolicyFeatures.FROM_AREA: lambda policy, term, area: f'delete policy-options policy-statement {policy.name} term {term} from area {area}',
    PolicyFeatures.FROM_AS_PATH: lambda policy, term, as_path: f'delete policy-options policy-statement {policy.name} term {term} from as-path {as_path}',
    PolicyFeatures.FROM_AS_PATH_GROUP: lambda policy, term, group: f'delete policy-options policy-statement {policy.name} term {term} from as-path-group {group}',
    PolicyFeatures.FROM_COLOR: lambda policy, term, color: f'delete policy-options policy-statement {policy.name} term {term} from color {color}',
    PolicyFeatures.FROM_COMMUNITY: lambda policy, term, community: f'delete policy-options policy-statement {policy.name} term {term} from community {community}',
    PolicyFeatures.FROM_FAMILY: lambda policy, term, family: f'delete policy-options policy-statement {policy.name} term {term} from family {family}',
    PolicyFeatures.FROM_INSTANCE: lambda: f'',
    PolicyFeatures.FROM_INTERFACE: lambda policy, term, interface: f'delete policy-options policy-statement {policy.name} term {term} from interface {interface.name}',
    PolicyFeatures.FROM_LEVEL: lambda: f'',
    PolicyFeatures.FROM_LOCAL_PREFERENCE: lambda policy, term, preference: f'delete policy-options policy-statement {policy.name} term {term} from local-preference {preference}',
    PolicyFeatures.FROM_METRIC: lambda policy, term, metric: f'delete policy-options policy-statement {policy.name} term {term} from metric {metric}',
    PolicyFeatures.FROM_NEIGHBOUR: lambda policy, term, neighbour: f'delete policy-options policy-statement {policy.name} term {term} from neighbor {int_to_ip(neighbour.address)}',
    PolicyFeatures.FROM_ORIGIN: lambda policy, term, origin: f'delete policy-options policy-statement {policy.name} term {term} from origin {origin}',
    PolicyFeatures.FROM_POLICY: lambda policy, term, policy2: f'delete policy-options policy-statement {policy.name} term {term} from policy {policy2}',
    PolicyFeatures.FROM_PREFIX_LIST: lambda policy, term, prefix_list: f'delete policy-options policy-statement {policy.name} term {term} from prefix-list {prefix_list}',
    PolicyFeatures.FROM_PREFIX_LIST_FILTER: lambda policy, term, prefix_list, match_type: f'delete policy-options policy-statement {policy.name} term {term} from prefix-list-filter {prefix_list} {match_type}',
    PolicyFeatures.FROM_PROTOCOL: lambda policy, term, protocol: f'delete policy-options policy-statement {policy.name} term {term} from protocol {protocol}',
    PolicyFeatures.FROM_RIB: lambda policy, term, rib: f'delete policy-options policy-statement {policy.name} term {term} from rib {rib}',
    PolicyFeatures.FROM_ROUTE_FILTER: lambda policy, term, net, match_type: f'delete policy-options policy-statement {policy.name} term {term} from route-filter {int_to_ip(net.address)}/{net.prefix} {match_type}',
    PolicyFeatures.FROM_ROUTE_TYPE: lambda policy, term, route_type: f'delete policy-options policy-statement {policy.name} term {term} from route-type {route_type}',
    PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER: lambda policy, term, source_filter, match_type: f'delete policy-options policy-statement {policy.name} term {term} from source-address-filter {source_filter} {match_type}',
    PolicyFeatures.FROM_TAG: lambda policy, term, tag: f'delete policy-options policy-statement {policy.name} term {term} from tag {tag}',
    PolicyFeatures.FROM_NEXT_HOP: lambda policy, term, next_hop: f'delete policy-options policy-statement {policy.name} term {term} from next-hop {int_to_ip(next_hop)}',
    PolicyFeatures.TO_LEVEL: lambda: f'',
    PolicyFeatures.TO_RIB: lambda: f'',
    PolicyFeatures.THEN_ACCEPT: lambda policy, term: f'delete policy-options policy-statement {policy.name} term {term} then accept',
    PolicyFeatures.THEN_AS_PATH_EXPAND: lambda policy, term, n: f'delete policy-options policy-statement {policy.name} term {term} then as-path-expand last-as count {n}',
    PolicyFeatures.THEN_AS_PATH_PREPEND: lambda policy, term, as_path: f'delete policy-options policy-statement {policy.name} term {term} then as-path-prepend {as_path}',
    PolicyFeatures.THEN_COLOR: lambda policy, term, add, color: f'delete policy-options policy-statement {policy.name} term {term} then color {add} {color}',
    PolicyFeatures.THEN_COLOR2: lambda policy, term, add, color: f'delete policy-options policy-statement {policy.name} term {term} then color2 {add} {color}',
    PolicyFeatures.THEN_COMMUNITY_ADD: lambda policy, term, community: f'delete policy-options policy-statement {policy.name} term {term} then community add {community}',
    PolicyFeatures.THEN_COMMUNITY_DELETE: lambda policy, term, community: f'delete policy-options policy-statement {policy.name} term {term} then community delete {community}',
    PolicyFeatures.THEN_COMMUNITY_SET: lambda policy, term, community: f'delete policy-options policy-statement {policy.name} term {term} then community set {community}',
    PolicyFeatures.THEN_COS_NEXT_HOP_MAP: lambda policy, term, cos_map: f'delete policy-options policy-statement {policy.name} term {term} then cos-next-hop-map {cos_map}',
    PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT: lambda policy, term: f'delete policy-options policy-statement {policy.name} term {term} then default-action accept',
    PolicyFeatures.THEN_DEFAULT_ACTION_REJECT: lambda policy, term: f'delete policy-options policy-statement {policy.name} term {term} then default-action reject',
    PolicyFeatures.THEN_EXTERNAL: lambda policy, term, metric_type: f'delete policy-options policy-statement {policy.name} term {term} then external type {metric_type}',
    PolicyFeatures.THEN_FORWARDING_CLASS: lambda policy, term, fwd_class: f'delete policy-options policy-statement {policy.name} term {term} then forwarding-class {fwd_class}',
    PolicyFeatures.THEN_INSTALL_NEXTHOP: lambda: f'',
    PolicyFeatures.THEN_LOCAL_PREFERENCE: lambda policy, term, pref: f'delete policy-options policy-statement {policy.name} term {term} then local-preference {pref}',
    PolicyFeatures.THEN_METRIC: lambda policy, term, metric: f'delete policy-options policy-statement {policy.name} term {term} then metric {metric}',
    PolicyFeatures.THEN_METRIC_ADD: lambda policy, term, metric: f'delete policy-options policy-statement {policy.name} term {term} then metric add {metric}',
    PolicyFeatures.THEN_METRIC_EXPRESSION: lambda: f'',
    PolicyFeatures.THEN_METRIC_IGP: lambda policy, term, offset: f'delete policy-options policy-statement {policy.name} term {term} then metric igp {offset}',
    PolicyFeatures.THEN_METRIC2: lambda policy, term, metric: f'delete policy-options policy-statement {policy.name} term {term} then metric2 {metric}',
    PolicyFeatures.THEN_METRIC2_EXPRESSION: lambda: f'',
    PolicyFeatures.THEN_NEXT_HOP: lambda policy, term, next_hop: f'delete policy-options policy-statement {policy.name} term {term} then next-hop {int_to_ip(next_hop)}',
    PolicyFeatures.THEN_NEXT_HOP_SELF: lambda policy, term: f'delete policy-options policy-statement {policy.name} term {term} then next-hop self',
    PolicyFeatures.THEN_NEXT_POLICY: lambda: f'',
    PolicyFeatures.THEN_NEXT_TERM: lambda: f'',
    PolicyFeatures.THEN_ORIGIN: lambda policy, term, origin: f'delete policy-options policy-statement {policy.name} term {term} then origin {origin}',
    PolicyFeatures.THEN_PREFERENCE: lambda policy, term, pref: f'delete policy-options policy-statement {policy.name} term {term} then preference {pref}',
    PolicyFeatures.THEN_PRIORITY: lambda policy, term, priority: f'delete policy-options policy-statement {policy.name} term {term} then priority {priority}',
    PolicyFeatures.THEN_REJECT: lambda policy, term: f'delete policy-options policy-statement {policy.name} term {term} then reject',
    PolicyFeatures.THEN_TAG: lambda policy, term, tag: f'delete policy-options policy-statement {policy.name} term {term} then tag {tag}',

    PolicyFeatures.POLICY_MATCH_FEATURE_BGP_OUT: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args),
    PolicyFeatures.POLICY_MATCH_FEATURE_BGP_IN: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args),
    PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_OUT: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args),
    PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_IN: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_BGP_OUT: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_BGP_IN: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_OSPF_OUT: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args),
    PolicyFeatures.POLICY_SET_FEATURE_OSPF_IN: lambda policy, term, feature, *args: feature_disable[feature](policy, term, *args)
}


def config_mode(router, feature, arg):
    return ()


def exit_config_mode(feature):
    return []


def generate_maps_lists_config(router):
    config = []

    for as_path in router.as_path_lists:
        config.append(f'set policy-options as-path {as_path.name} {as_path.regex}')

    for community in router.comm_lists:
        config.append(f'set policy-options community {community.name} members [{",".join(community.comms)}]')

    for prefix_list in router.prefix_lists:
        for seq in prefix_list.prefix:
            net = prefix_list.prefix[seq]
            config.append(f'set policy-options prefix-list {prefix_list.name} {int_to_ip(net.address)}/{net.prefix}')

    for policy in router.ospf_in_route_maps:
        config.append(f'set policy-options policy-statement {policy.name} then accept')

    for policy in router.ospf_out_route_maps:
        config.append(f'set policy-options policy-statement {policy.name} then accept')

    for policy in router.bgp_in_route_maps:
        config.append(f'set policy-options policy-statement {policy.name} then accept')

    for policy in router.bgp_out_route_maps:
        config.append(f'set policy-options policy-statement {policy.name} then accept')

    return config


def generate_bgp_config(router):
    config = [
        f'set routing-options autonomous-system {router.AS.num}',
        f'set routing-options router-id {int_to_ip(router.router_id)}',
        f'set protocols bgp group IBGP type internal',
        f'set protocols bgp group IBGP local-address {int_to_ip(router.router_id)}',
        f'set protocols bgp group EBGP type external'
    ]

    for neighbour in router.bgp_neighbours:
        if neighbour.AS == router.AS:
            config.append(f'set protocols bgp group {neighbour.group} neighbor {int_to_ip(neighbour.address)}')
        else:
            config.append(
                f'set protocols bgp group {neighbour.group} neighbor {int_to_ip(neighbour.address)} peer-as {neighbour.AS.num}')

    return config


def get_base_config(router):
    config = [
        f'set system host-name {router.name}',
        f'set interfaces lo0.0 family inet address {int_to_ip(router.router_id)}/32'
    ]

    for interface in router.interfaces:
        if interface.address is not None:
            config.append(f'set interfaces {interface.name} family inet address '
                          f'{int_to_ip(interface.address)}/{interface.prefix}')
        if interface.area is not None:
            config.append(f'set protocols ospf area {interface.area} interface {interface.name}')

    for network, interface in router.fixed_static_routes:
        config.append(f'set routing-options static route {int_to_ip(network.address)}/{network.prefix} next-hop {interface.name}')

    for area in router.ospf_areas:
        if area.type == OSPF_Area_Type.STUB:
            config.append(f'set protocols ospf area {area} stub')
        elif area.type == OSPF_Area_Type.NSSA:
            config.append(f'set protocols ospf area {area} nssa')

    for protocol in ['direct', 'static', 'ospf', 'bgp']:
        config.append(f'set policy-options policy-statement send-{protocol} term 1 from protocol {protocol}')
        config.append(f'set policy-options policy-statement send-{protocol} term 1 then accept')

    if Protocols.BGP in router.enabled_protocols:
        config.append(f'set protocols bgp hold-time 3')
        config.extend(generate_bgp_config(router))

    config.extend(generate_maps_lists_config(router))

    return config


def write_config(router, path):
    config = get_base_config(router)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(f'{path}{router.name}.set', 'w') as f:
        f.write('\n'.join(config))
