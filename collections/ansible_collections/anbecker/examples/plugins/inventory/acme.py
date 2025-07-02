from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
    name: acme
    plugin_type: inventory
    short_description: Static inventory of hosts grouped by even/odd numbers
    description:
        - Generates a configurable static inventory with hosts
        - Groups hosts into 'evens' and 'odds' based on host number
    extends_documentation_fragment:
        - constructed
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['anbecker.examples.acme']
        host_count:
            description: Number of hosts to generate
            type: int
            default: 10
        domain:
            description: Domain name to use for host names
            type: str
            default: example.com
    author:
        - "Ansible Adoption Examples"
'''

EXAMPLES = '''
    # Example configuration file (acme.yml)
    plugin: anbecker.examples.acme
    host_count: 5
    domain: mycompany.com
'''

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleParserError

class InventoryModule(BaseInventoryPlugin):
    NAME = 'anbecker.examples.acme'  # fully qualified collection name

    def verify_file(self, path):
        """Return true/false if this is possibly a valid file for this plugin to consume"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # Base class verifies that file exists and is readable
            if path.endswith(('yaml', 'yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory source"""
        # Initialize inventory plugin
        super(InventoryModule, self).parse(inventory, loader, path)
        
        # Store reference to inventory object
        self.inventory = inventory
        
        # Read the config data from YAML source
        self._read_config_data(path)
        
        try:
            # Get configured parameters with defaults
            host_count = self.get_option('host_count')
            if host_count is None:
                host_count = 10
            domain = self.get_option('domain')
            if domain is None:
                domain = 'example.com'
            
            # Set up groups
            group_evens = 'evens'
            group_odds = 'odds'
            
            # Add groups
            self.inventory.add_group(group_evens)
            self.inventory.add_group(group_odds)

            # Add hosts and assign to groups
            for i in range(1, int(host_count) + 1):
                hostname = f"host{i}.{domain}"
                
                # Add host to inventory
                self.inventory.add_host(hostname)
                
                # Add host_number variable
                self.inventory.set_variable(hostname, 'host_number', i)
                
                # Add to appropriate group based on number
                group = group_evens if i % 2 == 0 else group_odds
                self.inventory.add_child(group, hostname)
        except Exception as e:
            raise AnsibleParserError(
                'All correct options required: {}'.format(e))
