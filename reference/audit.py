""" 
Network Compliance Auditor

audit.py reads an inventory file of network devices and a policy file. Both files are formatted in YAML. This script then evaluates if each device is compliant with the policy and responds with a pass or fail.else
"""

import yaml
import re
from rich.console import Console
from rich.table import Table

def load_inventory(path):
    "Loads the inventory YAML file then returns the list of inventory"
    with open(path) as f:
        data = yaml.safe_load(f)
    return data["devices"]

def load_policy(path):
    "Loads the policty YAML file then returns the policy"
    with open(path) as f:
        data = yaml.safe_load(f)
    return data

def load_config(device):
    "Loads the device configs"
    with open(device["config_path"]) as f:
        data = f.read()
    return data

def search_config(config, pattern, match_type="exact"):
    #Search the config for a pattern, returns TRUE if found.
    if match_type == "regex":
        return re.search(pattern, config) is not None
    else:
        return pattern in config

def rule_applied(rule, device):
    "Returns True if the fule should run against the device"
    "A rule with no 'applies_to' field runs globally."
    "A rule with 'applies_to' field runs only when every value matches the corresponding field for the device"
    if "applies_to" not in rule:
        return True
    
    for key, value in rule["applies_to"].items():
        if device.get(key) != value:
            return False
    
    return True

def check_config_contains(rule, config):
    "PASS if pattern is found in the config, FAIL if not found"
    pattern = rule["pattern"]
    match_type = rule.get("match_type", "exact")
    found = search_config(config, pattern, match_type)

    if found:
        return ("PASS", f"Found pattern: {pattern}")
    else:
        return ("FAIL", f"Pattern not found: {pattern}")
    
def check_config_not_contains(rule, config):
    "PASS if pattern is not found in the config, FAIL if found"
    pattern = rule["pattern"]
    match_type = rule.get("match_type", "exact")
    found = search_config(config, pattern, match_type)

    if found:
        return ("FAIL", f"Bad pattern found: {pattern}")
    else:
        return ("PASS", f"Pattern absent: {pattern}")

def check_every_int(rule, config):
    "PASS only if every interface block in the config contains the required fields. FAIL if missing the fields"
    field = rule["field"]
    interfaces = parse_interfaces(config)

    if not interfaces:
        return ("PASS", "No interfaces found in config")
    
    missing = []
    for iface_name, iface_lines in interfaces.items():
        if not any(field in line for line in iface_lines):
            missing.append(iface_name)

    if missing:
        return ("FAIL", f"Missing '{field}' on {', '.join(missing)}")
    else:
        return ("PASS", f"All {len(interfaces)} interfaces have '{field}'")
    
def parse_interfaces(config):
    "Goes through a Cisco style config"
    interfaces = {}
    current_iface = None

    for line in config.splitlines():
        if line.startswith("interface "):
            current_iface = line.strip()
            interfaces[current_iface] = []
        elif current_iface is not None:
            if line.startswith(" ") or line.startswith("\t"):
                interfaces[current_iface].append(line.strip())
            else:
                current_iface = None

    return interfaces


rule_handler = {
    "config_contains": check_config_contains,
    "config_not_contains": check_config_not_contains,
    "every_interface_has": check_every_int,
}

def evaluate_rule(rule, config):
    #Looks at the handlers for the rule and calls it
    handler = rule_handler.get(rule["type"])
    if handler is None:
        return ("FAIL", f"Unknown rule type: {rule['type']}")
    return handler(rule, config)

def run_audit(inventory, policy):
    #Evaluates or skips, then records, the rules for each device
    results = []

    for device in inventory:
        try:
            config = load_config(device)
        except FileNotFoundError:
            for rule in policy["rules"]:
                results.append({
                    "device": device["name"],
                    "rule_id": rule["id"],
                    "severity": rule["severity"],
                    "status": "ERROR",
                    "reason": f"Config file not found: {device['config_path']}",
                })
            continue
        
        for rule in policy["rules"]:
            if not rule_applied(rule, device):
                results.append({
                    "device": device["name"],
                    "rule_id": rule["id"],
                    "severity": rule["severity"],
                    "status": "N/A",
                    "reason": "Rule does not apply to this device",
                })
                continue

            status, reason = evaluate_rule(rule, config)
            results.append({
                "device": device["name"],
                "rule_id": rule["id"],
                "severity": rule["severity"],
                "status": status,
                "reason": reason,
            })
    return results

status_styles = {
    "PASS": "green",
    "FAIL": "red",
    "N/A": "dim",
    "ERROR": "yellow",
}

def print_report(results, policy):
    "Displays a colored table to show results in terminal"
    console = Console()

    meta = policy["metadata"]
    console.print()
    console.print(f"[bold]Network Compliance Report [/bold]")
    console.print(f"Policy: {meta['name']} v{meta['version']}")
    console.print(f"Author: {meta['author']}")
    console.print()

    table = Table(show_lines=False)
    table.add_column("Device", style="cyan", no_wrap=True)
    table.add_column("Rule ID", no_wrap=True)
    table.add_column("Severity", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Reason")

    for r in results:
        style = status_styles.get(r["status"], "white")
        table.add_row(
            r["device"],
            r["rule_id"],
            r["severity"].upper(),
            f"[{style}]{r['status']}[/{style}]",
            r["reason"],
        )

    console.print(table)

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "N/A")
    errored = sum(1 for r in results if r["status"] == "ERROR")

    console.print()
    console.print(f"[bold]Summary:[/bold] {total} checks - "
                  f"[green]{passed} pass[/green], "
                  f"[red]{failed} fail[/red], "
                  f"[dim]{skipped} skipped[/dim], "
                  f"[yellow]{errored} errored[/yellow]")
    console.print()

def main():
    inventory = load_inventory("reference/inventory.yaml")
    policy = load_policy("reference/policy.yaml")
    results = run_audit(inventory, policy)
    print_report(results, policy)

if __name__ == "__main__":
    main()