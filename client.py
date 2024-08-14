import Pyro4
import tkinter as tk

class Client:
    def __init__(self):
        self.name = None
        self.window = None
        self.contacts = []
        self.proxy = None

    def connect(self):
        self.name  = entryUsername.get()
        self.proxy = Pyro4.Proxy("PYRONAME:chat.server@" + entryNameServer.get() + ":9090")
        self.proxy.register_client(self.name)

    def add_contact(self):
        pass

    def change_state(self):
        if buttonState.get():
            buttonChangeState.config(text="Offline", background="red")
            buttonState.set(False)
        else:
            buttonChangeState.config(text="Online", background="green")
            buttonState.set(True)

clientGui = Client()
clientGui.window = tk.Tk()
clientGui.window.title("Aplicação do Cliente")

# Get Username
# -------------------------------------------------------------------------------------
# Label
labelUsername = tk.Label(clientGui.window, text="Nome de usuário :")
labelUsername.grid(column=0, row=0, padx=5, pady=5, sticky='w')
# Input
entryUsername = tk.Entry(clientGui.window)
entryUsername.grid(column=1, row=0, columnspan=2, padx=5, pady=5)
# -------------------------------------------------------------------------------------

# Get NameServer IP
# -------------------------------------------------------------------------------------
# Label
labelNameServer = tk.Label(clientGui.window, text="IP do Servidor de Nomes :")
labelNameServer.grid(column=0, row=1, padx=5, pady=5,  sticky='w')
# Input
entryNameServer = tk.Entry(clientGui.window)
entryNameServer.grid(column=1, row=1, columnspan=2, padx=5, pady=5)
# Button
buttonSubmitNameServer = tk.Button(clientGui.window, text="Conectar", command=clientGui.connect)
buttonSubmitNameServer.grid(column=3, row=1, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Horizontal Line
# -------------------------------------------------------------------------------------
canvas = tk.Canvas(clientGui.window, height=2, bd=0, highlightthickness=0)
canvas.create_line(0, 0, 640, 0, fill="black", width=5)
canvas.grid(column=0, row=2, columnspan=4)
# -------------------------------------------------------------------------------------

# Add Contact
# -------------------------------------------------------------------------------------
# Label
labelContact = tk.Label(clientGui.window, text="Adicionar contato :")
labelContact.grid(column=0, row=3, padx=5, pady=5,  sticky='w')
# Input
entryContact = tk.Entry(clientGui.window)
entryContact.grid(column=1, row=3, columnspan=2, padx=5, pady=5)
# Button
buttonSubmitContact = tk.Button(clientGui.window, text="Enviar", command=clientGui.add_contact)
buttonSubmitContact.grid(column=3, row=3, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Change State
# -------------------------------------------------------------------------------------
buttonState = tk.BooleanVar()
buttonState.set(True)
buttonChangeState = tk.Button(clientGui.window, text="Online", command=clientGui.change_state, background="green")
buttonChangeState.grid(column=0, row=4, columnspan=4, sticky="nsew")
# -------------------------------------------------------------------------------------

clientGui.window.mainloop()
