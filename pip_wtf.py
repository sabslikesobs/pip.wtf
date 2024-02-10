#!/usr/bin/env python3

# https://pip.wtf
def pip_wtf(command):
    import os, os.path, sys  # noqa: E401
    t = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".pip_wtf." + os.path.basename(__file__))
    sys.path = [p for p in sys.path if "-packages" not in p] + [t]
    os.environ["PATH"] = t + os.path.sep + "bin" + os.pathsep + os.environ["PATH"]
    os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
    if os.path.exists(t): return  # noqa: E701
    os.system(" ".join([sys.executable, "-m", "pip", "install", "-t", t, command]))

# Now you just call it to install your packages:
#   pip_wtf('the rest of the pip install command here')
# Here are some examples for different platforms:

import sys  # noqa: E402
if sys.version_info >= (3, 5):
    # You gotta shell-escape your requirements if they would break on the terminal.
    # If you're on Windows, remember Windows needs double-quotes, not single.
    pip_wtf('beautifulsoup4 "requests>=1.0" pyyaml==5.3.1')

elif sys.version_info >= (3, 0):
    # You can add anything else you want to the pip install command to help add
    # special flags for difficult situations, like when the Pip version is too old
    # to support automatic https URLs...
    pip_wtf('--index-url https://pypi.python.org/simple/ beautifulsoup4==4.2.1 requests==2.13.0 pyyaml==3.10 urllib3==2.0.5')

else:
    # It even works with Python 2.7 (kinda tough to find an environment with that these days).
    pip_wtf('beautifulsoup4 requests pyyaml')

import requests  # noqa: E402
import yaml  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
soup = BeautifulSoup(requests.get("https://pypi.org").content, "html.parser")
print(yaml.dump({"header": soup.find("h1").get_text()}))
