<center><img src="/favicon.png"></center>

**pip.wtf: Inline dependencies for small Python scripts.**

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=./pip_wtf.py&lines=3-11) -->
<!-- The below code snippet is automatically added from ./pip_wtf.py -->
```py
# https://pip.wtf
def pip_wtf(command):
    import os, os.path, sys
    t = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".pip_wtf." + os.path.basename(__file__))
    sys.path = [p for p in sys.path if "-packages" not in p] + [t]
    os.environ["PATH"] += os.pathsep + t + os.path.sep + "bin"
    os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
    if os.path.exists(t): return
    os.system(" ".join([sys.executable, "-m", "pip", "install", "-t", t, command]))
```
<!-- MARKDOWN-AUTO-DOCS:END -->

*On [GitHub](https://github.com/sabslikesobs/pip.wtf) and [pip.wtf](https://pip.wtf). Quick start: `curl -s pip.wtf/raw`*

* * *

I've had it. I just wanted to write a single-file Python script with one measly little external import. But the Python dependency management cabal just won't stop treating me like I'm an idiot.

Pipx? Not for scripts. Poetry? "Oh, poor baby, did you forget your pyproject.toml?" Pip-run? Tired of fighting with persistence. Pip by itself with a little -U? [I've gotta give them an extra flag to show I know how to wipe my own ass!](https://peps.python.org/pep-0668/) Well, Python, you've done it. I'm pissed. I'm giving up on you...r suite of god-awful, overbearing package managers and I'm going to do it myself, in my script, with no virtual environments, no pip wrappers, and no god damn TOML!

That's **pip_wtf**: a single function you copy to the top of your Python
script. It needs pip and that's it. You call it just once instead of running
`pip install`, then do your imports, and then you've got a script that works on
every Python version since 2.7 (as long as pip is around).

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=./pip_wtf.py) -->
<!-- The below code snippet is automatically added from ./pip_wtf.py -->
```py
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
# You can add anything else you want to the pip install command.
pip_wtf('--index-url https://pypi.python.org/simple/ beautifulsoup4 "requests>=1.0" pyyaml')

import requests
import yaml
from bs4 import BeautifulSoup
soup = BeautifulSoup(requests.get("https://pypi.org").content, "html.parser")
print(yaml.dump({"header": soup.find("h1").get_text()}))
```
<!-- MARKDOWN-AUTO-DOCS:END -->

How's it work? Well, for `/home/adder/bin/bite.py`:

1. All `pip_wtf()` packages get installed into `/home/adder/bin/.pip_wtf.bite.py` on first run
2. Further runs do nothing if that directory already exists, so you have to either clean it up yourself or change the function
3. The script's `sys.path` (where it looks for modules) includes the `.pip_wtf...` directory and ignores all other `site-packages` directories just like a virtualenv would
4. The script's `PATH` (where subprocesses look for binaries) includes the `.pip_wtf...` directory
5. The script's `PYTHONPATH` (where subprocess's binaries will look for Python modules) includes the `.pip_wtf...` directory

**You're totally in charge of the new directory and the pip_wtf behavior.**

- New dependency? You need to `rm -rf` it first.
- Prefer to upgrade packages instead? Dump the early return.
- Need to support site-packages too? Change that list comprehension.
- Want to share dependencies across your seventeen pytorch scripts? Lose the early return and change `t` so it's one `.pip_wtf/` for your whole script directory, or import it, or something.

Finally. Python dependencies that follow your orders instead of the other way around.
