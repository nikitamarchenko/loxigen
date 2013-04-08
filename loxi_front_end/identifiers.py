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

##
# @brief Process identifiers for updating of_g.identifiers
#

import sys
import of_h_utils
from generic_utils import *
import of_g

##
# The value to use when an identifier is not defined for a version
UNDEFINED_IDENT_VALUE = 0

def add_identifiers(all_idents, idents_by_group, version, contents):
    """
    Update all_idents with identifiers from an openflow.h header file
    @param all_idents A dict, usually of_g.identifiers
    @param idents_by_group A dict for mapping LOXI idents to groups,
    usually of_g.identifiers_by_group
    @param version The OF wire version
    @param contents The contents of an openflow.h file
    """

    # Get the dictionary of enums from the file text
    enum_dict = of_h_utils.get_enum_dict(version,
                                         contents)
    for name, info in enum_dict.items():
        add_identifier(name, info.ofp_name, info.ofp_group, info.value,
                       version, all_idents, idents_by_group)

def add_identifier(name, ofp_name, ofp_group, value, version, all_idents, idents_by_group):
    if name in all_idents:
        all_idents[name]["values_by_version"][version] = value
        if ((all_idents[name]["ofp_name"] != ofp_name or
            all_idents[name]["ofp_group"] != ofp_group) and
            ofp_name.find("OFPP_") != 0):
            log("""
NOTE: Identifier %s has different ofp name or group in version %s
From ofp name %s, group %s to name %s, group %s.
This could indicate a name collision in LOXI identifier translation.
""" % (name, str(version), all_idents[name]["ofp_name"],
    all_idents[name]["ofp_group"], ofp_name, ofp_group))
            # Update stuff assuming newer versions processed later
            all_idents[name]["ofp_name"] = ofp_name
            all_idents[name]["ofp_group"] = ofp_group

    else: # New name
        all_idents[name] = dict(
            values_by_version = {version:value},
            common_value = value,
            ofp_name = ofp_name,
            ofp_group = ofp_group
            )
        if ofp_group not in idents_by_group:
            idents_by_group[ofp_group] = []
        if name not in idents_by_group[ofp_group]:
            idents_by_group[ofp_group].append(name)

def all_versions_agree(all_idents, version_list, name):
    val_list = all_idents[name]["values_by_version"]
    for version in version_list:
        if not version in val_list:
            return False
        if str(val_list[version]) != str(all_idents[name]["common_value"]):
            return False
    return True

def defined_versions_agree(all_idents, version_list, name):
    val_list = all_idents[name]["values_by_version"]
    for version in version_list:
        if version in val_list:
            if str(val_list[version]) != str(all_idents[name]["common_value"]):
                return False
    return True
