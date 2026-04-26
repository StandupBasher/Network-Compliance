import yaml

with open("reference/inventory.yaml") as f:
    inventory = yaml.safe_load(f)

with open("reference/policy.yaml") as f:
    policy = yaml.safe_load(f)