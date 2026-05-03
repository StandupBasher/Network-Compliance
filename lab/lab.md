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

