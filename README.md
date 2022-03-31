# importify

## Installation
Hopefully
```
pip install importify
```
should work.

## Use
Has a class named **Mod(modules,src,package)** which can almost directly translate to a 'pip' package and the imports to be made from said 'pip' package.

You can import the class by:
```
from importify import Mod
```

#### A **Mod** object's uses by example:
```
flaskMod=Mod(modules="jsonify,Flask as flsk",src="flask",package="Flask")

flaskMod.attemptImport() # Imports "Flask" from the "flask" module as "flsk" (Literal execution is "from flask import Flask as flsk" and also "jsonify" from the "flask" module (Literal execution is "from flask import jsonify") if it is installed*

flaskMod.install() # Installs package "Flask" if it is not installed*

flaskMod.uninstall() # Uninstalls package "Flask" if it is installed*

flaskMod.isInstalled() # Returns boolean value 'True' if the package is installed*
```
*The _Mod_ class has a static variable called PIP_FREEZE(Basically saves the information of all *currently* installed packages). Thus, calling multiple Mod.install() or Mod.uninstall()'s is not recommended because PIP_FREEZE might be corrupted/have bad data.
PIP_FREEZE is only refreshed when loading of the importify module and on install/uninstall of a _Mod_ package

#### Other features
- You can manually refresh PIP_FREEZE by *Mod.refreshPipFreezeInfo()*
- *Mod.getPipFreeze()* returns a list of _ModVersion_s that you can use to determine which packages are installed of which version. You can compare said _ModVersion_ objects with each other. Just check the methods honestly.

#### Disabling print messages for import, install, uninstall
The **Mod** class has around 9 static "silencing" boolean variables which, upon enabling, will stop printing their respective msgz.
Eg: **Mod.SILENCE_UNINSTALL_ERRORS=True** # Silence error messages when using **Mod.uninstall()**
They are all _False_ by default (No silencing)

## Purpose
This project was built solely for the purpose of providing a way to automate package installations and imports when sending over .py files that require certain imports but they aren't installed.
It also helps when you have incompatibilities and need ways to workaround by uninstalling,installing and uninstalling certain packages in certain orders. (Bad, incompatible package makers.... You are the reason for this)
