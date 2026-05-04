"""
Network Compliance Auditor Starter Template
Follow the modules to fill in the functions. The reference is in ../reference/audit.py if you get stuck
"""

import re
import yaml

def load_inventory(path):
    #Module 1: Load device inventory from YAML.
    #Open the file, parse YAML, return the devices list.
    pass

def load_policy(path):
    #Module 1: Load compliance policy from YAML.
    #Open the file, parse YAML, return the full dict
    pass

def load_config(device):
    #Module 2: Read a devices config file as a string
    pass

def search_config(config, pattern, match_type="exact"):
    #Module 3: Search a config for a pattern. Return True if found
    pass

def rule_applies(rule, device):
    #Module 4: Determine if a rull should apply against a given device
    #Return True if no applies_to, otherwise check each key/value
    pass


def check_config_contains(rule, config):
    #Module 4: PASS if pattern found in config
    pass

def check_config_not_contains(rule, config):
    #Module 4: Pass if pattern is absent from config
    pass

def check_every_int(rule, config):
    #Module 4: PASS if every interface block has the required field
    pass

def parse_interfaces(config):
    #Module 4: Parse Cisco config into a dict of interface blocks
    pass

rule_handler = {
    #Module 4: Map rule type strings to handler fuctions
}

def evaluate_rule(rule, config):
    #Module 4: Look up the right handler and call it
    pass

def run_audit(inventory, policy):
    #Module 5: Run every rule against every device and collect results
    pass

def print_report(results, policy):
    #Module 6: Render results as a colorized table
    pass

def main():
    inventory = load_inventory("reference/inventory.yaml")
    policy = load_policy("reference/policy.yaml")
    results = run_audit(inventory, policy)
    print_report(results, policy)

if __name__ == "__main__":
    main()