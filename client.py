import Pyro4
import tkinter as tk

class Client:
    def __init__(self):
        self.name = None
        self.window = None
        self.contacts = []
        self.proxy = None

    def connect(self):
        self.proxy = Pyro4.Proxy("PYRONAME:chat.server@" + entry.get() + ":9090")
        
clientGui = Client()

clientGui.window = tk.Tk()
clientGui.window.title("Aplicação do Cliente")
clientGui.window.geometry("300x100")

# Label
label = tk.Label(clientGui.window, text="IP do Servidor de Nomes")
label.pack(pady=1)

# Campo de entrada
entry = tk.Entry(clientGui.window, width=40)
entry.pack(pady=5)

# Botão para submeter a entrada
buttonSubmit = tk.Button(clientGui.window, text="Enviar", command=clientGui.connect)
buttonSubmit.pack(pady=5)

clientGui.window.mainloop()