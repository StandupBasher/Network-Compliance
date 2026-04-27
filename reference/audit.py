import yaml

def load_inventory(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return data["devices"]

def load_policy(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return data

def load_config(device):
    with open(device["config_path"]) as f:
        data = f.read()
    return data

if __name__ == "__main__":
    inventory = load_inventory("reference/inventory.yaml")
    policy = load_policy("reference/policy.yaml")
    print(f"Loaded {len(inventory)} devices")
    print(f"Loaded policy: {policy['metadata']['name']} v{policy['metadata']['version']}")
    print(f"Loaded {len(policy['rules'])} rules")

    first_device = inventory[0]
    config = load_config(first_device)
    print(f"\nConfig for {first_device['name']}: {len(config)} characters")
    print("First 200 chars:")
    print(config[:200])