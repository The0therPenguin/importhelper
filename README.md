# importhelper

## Requirements/Imports
- os
- threading
- traceback
- subprocess

## Installation
Hopefully...
```
pip install importhelper
```
... should work.

## Use
Has a class named _**Mod(modules,src,package)**_ which can almost directly translate to a pip package and the imports/installs to be made from said pip package. Custom urls for packages are not supported. (Only uses official packages from PyPI)

You can import the class by:
```
from importify import Mod
```

#### A **Mod** object's uses by example:
```
flaskMod = Mod(modules="jsonify,Flask as flsk",src="flask",package="Flask")
# If 'package' is not provided, it will take 'src's value
# 'src' and 'package' can only be strings
# 'modules' can either be a string with format "<Module> as <Name>,<Module2> as <Name2>,.."
# or can be a list like ["<Module> as <Name>","<Module2> as <Name2>"]
# or can be a dict like {"<Module>":"<Name>","<Module1>":"<Name2>"}
## Yes... I know Name:Module for dict makes more sense but izz too much effort to do that (Only 2 lines but still) =-=

# Imports "Flask" from the "flask" module as "flsk" (Literal execution is "from flask import Flask as flsk" and also "jsonify" from the "flask" module (Literal execution is "from flask import jsonify") if it is installed*
flaskMod.attemptImport()

# Installs package "Flask" if it is not installed*
flaskMod.install()

# Uninstalls package "Flask" if it is installed*
flaskMod.uninstall()

# Returns boolean value 'True' if the package is installed*
flaskMod.isInstalled()

requestsMod
```
* The _**Mod**_ class has a static variable called PIP_FREEZE(Basically saves the information of all *currently* installed packages). Thus, calling multiple Mod.install() or Mod.uninstall()'s is not recommended because PIP_FREEZE might be corrupted/have bad data.
PIP_FREEZE is only refreshed when loading of the importify module and on install/uninstall of a _**Mod**_ package.

#### Other features
- You can manually refresh PIP_FREEZE by *Mod.refreshPipFreezeInfo()*
- _**Mod.getPipFreeze()**_ returns a list of _**ModVersion**_ s that you can use to determine which packages are installed of which version. You can compare said _**ModVersion**_ objects with each other. Just check the methods honestly.

#### Disabling print messages for import, install, uninstall
The _**Mod**_ class has around 9 static "silencing" boolean variables which, upon enabling, will stop printing their respective msgz.
Eg: _**Mod.SILENCE_UNINSTALL_ERRORS=True**_ # Silence error messages when using _**Mod.uninstall()**_
They are all _False_ by default (No silencing)

## Purpose
This project was built solely for the purpose of providing a way to automate package installations and imports when sending over .py files that require certain imports but they aren't installed i.e., _**import requests**_ throws an error because you don't have it installed.
It also helps when you have incompatibilities and need ways to workaround by uninstalling, installing and uninstalling certain packages in certain orders.
(Bad and incompatible package creators.... You are the reason for this *eyes intensely*)
