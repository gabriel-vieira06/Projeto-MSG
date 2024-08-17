import Pyro4
import Pyro4.naming
import threading
import tkinter as tk

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RemoteServer:
    def __init__(self):
        self.clients = []
    
    def register_client(self, clientName):
        self.clients.append(clientName)
        print(self.clients)

class NameServer:
    def __init__(self):
        self.ip     = None
        self.window = None

    def set_ip(self):
        self.ip = entryNameServer.get()
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

# Set NameServer IP
# -------------------------------------------------------------------------------------
# Label
labelNameServer = tk.Label(nameServerGui.window, text="IP do Servidor de Nomes :")
labelNameServer.grid(column=0, row=0, padx=5, pady=5, sticky='w')
# Input
entryNameServer = tk.Entry(nameServerGui.window)
entryNameServer.grid(column=1, row=0, columnspan=2, padx=5, pady=5)
# Button
buttonSubmitNameServer = tk.Button(nameServerGui.window, text="Criar", command=nameServerGui.set_ip)
buttonSubmitNameServer.grid(column=3, row=0, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Loop principal
nameServerGui.window.mainloop()