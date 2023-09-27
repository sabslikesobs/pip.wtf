#!/usr/bin/env python3

# https://pip.wtf
def pip_wtf(command):
    import os, os.path, sys
    t = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".pip_wtf." + os.path.basename(__file__))
    sys.path = [p for p in sys.path if "-packages" not in p] + [t]
    os.environ["PATH"] += os.pathsep + t + os.path.sep + "bin"
    os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
    if os.path.exists(t): return
    os.system(" ".join([sys.executable, "-m", "pip", "install", "-t", t, command]))

import sys
if sys.version_info >= (3, 5):
    # You gotta shell-escape your requirements if they would break on the terminal.
    # If you're on Windows, remember Windows needs double-quotes, not single.
    pip_wtf('beautifulsoup4 "requests>=1.0" pyyaml==5.3.1')

else:
    # You can add anything else you want to the pip install command to help add
    # special flags for difficult situations. You can keep retrying it until it
    # works, if you really want to.
    pip_wtf('--index-url https://pypi.python.org/simple/ beautifulsoup4==4.2.1 requests==2.13.0 pyyaml==3.10 urllib3==2.0.5')

import requests
import yaml
from bs4 import BeautifulSoup
soup = BeautifulSoup(requests.get("https://pypi.org").content, "html.parser")
print(yaml.dump({"header": soup.find("h1").get_text()}))
