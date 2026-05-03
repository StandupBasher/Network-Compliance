# Network Compliance Auditor

**Author:** Wael Shahadeh  
**Version:** 1.0.0  

---

## About This Lab

This lab introduces network engineers to Python by having them build a working network compliance auditor. There is reference/audit.py as a guide to what a functional Python program looks like, and starter/audit.py, which provides a skeleton script for the engineer learning Python to build. Work in starter/audit.py and only use reference/audit.py if you get stuck. This guide lists instructions on how to get started with Python and basic usage, teaching how to build a functional audit.py.

The architecture diagram can be found in ../report/architecture.png

# Module 0: Setup and Prerequisites

- You would need an IDE of your choosing. An IDE is a piece of software that allows you to write, test, and debug code. I recommend Visual Studio Code, which you can download [here](https://code.visualstudio.com/).
  - There are several extensions which make coding in Python more friendly. Press Ctrl (or Command in macOS) + shift + x to open the extension menu.
    - Gitlens
    - indent-rainbow
    - Python
    - Ruff
    - Yaml

- The software Git is a very useful tool for code management. You can install it [here](https://git-scm.com/install/)
    - Once Git is installed, restart Visual Studio Code.
    - On the welcome page of Visual Studio Code, there will be the option to clone a repository. Click that, sign into GitHub (or make an account), and paste the URL of this repository into the search bar and press enter to clone (making a copy) of this repository for you to own locally on your device. Save into whichever folder of choice.
 
- This program and lab uses Python 3.14.4, which you can download [here](https://www.python.org/downloads/).
  - Ensure that when you are going through the installer, you select the " Add to Path " option.
  - Once Python is installed, restart Visual Studio Code.
  - On the top panel of Visual Studio Code, there will be a terminal option.
    - Open a terminal and type pip install -r requirements.txt
    - What this does is open requirements.txt and installs any external libraries this program uses. This lab in particular uses pyyaml and rich, which allow us to read and utilize files in a YAML format and have an elegant terminal output.

Congratulations! You are now ready to code in Python and learn from this lab!

---

# Module 1: Loading the Inventory

**Objectives:**

- Understand YAML basics
- Use yaml.safe_load
- Write your first Python function
- Work with dicts and lists

**Background**

**What is YAML?**

YAML is a human-readable data serialization standard, with the goal of being easier to read and understand compared to other data structures such as JSON or XML. YAML uses .yaml or .yml file extensions.

In the context of this lab, we are using YAML for the policy list for network devices and the inventory list. The reason we are using an external YAML file instead of hardcoding it into the Python program is that policies and devices change and update. It is relatively easy to break a program, so for the sake of stability, scalability, and maintainability, it would be wise to keep information of that nature in an external file, and just read the data from those files with our Python program.

**YAML has three structural rules:**

1. **Key-value pairs** use a colon followed by a space:
    'name: router1'


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

**Looking at 'reference/inventory.yaml':**

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

Notice the structure of inventory.yaml. A top key is called 'devices', whose value is a list, which is every item starting with '-'. Each device has four fields:
- 'name' - Identifier used in reports
- 'role' - 'core' or 'edge', used later for rule scoping
- 'site' - The physical location, also used for rule scoping
- 'config_path' - The relative path to the device's config file

