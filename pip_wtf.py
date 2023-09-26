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

# You gotta shell-escape your requirements if they would break on the terminal.
# If you're on Windows, remember Windows needs double-quotes, not single.
pip_wtf('beautifulsoup4 "requests>=1.0" pyyaml==5.3.1')
# You can add anything else you want to the pip install command
# to help add special flags for difficult situations.
pip_wtf('--index-url https://pypi.python.org/simple/ beautifulsoup4 "requests>=1.0" pyyaml')
# You can keep retrying it until it works, if you really want to.
pip_wtf('beautifulsoup4==4.0.1 requests==2.4.0 pyyaml==3.11')

import requests
import yaml
from bs4 import BeautifulSoup
soup = BeautifulSoup(requests.get("https://pypi.org").content, "html.parser")
print(yaml.dump({"header": soup.find("h1").get_text()}))
