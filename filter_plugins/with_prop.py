from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from string import Template

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.plugins.filter.json_query import json_query
from jinja2 import filters, contextfilter
# - name: Gather Nodes with property 'xxx_installed' == true
#   set_fact:
#     xxx_nodes: '{{ hostvars.values() | json_query("[*].{id: inventory_hostname, x_prop: xxx_installed}")
#                       | selectattr("x_prop", "equalto", true)
#                       | list | json_query("[*].id") }}'



@contextfilter
def keys_of_prop(a, obj_list, id_prop, prop, val):
    # get a simple list
    make_simple_list = json_query(obj_list, "[*].{id: %s, x_prop: %s}" % (id_prop, prop))
    select = filters.do_selectattr(a, make_simple_list, "x_prop", "equalto", val)
    new_list = filters.do_list(select)
    result = json_query(new_list, "[*].id")
    return result

@contextfilter
def hosts_with(a, hostvars, prop, val):
    return keys_of_prop(a, hostvars.values(), id_prop='inventory_hostname', prop=prop, val=val)


def lines_of_items(obj_list, template, obj_break = '\n'):
    _tmpl = Template(template)
    obj_lines=[]
    for obj in obj_list:
        obj_line = _tmpl.substitute(obj)
        obj_lines.append(obj_line)
    return obj_break.join(obj_lines)

# ---- Ansible filters ----
class FilterModule(object):
    ''' By Prop filter '''

    def filters(self):
        return {
            'keys_of_prop': keys_of_prop,
            'hosts_with': hosts_with,
            'lines_of_items': lines_of_items,
        }
