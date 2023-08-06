# Confy: A dictionary backed by a real .json file

Confy is a dictionary with a `.save()` method. Acts exactly the same as a regular dictionary otherwise.

## Install

`pip install confy`

## Use

```python
from confy import Confy

configPath = "config.json"
config = Confy(configPath)

if "timesOpened" in config:
    timesOpened = config["timesOpened"]
else:
    timesOpened = 0

print("Opened {} times".format(timesOpened))
config["timesOpened"] = timesOpened + 1
```

## Licensing

MIT

## Author

Made by Martijn Brekelmans. This project is used in [SMG music display](https://martijnbrekelmans.com/SMG).


