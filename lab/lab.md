### Network Compliance Auditor

**Author:** Wael Shahadeh
**Version:** 1.0.0

---

## About This Lab

This lab introduces network engineers to Python by building a working network compliance auditor. There is reference/audit.py to use as a guide of what a functional Python program looks like, and starter/audit.py, which has a skeleton script to be built by the engineer learning Python. This guide lists instructions on how to get started with Python and basic usage, teaching how to build a functional audit.py.


**Prerequisites:**

- You would need an IDE of your choosing. An IDE is a piece of software that allows you to write, test, and debug code. I recommend Visual Studio Code, which you can download [here](https://code.visualstudio.com/).
  - There are several extensions which make coding in Python more friendly. Press ctrl (or command in macOS) + shift + x to open the extension menu.
    - Gitlens
    - indent-rainbow
    - Prettier
    - Python
    - Ruff
    - Yaml

- The software Git is a very useful tool for code management. You can install it [here](https://git-scm.com/install/)
    - Once Git is installed, restart Visual Studio Code.
    - On the welcome page of Visual Studio Code, there will be the option to clone a repository. Click that, sign into Github (or make an account), and paste the url of this repository into the search bar and press enter to clone (making a copy) of this repository for you to own locally on your device. Save into whichever folder of choice.
  
- This program and lab uses Python 3.14.4, which you can download [here](https://www.python.org/downloads/). 
  - Ensure that when you are going through the installer, you select the add to path option.
  - Once Python is installed, restart Visual Studio Code.
  - On the top panel of Visual Studio Code, there will be a terminal option. 
    - Open a terminal and type pip install requirements.txt
    - What this does is open requirmeents.txt and installs any external libraries this program uses. This lab in particular uses pyyaml and rich, which allow us to read and utilize files in a YAML format and have an elegant terminal output.

Congradulations! You are now ready to code in Python and learn from this lab!

---

