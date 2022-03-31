import os 
import subprocess
import traceback
import threading

class ModVersion:
    def __init__(self,versionStr):
        self.versions = [int(i) for i in versionStr.split(".")]
    def __str__(self):
        return ".".join(self.versions)
    def __gt__(self, other):
        for i,j in self.versions,other.versions:
            if (i > j):
                return True
            elif (i < j):
                return False
        return False
    def __eq__(self, other):
        for i,j in self.versions,other.versions:
            if(i != j):
                return False
        return True
class Mod:
    PIP_FREEZE = {}
    SILENCE_IMPORT_START = False
    SILENCE_IMPORT_ERRORS = False
    SILENCE_IMPORT_SUCCESS = False
    SILENCE_INSTALL_START = False
    SILENCE_INSTALL_OUTPUT = False
    SILENCE_INSTALL_SUCCESS = False
    SILENCE_INSTALL_ERRORS = False
    SILENCE_UNINSTALL_START = False
    SILENCE_UNINSTALL_OUTPUT = False
    SILENCE_UNINSTALL_SUCCESS = False
    SILENCE_UNINSTALL_ERRORS = False
    IMPORT_ERROR_MESSAGE = "> Failed to import %s"
    IMPORT_START_MESSAGE = "> Importing %s..."
    IMPORT_SUCCESS_MESSAGE = "> Successfully imported %s"
    INSTALL_ERROR_MESSAGE = "> Failed to install %s==%s"
    INSTALL_START_MESSAGE = "> Installing %s==%s..."
    INSTALL_SUCCESS_MESSAGE = "> Successfully uninstalled %s==%s"
    UNINSTALL_ERROR_MESSAGE = "> Failed to uninstall %s==%s"
    UNINSTALL_START_MESSAGE = "> Uninstalling %s==%s..."
    UNINSTALL_SUCCESS_MESSAGE = "> Successfully uninstalled %s==%s"
    def __init__(self, modules=None,src=None,pip=None):
        self.modules = modules
        if(self.modules is None):
           if(pip is None):
               raise RuntimeError("Mod constructor requires EITHER modules as string/list/dict OR pip as string.")
        self.src = src
        self.package = pip
        self.packageVersion = None
        if(self.package is None):
            self.package = self.src
        if(type(self.package) is str and self.package.count("==") > 0):
            self.package,self.packageVersion = self.package.split("==")
        if(self.packageVersion is not None):
            self.packageVersion = ModVersion(self.packageVersion)
        if(self.package is None and type(self.modules) is str):
            self.package = self.modules
        self.__installOP = None
        self.__uninstallOP = None
    def isInstalled(self):
        return self.package in Mod.PIP_FREEZE
    def isMinimumVersionInstalled(self):
        return self.isInstalled and Mod.PIP_FREEZE[self.package] >= self.packageVersion
    def isRequiredVersionInstalled(self):
        return self.isInstalled and Mod.PIP_FREEZE[self.package] == self.packageVersion
    def getImportScript(self):
        if(self.modules is None):
            return None
        toExec = "import "
        if self.src is not None:
            toExec = "from %s " % self.src + toExec
        if(type(self.modules) is dict):
            for modl in self.modules:
                toExec = toExec + "%s as %s," % (modl,self.modules[modl])
        elif(type(self.modules) is list):
            for modl in self.modules:
                toExec = toExec + "%s," % modl
        else:
            toExec = toExec + self.modules
        if(toExec.endswith(",")):
            toExec = toExec[:-1]
        return toExec
    def getPackageVersion(self):
        return self.packageVersion if self.packageVersion else "Latest"
    def getInstalledPackageVersion(self):
        return Mod.PIP_FREEZE[self.package] if self.package in Mod.PIP_FREEZE else "UNKWN"
    def __install(self,*args):
        try:
            if(not Mod.SILENCE_INSTALL_START):
                if(Mod.INSTALL_START_MESSAGE.count("%s") == 2):
                    print(Mod.INSTALL_START_MESSAGE % (self.package,self.getPackageVersion()))
                else:
                    print(Mod.INSTALL_START_MESSAGE + " " + self.package + "==" + self.getPackageVersion())
            with subprocess.Popen(self.pipInstallCmd,shell=True,stdout=subprocess.PIPE) as sp:
                self.__installOP = ""
                while True:
                    line = sp.stdout.readline().decode()
                    if not line:
                        break
                    line = line.rstrip()
                    if(not Mod.SILENCE_INSTALL_OUTPUT):
                        print(line)
                    self.__installOP = self.__installOP + "%s\n" % line
            Mod.refreshPipFreezeInfo()
            if(not Mod.SILENCE_INSTALL_SUCCESS):
                if(Mod.INSTALL_SUCCESS_MESSAGE.count("%s") == 2):
                    print(Mod.INSTALL_SUCCESS_MESSAGE % (self.package,self.getInstalledPackageVersion()))
                else:
                    print(Mod.INSTALL_SUCCESS_MESSAGE + " " + self.package + "==" + str(self.getInstalledPackageVersion()))
        except Exception as e:
            if(not Mod.SILENCE_INSTALL_ERRORS):
                if(Mod.INSTALL_ERROR_MESSAGE.count("%s") == 2):
                    print(Mod.INSTALL_ERROR_MESSAGE % (self.package,self.getdPackageVersion()))
                else:
                    print(Mod.INSTALL_ERROR_MESSAGE + " " + self.package + "==" + str(self.getPackageVersion()))
            return False
    def __uninstall(self,*args):
        try:
            if(not Mod.SILENCE_UNINSTALL_START):
                if(Mod.UNINSTALL_START_MESSAGE.count("%s") == 2):
                    print(Mod.UNINSTALL_START_MESSAGE % (self.package,self.getInstalledPackageVersion()))
                else:
                    print(Mod.UNINSTALL_START_MESSAGE + " " + self.package + "==" + self.getInstalledPackageVersion())
            with subprocess.Popen(self.pipUninstallCmd,shell=True,stdout=subprocess.PIPE) as sp:
                self.__uninstallOP = ""
                while True:
                    line = sp.stdout.readline().decode()
                    if not line:
                        break
                    line = line.rstrip()
                    if(not Mod.SILENCE_UNINSTALL_OUTPUT):
                        print(line)
                    self.__uninstallOP = self.__uninstallOP + "%s\n" % line
            Mod.refreshPipFreezeInfo()
            if(not Mod.SILENCE_UNINSTALL_SUCCESS):
                if(Mod.UNINSTALL_SUCCESS_MESSAGE.count("%s") == 2):
                    print(Mod.UNINSTALL_SUCCESS_MESSAGE % (self.package,self.getInstalledPackageVersion()))
                else:
                    print(Mod.UNINSTALL_SUCCESS_MESSAGE + " " + self.package + "==" + str(self.getInstalledPackageVersion()))
        except Exception as e:
            if(not Mod.SILENCE_UNINSTALL_ERRORS):
                if(Mod.UNINSTALL_ERROR_MESSAGE.count("%s") == 2):
                    print(Mod.UNINSTALL_ERROR_MESSAGE % (self.package,self.getdPackageVersion()))
                else:
                    print(Mod.UNINSTALL_ERROR_MESSAGE + " " + self.package + "==" + str(self.getPackageVersion()))
            return False
    def install(self,upgrade=True,blockThread=True):
        if(self.package is None):
            return False
        self.pipInstallCmd = "pip install "
        if(upgrade):
            self.pipInstallCmd = self.pipInstallCmd + "--upgrade "
        self.pipInstallCmd = self.pipInstallCmd + self.package
        if(self.packageVersion is not None):
            self.pipInstallCmd = self.pipInstallCmd + "==%s" % self.packageVersion
        th = threading.Thread(target=self.__install,args=(self,),daemon=True)
        th.start()
        if(blockThread):
            th.join()
        if(self.__installOP):
            return self.__installOP
    def uninstall(self,blockThread=True):
        self.pipUninstallCmd = "pip uninstall -y %s" % self.package
        th = threading.Thread(target=self.__uninstall,args=(self,),daemon=True)
        th.start()
        if(blockThread):
            th.join()
        if(self.__uninstallOP):
            return self.__uninstallOP
    def attemptImport(self,globals=None,onFailCallback=None):
        if(globals is None):
            globals = globals()
        toExec = self.getImportScript()
        if(toExec is None):
            return False
        if(not Mod.SILENCE_IMPORT_START):
            if(Mod.IMPORT_START_MESSAGE.count("%s") == 1):
                print(Mod.IMPORT_START_MESSAGE % (toExec))
            else:
                print(Mod.IMPORT_START_MESSAGE + " " + toExec)
        try:
            exec(toExec,globals)
            if(not Mod.SILENCE_IMPORT_SUCCESS):
                if(Mod.IMPORT_SUCCESS_MESSAGE.count("%s") == 1):
                    print(Mod.IMPORT_SUCCESS_MESSAGE % (toExec))
                else:
                    print(Mod.IMPORT_SUCCESS_MESSAGE + " " + toExec)
            return True
        except ImportError as e:
            if(onFailCallback is not None):
                onFailCallback(self,e)
                return False
            if(not Mod.SILENCE_IMPORT_ERRORS):
                if(Mod.IMPORT_ERROR_MESSAGE.count("%s") == 1):
                    print(Mod.IMPORT_ERROR_MESSAGE % (toExec))
                else:
                    print(Mod.IMPORT_ERROR_MESSAGE + " " + toExec)
                traceback.print_exc()
            return False
    @classmethod
    def getPipFreeze(cls):
        with (subprocess.Popen("pip freeze --all",shell=True,stdout=subprocess.PIPE)) as sp:
            red = sp.stdout.read().decode()
            toReturn = dict(tuple(i.split("==")) for i in red.replace("\r\n","\n").split("\n") if i.count("==") > 0)
            for i in toReturn:
                toReturn[i] = ModVersion(toReturn[i])
            return toReturn
    @classmethod
    def refreshPipFreezeInfo(cls):
        Mod.PIP_FREEZE = Mod.getPipFreeze()
Mod.refreshPipFreezeInfo()
