import Pyro4
import Pyro4.naming
import threading
import tkinter as tk
import pika
from config.connection_config import amqp_broker_configs

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RemoteServer:
    def __init__(self):
        self.clients        = []
        self.connection     = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_broker_configs["HOST"],
                                                                                port=amqp_broker_configs["PORT"],
                                                                                credentials=pika.PlainCredentials(amqp_broker_configs["USERNAME"], amqp_broker_configs["PASSWORD"]),
                                                                                virtual_host=amqp_broker_configs["VIRTUAL_HOST"]))
        self.channel        = self.connection.channel()
        self.consume_thread = threading.Thread(target=self.channel.start_consuming, daemon=True)
    
    def register_client(self, clientName):
        if clientName not in self.clients:
            self.clients.append(clientName)
            self.channel.queue_declare(queue=clientName)
            self.channel.basic_consume(queue=clientName, on_message_callback=self.msg_callback, auto_ack=True)

    def msg_callback(self, ch, method, properties, body):
        print(f" [x] Recebido {body}")

    def send_message(self, destination, message):
        self.channel.queue_declare(queue=destination)
        self.channel.basic_publish(exchange='', routing_key=destination, body=message)

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