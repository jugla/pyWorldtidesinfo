# pyworldtidesinfo
## General
![GitHub release](https://img.shields.io/github/release/jugla/pyWorldtidesinfo)

Get tide info from World Tides Info server :
- Location Parameter : latitude/longitude of monitored point
- Tide prediction parameter : reference (LAT,...), tide station distance, tide prediction duration
- Tide picture : unit (meter/feet), plot/background color

## Installing
```
pip install pyworldtidesinfo
```

## Use
**Prerequisite** : a valid key from https://www.worldtides.info/

The `__main__.py` is provided to show an example of use.

- 2 main functions to connect to server :

  - retrieve tide station info

  - retrieve tide info (height, ...)

- several functions to decode the receive message from server


