import Pyro4
import tkinter as tk
import threading
import json

global chatBox

class Client:
    def __init__(self):
        self.name             = None
        self.window           = None
        self.contacts         = []
        self.proxy            = None
        self.state            = True   # true => online, false => offline
        self.selected_contact = None

    def connect(self):
        self.name  = entryUsername.get()
        self.proxy = Pyro4.Proxy("PYRONAME:chat.server@" + entryNameServer.get() + ":9090")
        self.proxy.register_client(self.name, self.state)
        threading.Thread(target=self.get_message, daemon=True).start()

    def contact_exists(self, newContact):
        for contact in self.contacts:
            if contact["nome"] == newContact["nome"]:
                return True
        return False

    def add_contact(self):
        newContact = {"nome": entryContact.get(), "button": None}
        if not self.contact_exists(newContact):
            self.contacts.append(newContact)
            self.selected_contact = newContact["nome"]
            newContact["button"]  = tk.Button(self.window, text=newContact["nome"], command=lambda contact=newContact["nome"]: self.select_contact(contact))
            newContact["button"].grid(column=0, row=(4+len(self.contacts)), padx=5, pady=5, sticky="nsew")

    def select_contact(self, contactButton):
        self.selected_contact = contactButton
        for contact in self.contacts:
            if contact["nome"] == contactButton:
                contact["button"].config(bg="lightgreen")
            else:
                contact["button"].config(bg="white")

    def send_message(self):
        message = json.dumps(entryMessage.get())
        self.proxy.send_message(self.selected_contact, message, self.name)
        chatBox.insert(tk.END, f'{self.name} : {message}\n')

    def change_state(self):
        if buttonState.get():
            buttonChangeState.config(text="Offline", background="red")
            buttonState.set(False)
            entryMessage.config(state="disabled")
        else:
            buttonChangeState.config(text="Online", background="green")
            buttonState.set(True)
            entryMessage.config(state="normal")
        
        self.state = buttonState.get()
        self.proxy.change_client_state(self.name, self.state)
    
    def get_message(self):
        while True:
            listClients = self.proxy.get_clients()
            for client in listClients:
                if client["nome"] == self.name and client["notify"] == True:
                    chatBox.insert(tk.END, f'{client["message"]}\n')
                    self.proxy.msg_acknowledge(self.name)
                
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
entryUsername.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Get NameServer IP
# -------------------------------------------------------------------------------------
# Label
labelNameServer = tk.Label(clientGui.window, text="IP do Servidor de Nomes :")
labelNameServer.grid(column=0, row=1, padx=5, pady=5,  sticky='w')
# Input
entryNameServer = tk.Entry(clientGui.window)
entryNameServer.grid(column=1, row=1, columnspan=2, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitNameServer = tk.Button(clientGui.window, text="Conectar", command=clientGui.connect)
buttonSubmitNameServer.grid(column=3, row=1, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Add Contact
# -------------------------------------------------------------------------------------
# Label
labelContact = tk.Label(clientGui.window, text="Adicionar contato :")
labelContact.grid(column=0, row=2, padx=5, pady=5,  sticky='w')
# Input
entryContact = tk.Entry(clientGui.window)
entryContact.grid(column=1, row=2, columnspan=2, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitContact = tk.Button(clientGui.window, text="Enviar", command=clientGui.add_contact)
buttonSubmitContact.grid(column=3, row=2, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Change State
# -------------------------------------------------------------------------------------
buttonState = tk.BooleanVar()
buttonState.set(True)
buttonChangeState = tk.Button(clientGui.window, text="Online", command=clientGui.change_state, background="green")
buttonChangeState.grid(column=0, row=3, columnspan=4, sticky="nsew")
# -------------------------------------------------------------------------------------

# Input message
# -------------------------------------------------------------------------------------
# Label
labelMessage = tk.Label(clientGui.window, text="Envie uma mensagem :")
labelMessage.grid(column=0, row=4, padx=5, pady=5,  sticky='w')
# Input
entryMessage = tk.Entry(clientGui.window)
entryMessage.grid(column=1, row=4, columnspan=2, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitMessage = tk.Button(clientGui.window, text="Enviar", command=clientGui.send_message)
buttonSubmitMessage.grid(column=3, row=4, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Chat box
# -------------------------------------------------------------------------------------
chatBox = tk.Text(clientGui.window)
chatBox.grid(column=1, row=5, rowspan=6, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Loop Principal
clientGui.window.mainloop()
