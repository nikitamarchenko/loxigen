# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.

"""
@brief Show function generation

Generates show function files.

"""

import sys
import c_gen.of_g_legacy as of_g
import c_gen.match as match
import c_gen.flags as flags
from generic_utils import *
import c_gen.type_maps as type_maps
import loxi_utils.loxi_utils as loxi_utils
import c_gen.loxi_utils_legacy as loxi_utils
import c_gen.identifiers as identifiers
from c_test_gen import var_name_map

show_override = {
    ('uint32_t', 'arp_tpa'): 'ipv4',
    ('uint32_t', 'arp_spa'): 'ipv4',
    ('uint32_t', 'nw_addr'): 'ipv4',
    ('uint32_t', 'dst'): 'ipv4',
}

show_hex = set([
    ('uint8_t', 'icmpv6_code'),
    ('uint8_t', 'mpls_tc'),
    ('uint16_t', 'eth_type'),
    ('uint8_t', 'ip_dscp'),
    ('uint64_t', 'metadata'),
    ('uint16_t', 'ingress_tpid'),
    ('uint16_t', 'egress_tpid'),
    ('uint32_t', 'xid'),
    ('uint16_t', 'flags'),
    ('uint32_t', 'experimenter'),
    ('uint32_t', 'mask'),
    ('uint8_t', 'report_mirror_ports'),
    ('uint64_t', 'datapath_id'),
    ('uint32_t', 'capabilities'),
    ('uint32_t', 'actions'),
    ('uint64_t', 'cookie'),
    ('uint8_t', 'reason'),
    ('uint32_t', 'role'),
    ('uint32_t', 'config'),
    ('uint32_t', 'advertise'),
    ('uint32_t', 'advertised'),
    ('uint32_t', 'supported'),
    ('uint32_t', 'peer'),
    ('uint64_t', 'cookie_mask'),
    ('uint32_t', 'reserved'),
    ('uint16_t', 'ethertype'),
    ('uint64_t', 'metadata_mask'),
    ('uint32_t', 'instructions'),
    ('uint32_t', 'write_actions'),
    ('uint32_t', 'apply_actions'),
    ('uint32_t', 'types'),
    ('uint32_t', 'actions_all'),
    ('uint32_t', 'actions_select'),
    ('uint32_t', 'actions_indirect'),
    ('uint32_t', 'actions_ff'),
    ('uint64_t', 'generation_id'),
    ('uint16_t', 'value_mask'),
    ('uint32_t', 'value_mask'),
    ('uint32_t', 'oxm_header'),
    ('uint8_t', 'value_mask'),
    ('uint64_t', 'value_mask'),
    ('uint64_t', 'write_setfields'),
    ('uint64_t', 'apply_setfields'),
    ('uint64_t', 'metadata_match'),
    ('uint64_t', 'metadata_write'),
    ('uint32_t', 'packet_in_mask_equal_master'),
    ('uint32_t', 'packet_in_mask_slave'),
    ('uint32_t', 'port_status_mask_equal_master'),
    ('uint32_t', 'port_status_mask_slave'),
    ('uint32_t', 'flow_removed_mask_equal_master'),
    ('uint32_t', 'flow_removed_mask_slave'),
    ('uint32_t', 'band_types'),
    ('uint16_t', 'bsn_tcp_flags'),
])

def gen_emitter(cls, m_name, m_type):
    if (m_type, m_name) in show_override:
        short_type = show_override[(m_type, m_name)]
    elif (m_type, m_name) in show_hex:
        short_type = loxi_utils.type_to_short_name(m_type).replace('u', 'x')
    else:
        short_type = loxi_utils.type_to_short_name(m_type)
    return "LOCI_SHOW_" + short_type;

def gen_obj_show_h(out, name):
    loxi_utils.gen_c_copy_license(out)
    out.write("""
/**
 *
 * AUTOMATICALLY GENERATED FILE.  Edits will be lost on regen.
 *
 * Header file for object showing.
 */

/**
 * Show  object declarations
 *
 * Routines that emit a human-readable dump of each object.
 *
 */

#if !defined(_LOCI_OBJ_SHOW_H_)
#define _LOCI_OBJ_SHOW_H_

#include <loci/loci.h>
#include <stdio.h>

/* g++ requires this to pick up PRI, etc.
 * See  http://gcc.gnu.org/ml/gcc-help/2006-10/msg00223.html
 */
#if !defined(__STDC_FORMAT_MACROS)
#define __STDC_FORMAT_MACROS
#endif
#include <inttypes.h>


/**
 * Show any OF object.
 */
int of_object_show(loci_writer_f writer, void* cookie, of_object_t* obj);






""")

    for version in of_g.of_version_range:
        for cls in of_g.standard_class_order:
            if not loxi_utils.class_in_version(cls, version):
                continue
            if cls in type_maps.inheritance_map:
                continue
            out.write("""\
int %(cls)s_%(ver_name)s_show(loci_writer_f writer, void* cookie, %(cls)s_t *obj);
""" % dict(cls=cls, ver_name=loxi_utils.version_to_name(version)))

    out.write("""
#endif /* _LOCI_OBJ_SHOW_H_ */
""")

def gen_obj_show_c(out, name):
    loxi_utils.gen_c_copy_license(out)
    out.write("""
/**
 *
 * AUTOMATICALLY GENERATED FILE.  Edits will be lost on regen.
 *
 * Source file for object showing.
 *
 */

#define DISABLE_WARN_UNUSED_RESULT
#include <loci/loci.h>
#include <loci/loci_show.h>
#include <loci/loci_obj_show.h>

static int
unknown_show(loci_writer_f writer, void* cookie, of_object_t *obj)
{
    return writer(cookie, "Unable to print object of type %d, version %d\\n",
                         obj->object_id, obj->version);
}
""")

    for version in of_g.of_version_range:
        ver_name = loxi_utils.version_to_name(version)
        for cls in of_g.standard_class_order:
            if not loxi_utils.class_in_version(cls, version):
                continue
            if cls in type_maps.inheritance_map:
                continue
            out.write("""
int
%(cls)s_%(ver_name)s_show(loci_writer_f writer, void* cookie, %(cls)s_t *obj)
{
    int out = 0;
""" % dict(cls=cls, ver_name=ver_name))

            members, member_types = loxi_utils.all_member_types_get(cls, version)
            for m_type in member_types:
                if loxi_utils.type_is_scalar(m_type) or m_type in \
                        ["of_match_t", "of_octets_t"]:
                    # Declare instance of these
                    out.write("    %s %s;\n" % (m_type, var_name_map(m_type)))
                else:
                    out.write("""
    %(m_type)s %(v_name)s;
"""  % dict(m_type=m_type, v_name=var_name_map(m_type)))
                    if loxi_utils.class_is_list(m_type):
                        base_type = loxi_utils.list_to_entry_type(m_type)
                        out.write("    %s elt;\n    int rv;\n" % base_type)
            for member in members:
                m_type = member["m_type"]
                m_name = member["name"]
                emitter = gen_emitter(cls, m_name, m_type)
                if loxi_utils.skip_member_name(m_name):
                    continue
                if (loxi_utils.type_is_scalar(m_type) or
                    m_type in ["of_match_t", "of_octets_t"]):
                    out.write("""
    %(cls)s_%(m_name)s_get(obj, &%(v_name)s);
    out += writer(cookie, "%(m_name)s=");
    out += %(emitter)s(writer, cookie, %(v_name)s);
    out += writer(cookie, " ");
""" % dict(cls=cls, m_name=m_name, m_type=m_type,
           v_name=var_name_map(m_type), emitter=emitter))
                elif loxi_utils.class_is_list(m_type):
                    sub_cls = m_type[:-2] # Trim _t
                    elt_type = loxi_utils.list_to_entry_type(m_type)
                    out.write("""
    out += writer(cookie, "%(elt_type)s={ ");
    %(cls)s_%(m_name)s_bind(obj, &%(v_name)s);
    %(u_type)s_ITER(&%(v_name)s, &elt, rv) {
        of_object_show(writer, cookie, (of_object_t *)&elt);
    }
    out += writer(cookie, "} ");
""" % dict(sub_cls=sub_cls, u_type=sub_cls.upper(), v_name=var_name_map(m_type),
           elt_type=elt_type, cls=cls, m_name=m_name, m_type=m_type))
                else:
                    sub_cls = m_type[:-2] # Trim _t
                    out.write("""
    %(cls)s_%(m_name)s_bind(obj, &%(v_name)s);
    out += %(sub_cls)s_%(ver_name)s_show(writer, cookie, &%(v_name)s);
""" % dict(cls=cls, sub_cls=sub_cls, m_name=m_name,
           v_name=var_name_map(m_type), ver_name=ver_name))

            out.write("""
    return out;
}
""")
    out.write("""
/**
 * Log a match entry
 */
int
loci_show_match(loci_writer_f writer, void* cookie, of_match_t *match)
{
    int out = 0;
""")

    for key, entry in match.of_match_members.items():
        m_type = entry["m_type"]
        emitter = gen_emitter('of_match', key, m_type)
        out.write("""
    if (OF_MATCH_MASK_%(ku)s_ACTIVE_TEST(match)) {
        out += writer(cookie, "%(key)s active=");
        out += %(emitter)s(writer, cookie, match->fields.%(key)s);
        out += writer(cookie, "/");
        out += %(emitter)s(writer, cookie, match->masks.%(key)s);
        out += writer(cookie, " ");
    }
""" % dict(key=key, ku=key.upper(), emitter=emitter, m_type=m_type))

    out.write("""
    return out;
}
""")

    # Generate big table indexed by version and object
    for version in of_g.of_version_range:
        out.write("""
static const loci_obj_show_f show_funs_v%(version)s[OF_OBJECT_COUNT] = {
""" % dict(version=version))
        out.write("    unknown_show, /* of_object, not a valid specific type */\n")
        for j, cls in enumerate(of_g.all_class_order):
            comma = ""
            if j < len(of_g.all_class_order) - 1: # Avoid ultimate comma
                comma = ","

            if (not loxi_utils.class_in_version(cls, version) or
                    cls in type_maps.inheritance_map):
                out.write("    unknown_show%s\n" % comma);
            else:
                out.write("    %s_%s_show%s\n" %
                          (cls, loxi_utils.version_to_name(version), comma))
        out.write("};\n\n")

    out.write("""
static const loci_obj_show_f *const show_funs[5] = {
    NULL,
    show_funs_v1,
    show_funs_v2,
    show_funs_v3,
    show_funs_v4
};

int
of_object_show(loci_writer_f writer, void* cookie, of_object_t *obj)
{
    if ((obj->object_id > 0) && (obj->object_id < OF_OBJECT_COUNT)) {
        if (((obj)->version > 0) && ((obj)->version <= OF_VERSION_1_2)) {
            /* @fixme VERSION */
            return show_funs[obj->version][obj->object_id](writer, cookie, (of_object_t *)obj);
        } else {
            return writer(cookie, "Bad version %d\\n", obj->version);
        }
    }
    return writer(cookie, "Bad object id %d\\n", obj->object_id);
}
""")

