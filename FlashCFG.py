from Flashcord_API_Client import * 
import json, time

"""
This tool lets you quickly configure your page in a hurry.
Read https://github.com/SiriusBYT/Flashcord/wiki/The-Flashcord-Store-Template for how this file works.

This allows the script to connect to the SGN servers in order to make your store page more complete without user input
It's now probably not a good idea to disable this.
"""
AllowAPI = True; Debug = True

# Logging System + Getting current time and date in preferred format
def GetTime():
    CTime = time.localtime()
    Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
    Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
    return Time,Date
def WriteLog(Log):
    Time,Date = GetTime()
    PrintLog = f"[{Time} - {Date}] {Log}"
    print(PrintLog)
    

def ConfigLoader():
    global Addon_Name, Addon_DescriptionShort, Addon_Version, Addon_Repository, Addon_Author, Addon_License, Addon_Type, Addon_Contributors, Addon_Discord, Addon_Year, Addon_Theme, Addon_Color, Addon_Tags, Addon_Folder, Addon_ImageStore, Addon_ImageEmbed, Addon_Backup, Addon_DescriptionLong, Addon_LicenseString, Store_Template, Embed_Template, Username, Store_File, Embed_File, Type_Folder, Addon_Other, Addon_RepositoryName, Addon_TagsString
    WriteLog("Fetching all informations required for the Addon Page...")
    with open("manifest.json", "r", encoding="utf8") as Manifest_File: Manifest_JSON = json.load(Manifest_File)
    # Collect all the information from the Vanilla Replugged Manifest
    Addon_Name = Manifest_JSON["name"]
    Addon_DescriptionShort =  Manifest_JSON["description"]
    Addon_Version = Manifest_JSON["version"]
    Addon_Repository = Manifest_JSON["source"]
    Temporary = Addon_Repository.split("/")
    Addon_Author = Temporary[-2] # This looks janky but this is the best way to get the author name like I want it.
    Addon_RepositoryName = Temporary[-1]
    Addon_License = Manifest_JSON["license"]
    Addon_Type = Manifest_JSON["type"]

    # Collect all the information from the Flashcord Store Manifest
    Flashcord_Key = Manifest_JSON["flashcord"]
    Flashcord_General = Flashcord_Key["general_information"]
    Flashcord_Internal = Flashcord_Key["internal_structure"]
        # General Information
    Addon_Contributors = Flashcord_General["contributors"]
    Addon_Discord = Flashcord_General["discord_link"]
    Addon_Year = Flashcord_General["license_year"]
    Addon_Theme = Flashcord_General["sndl_theme"]
    Addon_Color = Flashcord_General["embed_color"]
    Addon_Tags = Flashcord_General["tags"]
        # Internal Information
    Addon_Folder = Flashcord_Internal["internal_name"]
    Addon_ImageStore = Flashcord_Internal["image_store"]
    Addon_ImageEmbed = Flashcord_Internal["image_embed"]
    Addon_Backup = Flashcord_Internal["backup_files"]

    # Get the HTML for the Long Description
    with open("description.html") as Description_File: Addon_DescriptionLong = Description_File.read()
    
    WriteLog("Processing Information...")
    Addon_TagsString = str(Addon_Tags).replace("[","").replace("]","").replace('"','').replace("'","")
    Addon_LicenseString = f"{Addon_Author} © {Addon_Year} - {Addon_Name} | {Addon_License}"
    Username = Addon_Author.lower()
    match Addon_Type:
        case "replugged-plugin":
            Store_Template = "flashcord/store/templates/default/default-plugin_template.html"
            Type_Folder = "plugins"
        case "replugged-theme":
            Store_Template = "flashcord/store/templates/default/default-theme_template.html"
            Type_Folder = "themes"
        case _:
            Store_Template = "flashcord/store/templates/default/default-module_template.html"
            Type_Folder = "modules"
    Embed_Template = "flashcord/store/templates/default/default-embed_template.html"
    Store_File = f"flashcord/store/{Type_Folder}/{Username}/{Addon_Folder}.html"
    Embed_File = f"flashcord/store/{Type_Folder}/{Username}/{Addon_Folder}-files/embed.html"

    # Call the Flashcord API to get all other addons made by the author (Warning: code is bad and ugly)
    API_Folders = Flashcord_API_Client(f"GET/{Type_Folder.upper()}/{Username.upper()}"); Addon_Other = ""
    if API_Folders != None:
        API_Folders = API_Folders.replace("[","").replace("]","").replace('"','').replace("'","").replace(' ','').split(",")
        for cycle in range (len(API_Folders)):
            API_Folders[cycle] = API_Folders[cycle] + "-files"
        if Addon_Folder in API_Folders: API_Folders.remove(Addon_Folder) # We don't want duplicates!
        if API_Folders == []: Addon_Other = "<h3>It's bloody empty in here!</h3>" # Nor an empty div!
        else:
            for cycle in API_Folders:
                Addon_Other = Addon_Other + f'<iframe class="Flashcord-Module_Embed" src="{cycle}/embed.html"></iframe>\n'
    else: Addon_Other = "<h3>It's bloody empty in here!</h3>"

    ShowConfig()


def ShowConfig(): # Prints all the config loaded, debug information
    if Debug == True:
        print("")
        WriteLog(f"Name: {Addon_Name} // Author: {Addon_Author} // Version: {Addon_Version}")
        WriteLog(f"Contributors: {Addon_Contributors} // License: {Addon_LicenseString}")
        WriteLog(f"Repository: {Addon_Repository}")
        WriteLog(f"Description (Short): {Addon_DescriptionShort}")
        WriteLog(f"Description (Long): \n{Addon_DescriptionLong}")
        WriteLog(f"Tags: {Addon_Tags}")
        WriteLog(f"Theme: {Addon_Theme} // Embed Color: {Addon_Color}")
        WriteLog(f"Internal Name: {Addon_Folder} // Discord Link: {Addon_Discord}")
        WriteLog(f"Store Image: {Addon_ImageStore}")
        WriteLog(f"Embed Image: {Addon_ImageStore}")
        WriteLog(f"Store Template: {Store_Template}")
        WriteLog(f"Embed Template: {Embed_Template}")
        WriteLog(f"Store File: {Store_File}")
        WriteLog(f"Embed File: {Embed_File}")
        WriteLog(f"'Also made by' Code: \n {Addon_Other}")
        print("")

def Backup_Files():
    WriteLog("Backing up files...")
    try:
        with open(Store_File, 'r', encoding='utf-8') as Store_FileOriginal:
            with open(f"{Store_File}.bak", 'w', encoding='utf-8') as Store_FileBackup:
                Store_FileBackup.write((Store_FileOriginal.read()))
        with open(Embed_File, 'r', encoding='utf-8') as Embed_FileOriginal:
            with open(f"{Embed_File}.bak", 'w', encoding='utf-8') as Embed_FileBackup:
                Embed_FileBackup.write((Embed_FileOriginal.read()))
    except:
        WriteLog("Files not found! Creating empty files instead...")
        with open(Store_File, 'w', encoding='utf-8') as Store_FileOriginal: Store_FileOriginal.write("")
        with open(Embed_File, 'w', encoding='utf-8') as Embed_FileOriginal: Embed_FileOriginal.write("")
    WriteLog("Backup complete.\n")

def Build(File, Template):
    WriteLog(f"Building {File}..."); print("")
    with open(Template, "r", encoding="utf-8") as Template_File:
        with open(File, "w", encoding="utf-8") as Final_File: print("Emptying Final File...", end="\r"); Final_File.write("")
        with open(File, "a", encoding="utf-8") as Final_File:
            print("Reading Template...", end="\r")
            Template_HTML = Template_File.readlines()
            Template_Lines = len(Template_HTML)
            Processing_Percent = Current_Line = 0
            for line in Template_HTML:
                print(f"Processing Line {Current_Line}/{Template_Lines} // {Processing_Percent}%", end="\r")
                line = line.replace("[Addon_Name]", Addon_Name)
                line = line.replace("[Addon_DescriptionShort]", Addon_DescriptionShort)
                line = line.replace("[Addon_Version]", Addon_Version)
                line = line.replace("[Addon_Repository]", Addon_Repository)
                line = line.replace("[Addon_Author]", Addon_Author)
                line = line.replace("[Addon_RepositoryName]", Addon_RepositoryName)
                line = line.replace("[Addon_License]", Addon_License)
                line = line.replace("[Addon_Type]", Addon_Type)
                line = line.replace("[Addon_Contributors]", Addon_Contributors)
                line = line.replace("[Addon_Discord]", Addon_Discord)
                line = line.replace("[Addon_Year]", Addon_Year)
                line = line.replace("[Addon_Theme]", Addon_Theme)
                line = line.replace("[Addon_Color]", Addon_Color)
                line = line.replace("[Addon_Folder]", Addon_Folder)
                line = line.replace("[Addon_ImageStore]", Addon_ImageStore)
                line = line.replace("[Addon_ImageEmbed]", Addon_ImageEmbed)
                line = line.replace("[Addon_DescriptionLong]", Addon_DescriptionLong)
                line = line.replace("[Addon_Other]", Addon_Other)
                line = line.replace("[Addon_LicenseString]", Addon_LicenseString)
                line = line.replace("[Username]", Username)
                line = line.replace("[Addon_TagsString]", Addon_TagsString)
                print(f"Writing Line {Current_Line}/{Template_Lines} // {Processing_Percent}%", end="\r")
                Final_File.write(line)
                Current_Line+=1
                Processing_Percent = (Current_Line/Template_Lines)*100
                print(f"Finished Writing Line {Current_Line}/{Template_Lines} // {Processing_Percent}%", end="\r")
    WriteLog("Finished Building File")



def FlashCFG():
    ConfigLoader()
    if Addon_Backup == True:
        Backup_Files()
    Build(Store_File, Store_Template)
    Build(Embed_File, Embed_Template)
    WriteLog("Script Complete.")

FlashCFG()