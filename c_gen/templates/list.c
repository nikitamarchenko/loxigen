:: # Copyright 2014, Big Switch Networks, Inc.
:: #
:: # LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
:: # the following special exception:
:: #
:: # LOXI Exception
:: #
:: # As a special exception to the terms of the EPL, you may distribute libraries
:: # generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
:: # that copyright and licensing notices generated by LoxiGen are not altered or removed
:: # from the LoxiGen Libraries and the notice provided below is (i) included in
:: # the LoxiGen Libraries, if distributed in source code form and (ii) included in any
:: # documentation for the LoxiGen Libraries, if distributed in binary form.
:: #
:: # Notice: "Copyright 2014, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
:: #
:: # You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
:: # a copy of the EPL at:
:: #
:: # http://www.eclipse.org/legal/epl-v10.html
:: #
:: # Unless required by applicable law or agreed to in writing, software
:: # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
:: # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
:: # EPL for the specific language governing permissions and limitations
:: # under the EPL.
::
:: include('_copyright.c')
:: include('_pragmas.c')

#include "loci_log.h"
#include "loci_int.h"

/**
 * Associate an iterator with a list
 * @param list The list to iterate over
 * @param obj The list entry iteration pointer
 * @return OF_ERROR_RANGE if the list is empty (end of list)
 *
 * The obj instance is completely initialized.  The caller is responsible
 * for cleaning up any wire buffers associated with obj before this call
 */

int
${cls}_first(${cls}_t *list, of_list_iter_t iter)
{
    int rv;
    of_object_t *obj = iter.obj;

    ${e_cls}_init(obj, list->version, -1, 1);

    if ((rv = of_list_first(list, obj)) < 0) {
        return rv;
    }

:: if e_uclass.virtual:
    ${e_cls}_wire_object_id_get(obj, &obj->object_id);
:: #endif

:: if wire_length_get != 'NULL':
    ${wire_length_get}(obj, &obj->length);
:: #endif

    return rv;
}

/**
 * Advance an iterator to the next element in a list
 * @param list The list being iterated
 * @param obj The list entry iteration pointer
 * @return OF_ERROR_RANGE if already at the last entry on the list
 *
 */

int
${cls}_next(${cls}_t *list, of_list_iter_t iter)
{
    int rv;
    of_object_t *obj = iter.obj;

    if ((rv = of_list_next(list, obj)) < 0) {
        return rv;
    }

:: if e_uclass.virtual:
    ${e_cls}_wire_object_id_get(obj, &obj->object_id);
:: #endif

:: if wire_length_get != 'NULL':
    ${wire_length_get}(obj, &obj->length);
:: #endif

    return rv;
}

/**
 * Set up to append an object of type ${e_cls} to an ${cls}.
 * @param list The list that is prepared for append
 * @param obj Pointer to object to hold data to append
 *
 * The obj instance is completely initialized.  The caller is responsible
 * for cleaning up any wire buffers associated with obj before this call.
 *
 * See the generic documentation for of_list_append_bind.
 */

int
${cls}_append_bind(${cls}_t *list, of_list_iter_t iter)
{
    return of_list_append_bind(list, iter.obj);
}

/**
 * Append an object to a ${cls} list.
 *
 * This copies data from obj and leaves item untouched.
 *
 * See the generic documentation for of_list_append.
 */

int
${cls}_append(${cls}_t *list, of_list_iter_t iter)
{
    return of_list_append(list, iter.obj);
}