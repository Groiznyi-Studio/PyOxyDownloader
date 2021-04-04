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

            
    def GetNextUrl(Data, Step):
        if Step == 1:
            for Line in Data:
                if Line.find("  <a href=\"https:") != -1:
                     Core.__Params["SecondUrl"] = Line
                     break            
            Index = 11
            for char in Core.GetParam("SecondUrl")[11:len(Core.GetParam("SecondUrl"))]:
                Index += 1
                if char == "\"":
                    Core.__Params["SecondUrl"] = Core.GetParam("SecondUrl")[11:Index-1]
                    break
                
        elif Step == 2:
            for Line in Data:
                if Line.find("                                              var page_url = \'") != -1:
                     Core.__Params["FinalUrl"] = Line
                     break
            Index = 64
            for Char in Core.GetParam("FinalUrl")[64:len(Core.GetParam("FinalUrl"))]:
                Index += 1
                if Char == "\'":
                    Core.__Params["FinalUrl"] = Core.GetParam("FinalUrl")[64:Index-1]
                    Core.__Params["FinalUrl"] = "http://"+Core.GetParam("FinalUrl")
                    break


    def GetNameFile(Data):
        for Line in Data:
            if Line.find("                                              <b>Название файла:</b> ") != -1:
                 Core.__Params["NameFile"] = Line
                 break
        Index = 69
        for Char in Core.GetParam("NameFile")[69:len(Core.GetParam("NameFile"))]:
            Index += 1
            if Char == "<":
                Core.__Params["NameFile"] = Core.GetParam("NameFile")[69:Index-2]
                break

            
    def WriteHtmlCodePage(NameFile, Content = False):
        if Content == False:
            try:
                File = open(Core.__Params["ActiveDirectory"]+"/"+NameFile, "w")
                File.write(Core.__Params["HtmlCodePage"])
                File.close()
                return 1
            except:
                raise Core.CoreException("WriteHtmlCodePage return error!!!")
        elif Content:
            try:
                File = open(Core.__Params["ActiveDirectory"]+"/"+NameFile, "wb")
                File.write(Core.__Params["HtmlCodePage"])
                File.close()
                return 1
            except:
                raise Core.CoreException("WriteHtmlCodePage return error!!!")


    def ReadHtmlCodePage(NameFile):
        try:
            File = open(Core.__Params["ActiveDirectory"]+"/"+NameFile)
            Data = File.readlines()
            File.close()
            return Data
        except:
            raise Core.CoreException("ReadHtmlCodePage return error!!!")


    def DeleteFile(NameFile):
        try:
            os.remove(Core.__Params["ActiveDirectory"]+"/"+NameFile)
            return 1
        except:
            return 0
    
    
    class CoreException(Exception):
        pass

        
#------------------------------------------USE CORE AND DOWNLOAD FILE--------------------------------------
if __name__ == '__main__':
    try:
        Core.GetMainUrl()
        Core.GetHtmlCodePage(Core.GetParam("MainUrl"))
        Core.WriteHtmlCodePage("HtmlCodePage1")
        Core.ReadHtmlCodePage("HtmlCodePage1")
        Core.GetNextUrl(Core.ReadHtmlCodePage("HtmlCodePage1"), 1)
        Core.ClearParam("HtmlCodePage")
        Core.DeleteFile("HtmlCodePage1")

        Core.GetHtmlCodePage(Core.GetParam("SecondUrl"))
        Core.WriteHtmlCodePage("HtmlCodePage2")
        Core.GetNextUrl(Core.ReadHtmlCodePage("HtmlCodePage2"), 2)
        Core.GetNameFile(Core.ReadHtmlCodePage("HtmlCodePage2"))
        Core.ClearParam("HtmlCodePage")
        Core.DeleteFile("HtmlCodePage2")

        Core.GetHtmlCodePage(Core.GetParam("FinalUrl"), True)
        Core.WriteHtmlCodePage(Core.GetParam("NameFile"), True)
    except:
        print("CoreError!!!")
        input("Press Emter...")
        sys.exit()
        
    input("Finish!!! Press Enter...")
#------------------------------------------------IMPORT CORE-----------------------------------------------
else:
    pass
