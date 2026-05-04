# Network Compliance Auditor

**Author:** Wael Shahadeh  
**Version:** 1.0.0  

---

## About This Lab

This lab introduces network engineers to Python by having them build a working network compliance auditor. There is reference/audit.py as a guide to what a functional Python program looks like, and starter/audit.py, which provides a skeleton script for the engineer learning Python to build. Work in starter/audit.py and only use reference/audit.py if you get stuck. This guide lists instructions on how to get started with Python and basic usage, teaching how to build a functional audit.py.

The architecture diagram can be found in ../report/architecture.png

# Module 0: Setup and Prerequisites

- You would need an Integrated Development Enviornment (IDE) of your choosing. An IDE is a piece of software that allows you to write, test, and debug code. I recommend Visual Studio Code, which you can download [here](https://code.visualstudio.com/).
  - There are several extensions which make coding in Python within VSCode for this lab more friendly. Press Ctrl (or Command in macOS) + shift + x to open the extension menu.
    - Gitlens
    - indent-rainbow
    - Python
    - Ruff
    - Yaml

- The software Git is a very useful tool for code management. You can install it [here](https://git-scm.com/install/)
    - Once Git is installed, restart Visual Studio Code.
    - On the welcome page of Visual Studio Code, there will be the option to clone a repository. Click that, sign into GitHub (or make an account), and paste the URL of this repository into the search bar and press enter to clone (making a copy) of this repository for you to own locally on your device. Save into whichever folder of choice.
 
- This program and lab uses Python 3.10 or later, which you can download [here](https://www.python.org/downloads/).
  - Ensure that when you are going through the installer, you select the " Add to Path " option.
  - Once Python is installed, restart Visual Studio Code.
  - On the top panel of Visual Studio Code, there will be a terminal option.
    - Open a terminal and type `pip install -r requirements.txt`
    - This opens requirements.txt and installs any external libraries this program uses. This lab in particular uses pyyaml and rich, which allow us to read and utilize files in a YAML format and have an elegant terminal output.

Congratulations! You are now ready to code in Python and learn from this lab!

---

# Module 1: Loading the Inventory

**Objectives:**

- Understand YAML basics
- Use yaml.safe_load
- Write your first Python function with help
- Write your second Python Function on your own
- Work with dicts and lists

**Background**

**What is YAML?**

YAML is a human-readable data serialization standard, with the goal of being easier to read and understand compared to other data structures such as JSON or XML. YAML uses .yaml or .yml file extensions.

In the context of this lab, we are using YAML for the policy list for network devices and the inventory list. The reason we are using an external YAML file instead of hardcoding it into the Python program is that policies and devices change and update. It is relatively easy to break a program, so for the sake of stability, scalability, and maintainability, it would be wise to keep information of that nature in an external file, and just read the data from those files with our Python program.

**YAML has three structural rules:**

1. **Key-value pairs** use a colon followed by a space:
    `name: router1`


2. **Lists** are written with a dash for each item

```yaml
   interfaces:
     - eth0
     - eth1
```

3. **Nested data** uses indentation. Items under a parent must be indented the same amount. Always use spaces and never use tabs:

```yaml
   router1:
     ip: 10.0.0.1
     role: edge
```

**Looking at `reference/inventory.yaml`:**

```yaml
devices:
  - name: router1
    role: edge
    site: DC
    config_path: reference/configs/router1.txt
  - name: router2
    role: core
    site: branch1
    config_path: reference/configs/router2.txt
  - name: switch1
    role: core
    site: branch1
    config_path: reference/configs/switch1.txt
```

Notice the structure of inventory.yaml. A top key is called `devices`, whose value is a list, which is every item starting with `-`. Each device has four fields:
- `name` - Identifier used in reports
- `role` - `core` or `edge`, used later for rule scoping
- `site` - The physical location, also used for rule scoping
- `config_path` - The relative path to the device`s config file

**Writing your first Python function!**

Open `starter/audit.py`. You`ll see this in the first function:

```python
def load_inventory(path):
    #Module 1: Load device inventory from YAML.
    #Open the file, parse YAML, return the devices list.
    pass
```

`def` means to define. We are "defining" a function called `load_inventory` for us to use in our program. Inside the paranthesis, we wrote `path`. This is just a placeholder variable that we can input into our function and manipulate. `pass` means to do nothing. It is so we can make this empty function without Python failing. It will be replaced by actual code.

Each step will have instructions, a description of the goal, and a framework. Try to complete each step on your own. The solution would be right below if you get stuck.

There is not a one answer solution for coding 99% of the time! If your function doesn`t look identical to the solution but is fully operational, that`s good!

---

**Step 1: Safely opening the file**

Python opens files with the `open()` function. The issue is, leaving files open and not in use can cause a resource leak, leading to performance issues. The solution is simple! Python has a `with` statement, which handles opening and closing automatically:

```python
with open(<path>) as <variable>:
  # code that uses the file, we can use pass as a placeholder
  pass
```

**Try it yourself!** Inside the `load_inventory` function, write a with block that opens the inventory file at `path` and names the opened file as `f`. You don`t need to put stuff inside the block yet.

**Solution**
```python
with open(path) as f:
  pass
```

---

**Step 2: YAML parsing**

The pyyaml library has a `yaml.safe_load()` function built in. This opens a YAML file and returns its contents as objects that Python can understand, such as dicts, lists, strings, and numbers.

**Try it yourself!** Inside your `with` block, store the results of `f` into a variable called `data` using `yaml.safe_load()`. You can get rid of the `pass`.

**Solution**

```python
with open(path) as f:
  data = yaml.safe_load(f)
```

---

**Step 3: Return a device list**

`data` now holds parsed YAML. Looking at inventory.yaml, its structure is `{"devices": [...]}`. The list of devices is under the `devices` key.

Lets introduce the `return` concept in Python. `return` takes the output of a function and moves that data out of the function and into the rest of your code. A variable is a name that points to a specific spot in memory. 

**Question:** Should the function return `data`, which is the whole parsed YAML, or `data["devices"]`? Why?

**Answer:** The function should output `data["devices"]` because the caller of `load_inventory` only cares about the device list. They don`t need to know that there is a `devices` key wrapping it. Returning the list directly hides that detail.

**Try it yourself!** Add a `return` statement that gives you back just the lists of devices.

```python
with open(path) as f:
  data = yaml.safe_load(f)
  return data["devices"]
```

That is `load_inventory` complete! 

---

**Now build `load_policy`!**

Using what we learned so far, build `load_policy` so that it reads policy.yaml safely and outputs the needed data!

Hint: `load_policy` should output the full parsed YAML dict, not just a subkey! The caller needs both metadata and rules.

**Testing the function**

Add a test block at the bottom 'starter/audit.py':

```python
if __name__ == "__main__":
    inventory = load_inventory("starter/inventory.yaml")
    print(f"Loaded {len(inventory)} devices")
    for device in inventory:
        print(f"  - {device['name']} ({device['role']}) at {device['site']}")
```

Now run it from the project root or Visual Studio Code terminal:

```python
python starter/audit.py
```

You should see:

```
Loaded 3 devices
  - router1 (edge) at DC
  - switch1 (core) at branch1
  - router2 (core) at branch1
```

If this appears in the terminal, your function works. If you see an error, check:
- Did you save `audit.py` after editing?
- Are you running from project root, and not inside `starter/`?
- Did `pip install -r requirements.txt` complete successfully?

Some common mistakes are using tabs instead of spaces in YAML for indentation. If you use tabs, you'll confuse the parsing. 

If your code gets a `KeyError` with `devices`, it means your YAML doesn't have a top-level named `devices:` key.

---

**Final Tasks for Module 1:**

1. Add a fourth device named `firewall1` to `starter/inventory.yaml` with `role: edge` amd `site: DC`. What does your test output show now?

2. What's the difference between `yaml.safe_load()` and `yaml.load()`? Why should you always use `safe_load`?

3. What does `load_inventory()` return `data["devices"]` instead of just `data`?

---

# Module 2: Loading Device Configs

**Objectives:**

- Read raw text from files
- Understannd when to use raw file reading vs structured parsing
- How to handle missing files
- Pass and use dict data inside a function

**Background**

Module 1 used `yaml.safe_load()` because YAML is structured data. It has keys, lists, and nested objects that cleanly work with Python dicts and lists. A device configuration is different in a sense that it is just text. There is no formal structure with plain text files. Using `yaml.safe_load()` on a non-YAML formatted file would either fail or produce garbage data.

Python has a tool built in for raw text files. `f.read()` returns the entire file's contents as a string, which is what we want. We can then search through that string to find whichever specific data to check for compliance patterns.

**Looking at `reference/config/router1.txt`:**

```
!
! Cisco IOS Configuration
! Device: router1
! Role: edge
! Site: DC
!
hostname router1
!
banner login ^
WARNING: Authorized access only. All activity is monitored and logged.
Unauthorized access is prohibited and will be prosecuted.
^
!
ntp server 10.0.0.100
ntp server 10.0.0.101
!
snmp-server community NetMon-r0 RO
snmp-server location DC-Rack-12
snmp-server contact awesomesauce@example.com
!
ip ssh version 2
!
interface Loopback0
 description Management Loopback
 ip address 10.255.0.1 255.255.255.255
!
```

This is plain text. There are no keys or structures to grab from, just what you would see if you run `show running-config` on a real Cisco device. We want to load it into our program with a function so we can search it later.

**Writing `load_config()`**

Open `starter/audit.py` and  find `load_config()`:

```python
def load_config(device):
    #Module 2: Read a devices config file as a string
    pass
```

Notice how there is a differnce to this function than what we saw in `load_inventory`. We are now using a parameter called `device` instead of `path`. This is because `load_config` receives a whole device dict, which was loaded in from `load_inventory` from Module 1, and the path lives inside that dict.

We will also build `load_config` in three steps.

---

**Step 1: Get the path from the device dict**

When `load_config` is called later, it will pass a device dict that looks like this:

```python
{"name": "router1", "role": "edge", "site": "DC", "config_path": "reference/configs/router1.txt"}
```

You can reach a value in the dict by writing `dict_name["key"]`. SO if your dict is named `device` and you want the value at `"config_path"`, you would write `device["config_path"]`.

**Try it yourself!** Inside `load_config`, write a `with` block that opens the file at the device's config path and names the open file `f`. Use the same pattern as what we learned from Module 1.

**Solution:**

```python
load_config(device):
    with open(device["config_path"]) as f:
      pass
```

---

**Step 2: Read the file's contents**

Python has a build function, `f.read()`, which returns the entire file as a single string. We are using that instead of `yaml.safe_load()` because we are reading an unstructured, regular plain text file.

**Try it yourself!** Inside your `with` block, store the results of `f.read()` in a variable named `data`..

```python
load_config(device):
  with open(device["config_path"]) as f:
    data = f.read()
```

**Step 3: Returning the contents**

We now want to get the config text from `load_config`. Return `data`.

**Try it yourself!** Add a `return statement`

**Solution**

```python
load_config(device):
  with open(device["config_path"]) as f:
    data = f.read()
  return data
```

The `load_config` is now complete! 

---

**Testing `load_config`**

Update your text block of `starter/audit.py`:

```python
if __name__ == "__main__":
    inventory = load_inventory("starter/inventory.yaml")
    first_device = inventory[0]
    config = load_config(first_device)
    print(f"Config for {first_device['name']}: {len(config)} characters")
    print("First 200 chars:")
    print(config[:200])
```

We are doing two special things with this test:

- `inventory[0]` grabs the first item from the device list. Python counting starts at `0` instead of `1`.
- `config[:200]` is string slicing. It grabs the first 200 characters of the string. This is useful for previewing a file without outputting its entire contents.

Run the project the same way we did for Module 1 and you shuold see:

```bash
Config for router1: 961 characters
First 200 chars:
!
! Cisco IOS Configuration
! Device: router1
! Role: edge
! Site: DC
!
hostname router1
!
banner login ^
WARNING: Authorized access only. All activity is monitored and logged.
```

---

What happens if someone removes `router1.txt` and you run the script? Try it out! Rename `router1.txt` to `router1_old.txt` to simulate it being removed and run the script.

You will see:

```bash
FileNotFoundError: [Errno 2] No such file or directory: 'starter/configs/router1.txt'
```

The script crashed! In a real audit, one device with a missing config should not kill the entire audit. We would instead want to record the error and keep going.

Python provides `try/except` for these type of situations:

```python
try:
  # Code that has the possibility of failing
  something_risky()
else SomeErrorType:
  # Instructions if it fails
  # error_handler()
```

We won't add error handling to `load_config` itself, which would complicate the function. Instead, we will add it to our `run_audit` function later, where the error context would matter more.

Rename `router1_old.txt` back to `router1.txt` and confirm the script works again.

---

A common mistake is passing the wrong data type. `load_config` expects a dict, not a string path. If you accidentally call `load_config("configs/router1.txt")`, Python will try to look up `"config_path"` inside the string `"configs/router1.txt"`, which will fail.

Another common mistake is using `yaml.safe_load()` on a config file. The config files aren't YAML, so they won't parse properly.

**A note on using this program in production**

This lab assumes you would have a config file in the correct directory. In a production enviornment, you would pull the configuration over SSH, using another Pyton library like Netmiko. This is beyond the scope of this lab, but is important to mention. The rest of the audit engine does not care about where the config file comes from, so long as it gets its data.

Here is a rough idea of what `load_config` would look like in production. Don't write this in the lab, it is just to represent the usage of Netmiko.

```python
from netmiko import ConnectHandler

def load_config(device):
  connection = ConnectHandler(
    device_type="cisco_ios",
    host=device["host"],
    username=device["username"],
    password=device["password"],
  )
  config = connection.send_command("show running-config")
  connection.disconnect()
  return config
```

---

**Some final questions for Module 2**

1. Why does `load_config` use `f.read()` instead of `yaml.safe_load()`? What would happen if you used `yaml.safe_load()` on a Cisco config file?

2. The function takes a `device` dict, not a path string. Why is that a better design instead of just passing the path?

3. If you wanted to read the config line-by-line, what would you use instead of `f.read()`? When might it be useful?

---

# Module 3: Searching Configs for Patterns

**Objectives:**

- Use Pythons `in` operator for substring matching
- Understand when substring matching isn't enough
- Use the `re` module for regular expression matching
- Write a reusable helper function

**Background**

In Module 2 we loaded a device's config as a single string. Now we need to search that string and find out if specific patterns appear in it. This is part of the core of our audit engine.

1. `in` checks if one string is a substring of another. `in` is exact match only.
2. Regular Expressions (regex) is a flexible pattern-matching langugage. Regex allows you to match patterns like "the word telnet appears anywhere on a line starting with transport input".

**How does `in` work?**

The `in` operator is built into Python and is used between two strings. After comparing the strings, it gives a boolean output, being `True` or `False`. It outputs `True` if the left of the string is in the right of the string. For example:

```python
"hello" in "hello world" #True
"world" in "hello world" #True
"goodbye" in "hello world" #false
"Hello" in "hello world" #false
```

It is case sensitive. This is fine for our goal of Cisco auditing, because Cisco syntax is consistent.

**Regular Expression (regex)**

Sometimes substring matching isn't flexible enough. Lets say there is a rule such as `telnet must not be enabled on VTY lines.` The config might say:

- `transport input telnet` telnet only
- `transport input ssh telnet` both telnet and ssh
- `transport input telnet ssh` both but different order

These three strings are all violations of that rule. A substring check for `transport input telnet` would catch the first two strings, but miss the third. A regex like `transport input.*telnet` catches all three because `.*` means "any characters in between"

Some important regex syntax to know:

- `.` matches any single character
- `.*` matches zero or more of nay character
- `(option1|option2)` matches either option (alternation)
- `^` matches the start of a line
- `$` natches the end of a line

Python's `re` module provides the regex functions we need. We will use `re.search()`, which scans the string for the first match and returns a match object.

```python
import re

re.search("hello", "hello world") #true
re.search("missing", "hello world") #false
re.search("transport input,*telnet", "transport input ssh telnet") #true
```

**Writing `search_config()`**

Open `starter/audit.py` and find `search_config()`:

```python
def search_config(config, pattern, match_type="exact"):
    #Module 3: Search a config for a pattern. Return True if found
    pass
```

Notice how the function has a third parameter, `match_type="exact"`. This means that it will default to exact searches if the user omits that parameter. If the user does need regex, they can select that and the function will still function properly. THis ensures the function works for both simple and complex string searches.

We will build `search_config()` in two steps.

---

**Step 1: Handle exact matching**

When `match_type` is `"exact"`, we use `in`. This would return `True` if `pattern` is in `config`, and `False` if not.

**Try it yourself!** Inside `search_config`, write an `if` statement that checks `match_type`. If it's `"exact"`, return whether `pattern` is in `config`.

**Solution**

```python
def search_config(config, pattern, match_type="exact"):
  if match_type == "exact":
    return pattern in config
```

---

**Step 2: Handle regex matching**

When `match_type` is `"regex"`, we use `re.search()`. The function returns a match object on hit, `None` on miss. We want a boolean, so compare to `None`:

```python
re.search(pattern, config) is not None
```

This ends up being `True` if there is a match, `False` if not.

Make sure `import re` is at the top of your file. Then add an `else` branch for the regex case.

**Try it yourself!** Add an `else` clause to `search_config`. Inside it, return whether `re.search(pattern, config)` is not `None`.

**Solution**
```python
def search_config(config, pattern, match_type="exact"):
  if match_type == "exact":
    return pattern in config
  else:
    return re.search(pattern, config) is not None
```

`search_config` is complete!

---

**Testing `search_config`**

Update your test block with this and run it:

```python
if __name__ == "__main__":
    inventory = load_inventory("starter/inventory.yaml")
    config = load_config(inventory[0])  # router1's config

    # Exact match — should return True
    print("NTP server present:", search_config(config, "ntp server 10.0.0.100"))

    # Exact match — should return False
    print("Public SNMP present:", search_config(config, "snmp-server community public"))

    # Regex match — catches both 'transport input telnet' and 'transport input ssh telnet'
    print("Telnet enabled:", search_config(config, "transport input.*telnet", match_type="regex"))
```

The expected output should be:

```bash
NTP server present: True
Public SNMP present: False
Telnet enabled: False
```

---

A common mistake is when you are working with special characters in regex, like `~!@#$%^&*()` for example. If your pattern contains a special character and you mean it literally, you have to escape it with a backslash. Another common mistake is case sensitivity. You can get around this by sanitizing the input with the `.lower()` function. 

So if:

```python
data = "Hello World"
print(data)
```

Your output would be:

```bash
Hello World
```

If you want to make everything lowercase, you can do this:

```python
data = "Hello World"
lowercasedData = data.lower()
print(lowercasedData)
```

Your output would be:

```bash
hello world
```

---

This function is important because it is reused in Module 4 with `check_config_contains` and `check_config_not_contains` The rule handlers will need this exact logic. Solve the search issue once so it doesn't need to be rebuilt for every function.

---

**Module 3 Question**

1. Why does `search_config` accept a `match_type`  parameter instead of always using regex?

---

# Module 4: The Engine

**Objectives:**

- Build the rule filter (`rule_applies`)
- Write three rule handler functions
- Build a Cisco style config parser
- Use a dispatch table to route rules to their handlers
- Understand why dispatch tables beat long if/elif/else chains

**Background**

This is the heart of the audit tool. We have devices (Module 1), configs (Module 2), and a way to search those configs (Module 3). We will now build the audit engine that takes a rule from `policy.yaml`, decides whether it applies to a given device, and runs the right check.

A rule looks like this:

```yaml
- id: NTP-001
  description: NTP server must be configured
  type: config_contains
  pattern: "ntp server 10.0.0.100"
  match_type: exact
  severity: high
```

Different rules need different evaluation logic. A `config_contains` rule searches for a pattern. A `config_not_contains` rule searches for the absence of a pattern. An `check_every_int` rule parses interface blocks and checks each one. The engine has to dispatch to the right logic based on the rule's `type` field.

We'll build it in five pieces:

1. `rule_applies` Checks if a rule applies to a device
2. `check_config_contains` Handles must contain rules
3. `check_config_not_contains` Handles must not contain rules
4. `parse_interfaces` and `check_every_int` Interface checks
5. The dispatch table and `evaluate_rule` Putting the pieces together

---

**Part 1: Rule applicability**

Some rules apply to every device. Others only apply to specific roles or sites. For example, a "WAN ACL must be present" rule only makes sense for edge routers, not core switches.

Look at this rule, which has an `applies_to` field:

```yaml
- id: WAN-ACL-001
  description: Edge routers must have inbound ACLs
  type: config_contains
  pattern: "ip access-group WAN_IN in"
  severity: critical
  applies_to:
    role: edge
```

This rule should only run on devices where the `role == "edge`. For devices in any other role, it should be skipped.

Open `starter/audit.py` and find rule_applies(rule, device):

```python
def rule_applies(rule, device):
    #Module 4: Determine if a rull should apply against a given device
    #Return True if no applies_to, otherwise check each key/value
    pass
```

---

The logic is:
- If the rule has no `applies_to` field, it applies to everything and will return `True`
- If the rule has an `applies_to` field, every key/value pair in it must match the device's corresponding fields and will return `True` if all match, `False` if any don't

---

**Step 1: Handle the no `applies_to` case**

If `"applies_to"` isn't a key in the rule dict, the rule applies globally. We can check this with the `in` operator:

```python
"applies_to" in role #True if the key exists
"applies_to" not in role #True if the key doesn't exist
```

**Try it yourself!** Inside `rule_applies`, return `True` if `applies_to` is not in `rule`

**Solution**

```python
def rule_applies(rule, device):
  if "applies_to" not in rule:
    return True
```

---

