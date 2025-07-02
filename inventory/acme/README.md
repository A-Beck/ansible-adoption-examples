# ACME Inventory Configuration

This directory contains the configuration for the ACME inventory plugin, which generates a dynamic inventory of hosts grouped by even and odd numbers.

## Configuration File

The `hosts.yml` file contains the following configuration:

```yaml
plugin: anbecker.examples.acme
host_count: 15
domain: acme-corp.com
```

### Parameters

- `plugin`: The name of the inventory plugin to use (required)
- `host_count`: Number of hosts to generate (optional, default: 10)
- `domain`: Domain name to use for the hosts (optional, default: example.com)

## Usage

To test the inventory configuration:

```bash
ansible-inventory -i inventory/acme/hosts.yml --list
```

To use this inventory with a playbook:

```bash
ansible-playbook -i inventory/acme/hosts.yml my_playbook.yml
```

## Generated Groups

The plugin will create two groups:
- `evens`: Contains hosts with even numbers (host2, host4, etc.)
- `odds`: Contains hosts with odd numbers (host1, host3, etc.) 