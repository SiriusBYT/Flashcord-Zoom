import socket
import time 
import math

def Flashcord_API_Client(API_Request):
    Request_Start = time.time()
    Debug_Mode = True
    Debug_Offline = False
    Allow_LogFile = False

    # Server & Client Information
    if Debug_Offline == True:
        Server_Address = socket.gethostname()
    else:
        Server_Address = "raw_api.sirio-network.com"
    Server_Port = 1407
    Packet_Size = 8192
    Server = socket.socket()
    Client_Version = "r240217"
    Client_API_Version = "3.1"

    ASCII_Banner = "\n░█▀▀░█░░░█▀█░█▀▀░█░█░█▀▀░█▀█░█▀▄░█▀▄░░░█▀█░█▀█░▀█▀░░░█▀▀░█░░░▀█▀░█▀▀░█▀█░▀█▀\n\
░█▀▀░█░░░█▀█░▀▀█░█▀█░█░░░█░█░█▀▄░█░█░░░█▀█░█▀▀░░█░░░░█░░░█░░░░█░░█▀▀░█░█░░█░\n\
░▀░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░░░░▀░▀░▀░░░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░"
    """
    Very important almighty Flashstore API Banner
    Legends say that removing this banner will cause the world to explode.
    """

    # Logging System + Getting current time and date in preferred format
    def GetTime():
        CTime = time.localtime()
        Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
        Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
        return Time,Date
    def WriteLog(Log,isDebugMessage):
        Time,Data = GetTime()
        LogFile = f"{Data}.log"
        PrintLog = f"[{Time}] {Log}"
        FileLog = f'{PrintLog}\n'
        if Allow_LogFile == True:
            with open(LogFile, "a", encoding="utf=8") as LogFile: LogFile.write(FileLog)
        if isDebugMessage == True and Debug_Mode == True: print(PrintLog)
        elif isDebugMessage == False: print(PrintLog)
    # Key Handling Functions
    def Send(Packet):
        try: Server.send(str(Packet).encode())
        except Exception as Error_Info: WriteLog(f"TIMED OUT: Failed to send data to the server! \n[ERROR TRACEBACK]\n{Error_Info}", False); return
    def Receive_Data():
        try: Response = Server.recv(Packet_Size).decode(); return Response
        except Exception as Error_Info: WriteLog(f"TIMED OUT: Failed to receive data from the server! \n[ERROR TRACEBACK]\n{Error_Info}", False); return
    
    # Glorious.
    def SplashBanner():
        print(ASCII_Banner)
        WriteLog(f"{Server_Address}:{Server_Port}@API_{Client_API_Version} w/ Client {Client_Version} // Debug: {Debug_Mode} - Packet Size: {Packet_Size}b\n", False)
    SplashBanner()

    try:
        Server_Latency = time.time(); Server.connect((Server_Address, Server_Port))
        Server_Latency = math.floor((time.time() - Server_Latency)/1000); Server_Latency = f'{Server_Latency}ms'
    except socket.error as Error_Info: WriteLog(f'ERROR: Failed to connect to the Flashstore API! \n[ERROR TRACEBACK]\n{Error_Info}', False); return "CONNECTION_FAILURE"

    WriteLog(f'SUCCESS: Connected to {Server_Address}:{Server_Port}! (Latency: {Server_Latency})',False)
    WriteLog(f'INFO: Requesting API Version {Client_API_Version}...',True)
    try: Send(Client_API_Version); Server_Data = Receive_Data()
    except Exception as Error_Info: WriteLog(f'[ERROR] Failed to send Client API Version to the server! \n[ERROR TRACEBACK]\n{Error_Info}", False)',False); return "TIMEOUT"
    match Server_Data:
        case "API_BANNED": WriteLog(f"[ERROR] You have been banned from using the Flashcord API.", True); return "API_BANNED"
        case "INVALID_VERSION": WriteLog(f'[ERROR] The server told us our API Version is invalid!', False); return "INVALID_VERSION"
        case "OUTDATED_VERSION": WriteLog(f'[ERROR] The server told us our API Version is out of date!', False); return "OUTDATED_VERSION"
        case "ALREADY_CONNECTED": WriteLog(f"[ERROR] The server told us we're already connected to it!", False); return "ALREADY_CONNECTED"
        case "OUTDATED_SERVER": WriteLog(f"[WARNING] The server told us our API Version is newer than the server's!", False)
        case "OK": WriteLog(f"[OK] We sent a valid API Version.", True)
    try:
        WriteLog(f'INFO: Requesting "{API_Request}".',True); Send(API_Request); Server_Data = Receive_Data()
        match Server_Data:
            case "INVALID_REQUEST": WriteLog(f'[ERROR] The server told us our request is invalid!',False); return "INVALID_REQUEST"
            case "MISSING_ARGUMENTS": WriteLog(f'[ERROR] The server told us our request is missing arguments!',False); return "MISSING_ARGUMENTS"
            case "NOT_FOUND": WriteLog(f"[ERROR] The server told us our request couldn't be found!",False); return "INVALID_REQUEST"
            case "ALREADY_DONE": WriteLog(f"[ERROR] The server told us our one-time request was already done!",False); return "ALREADY_DONE"
            case None: WriteLog(f"[ERROR] An unknown error occurred!",False); return "UNKNOWN_ERROR"
            case "": WriteLog(f"[ERROR] The server sent us an empty response!",False); return "EMPTY_RESPONSE"
            case _: WriteLog(f'[SUCCESS] Received {Server_Data} for our request!',False); return Server_Data
    except Exception as Error_Info: WriteLog(f'[ERROR] Failed to send our API request! \n[ERROR TRACEBACK]\n{Error_Info}", False)',False); return "TIMEOUT"