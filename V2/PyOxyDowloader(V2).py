#IMPORT MODULES
import requests #pip install requests!!!
import os
import sys
import os.path as osp #os.path -> osp


class Core():
    __Params = {
        "ActiveDirectory" : sys.argv[0][0:len(sys.argv[0]) - len(osp.basename(sys.argv[0])) - 1],
        "HtmlCodePage" : None,
        "MainUrl" : "",
        "SecondUrl" : "",
        "FinalUrl" : "",
        "NameFile" : ""}


    def GetMainUrl():
        MainUrl = input("Url Oxy.Cloud: ")
        Core.__Params["MainUrl"] = MainUrl


    def GetHtmlCodePage(Url, Content = False):
        if Content == False:
            try:
                HtmlCodePage = requests.get(Url)
                Core.__Params["HtmlCodePage"] = HtmlCodePage.text
                return 1
            except:
                raise Core.CoreException("GetHtmlCodePage return error!!!")
            
        elif Content:
            try:
                HtmlCodePage = requests.get(Url)
                Core.__Params["HtmlCodePage"] = HtmlCodePage.content
                return 1
            except:
                raise Core.CoreException("GetHtmlCodePage return error!!!")
        else:
            return 0


    def GetParam(Param):
        if Param in Core.__Params:
            return Core.__Params[Param]
        else:
            raise Core.CoreException("ClearParam \""+Param+"\" not defined!!!")

            
    def ClearParam(Param):
        if Param in Core.__Params:
            Core.__Params[Param] = None
            return 1
        else:
            raise Core.CoreException("ClearParam \""+Param+"\" not defined!!!")

            
    def GetNextUrl(Step):
        if Step == 1:
            try:
                Core.__Params["SecondUrl"] = Core.__Params["HtmlCodePage"].split('\n')[226]
            except:
                raise Core.CoreException("GetNextUrl return error!!!(Site not OxyCloud!!!)")
            Index = 11
            for char in Core.GetParam("SecondUrl")[11:len(Core.GetParam("SecondUrl"))]:
                Index += 1
                if char == "\"":
                    Core.__Params["SecondUrl"] = Core.GetParam("SecondUrl")[11:Index-1]
                    break
                
        elif Step == 2:
            try:
                Core.__Params["FinalUrl"] = Core.__Params["HtmlCodePage"].split('\n')[249]   
            except:
                raise Core.CoreException("GetNextUrl return error!!!(Site not OxyCloud!!!)")
            Index = 64
            for Char in Core.GetParam("FinalUrl")[64:len(Core.GetParam("FinalUrl"))]:
                Index += 1
                if Char == "\'":
                    Core.__Params["FinalUrl"] = Core.GetParam("FinalUrl")[64:Index-1]
                    Core.__Params["FinalUrl"] = "https://"+Core.GetParam("FinalUrl")
                    break


    def GetNameFile():
        try:
            Core.__Params["NameFile"] = Core.__Params["HtmlCodePage"].split('\n')[218]      
        except:
            raise Core.CoreException("GetNameFile return error!!!(Site not OxyCloud!!!)")
        Index = 69
        for Char in Core.GetParam("NameFile")[69:len(Core.GetParam("NameFile"))]:
            Index += 1
            if Char == "<":
                Core.__Params["NameFile"] = Core.GetParam("NameFile")[69:Index-2]
                break

            
    def WriteFile(NameFile):
        try:
            File = open(Core.__Params["ActiveDirectory"]+"/"+NameFile, "wb")
            File.write(Core.__Params["HtmlCodePage"])
            File.close()
            return 1
        except:
            raise Core.CoreException("WriteFile return error!!!")

    
    class CoreException(Exception):
        def __init__(self, Message):
            self.Message = Message

        
#------------------------------------------USE CORE AND DOWNLOAD FILE--------------------------------------
try:
    Core.GetMainUrl()
    os.system("cls")
    Core.GetHtmlCodePage(Core.GetParam("MainUrl"))
    Core.GetNextUrl(1)
    Core.ClearParam("HtmlCodePage")
    print("Url_1: "+Core.GetParam("SecondUrl"))
            
    Core.GetHtmlCodePage(Core.GetParam("SecondUrl"))
    Core.GetNextUrl(2)
    Core.GetNameFile()
    print("Url_2: "+Core.GetParam("FinalUrl"))
    print("NameFile: "+Core.GetParam("NameFile"))
    Core.ClearParam("HtmlCodePage")

    Core.GetHtmlCodePage(Core.GetParam("FinalUrl"), True)
    Core.WriteFile(Core.GetParam("NameFile"))
    input("Finish!!! Press Enter...")
except Core.CoreException as CoreException:
    print(CoreException.Message)
    input("Press Enter...")