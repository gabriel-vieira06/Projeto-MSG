import Pyro4
import Pyro4.naming
import threading
import tkinter as tk
from tkinter import messagebox

class NameServer:
    def name_server_init(self, ip):
        t_name_server = threading.Thread(
            target=Pyro4.naming.startNSloop, kwargs={"host": ip}, daemon=True
        )
        t_name_server.start()

class NameServerInterface:
    def __init__(self):
        self.ip = None
        self.window = None

    def get_ip(self):
        self.ip = entry.get()
        if self.ip:
            name_server = NameServer()
            name_server.name_server_init(self.ip)
        else:
            print("ERRO: ENTRADA VAZIA")

nameServerGui = NameServerInterface()

nameServerGui.window = tk.Tk()
nameServerGui.window.title("IP - Servidor de Nomes")
nameServerGui.window.geometry("300x100")

# Campo de entrada
entry = tk.Entry(nameServerGui.window, width=40)
entry.pack(pady=10)

# Botão para submeter a entrada
button_submit = tk.Button(nameServerGui.window, text="Enviar", command=nameServerGui.get_ip)
button_submit.pack(pady=5)

# Loop principal
nameServerGui.window.mainloop()