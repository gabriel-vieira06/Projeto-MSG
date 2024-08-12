import Pyro4
import Pyro4.naming
import threading
import tkinter as tk

class RemoteServer:
    def __init__(self):
        self.nome   = None

class NameServer:
    def __init__(self):
        self.ip     = None
        self.window = None

    def get_ip(self):
        self.ip = entry.get()
        if self.ip:
            self.launch_name_server()
            self.launch_remote_server()
        else:
            print("ERRO: ENTRADA VAZIA")

    def launch_name_server(self):
        threadNameServer = threading.Thread(
            target=Pyro4.naming.startNSloop, kwargs={"host": self.ip}, daemon=True
        )
        threadNameServer.start()

    def launch_remote_server(self):
        threadRemoteServer = threading.Thread(
            target=start_remote_server, kwargs={"ip": self.ip}, daemon=True
        )
        threadRemoteServer.start()
        
def start_remote_server(ip):
    daemon  = Pyro4.Daemon(host=ip)
    try:
        ns  = Pyro4.locateNS(host=ip, port=9090)
        uri = daemon.register(RemoteServer)
        ns.register("chat.server", uri)
        print("Aguardando Conexões...")
        daemon.requestLoop()
    except Exception as e:
        print(e)

nameServerGui = NameServer()

nameServerGui.window = tk.Tk()
nameServerGui.window.title("IP - Servidor de Nomes")
nameServerGui.window.geometry("300x100")

# Campo de entrada
entry = tk.Entry(nameServerGui.window, width=40)
entry.pack(pady=10)

# Botão para submeter a entrada
buttonSubmit = tk.Button(nameServerGui.window, text="Enviar", command=nameServerGui.get_ip)
buttonSubmit.pack(pady=5)

# Loop principal
nameServerGui.window.mainloop()