import socket
import threading
import json

class MLPlay:
    def __init__(self,*args, **kwargs):
        print("Initial ml script")        
                   
        self.scene_info = []
        self.server = GameServer()
        server_thread = threading.Thread(target=self.server.start)
        server_thread.start()
        
    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """       
        action_mapping =  [["UP"], ["DOWN"], ["LEFT"], ["RIGHT"],["NONE"]]
        
        while self.server.receive_command  is None:            
            pass

        command = self.server.receive_command["command"]
        self.server.receive_command = None 
        self.server.send_data(scene_info)        
            

        
        return action_mapping[command]

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        
        pass

class GameServer:
    def __init__(self, host='localhost', port=12345):        
        """
        Initialize the GameServer.

        Parameters:
        host (str): The hostname or IP address to bind the server to (default is 'localhost').
        port (int): The port number to listen on (default is 12345).
        """
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.client_socket = None
        self.receive_command = None
        self.running = True

    def handle_client(self, client_socket):
        """
        Handle communication with a connected client.

        Parameters:
        client_socket (socket.socket): The socket object representing the client connection.
        """
        self.client_socket = client_socket
        while self.running:
            received = client_socket.recv(4096).decode('utf-8')
            if not received:
                break            
            self.receive_command = json.loads(received)
            
    def send_data(self, data):
        """
        Send data to the connected client.

        Parameters:
        data (dict): The data to be sent in dictionary format.
        """
        if self.client_socket:
            json_data = json.dumps(data)
            self.client_socket.send(json_data.encode('utf-8'))

    def start(self):
        """
        Start the server and listen for client connections.
        """
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print(f'Server listening on {self.host}:{self.port}...')

        client, address = self.server.accept()
        print(f'Connected to {address}')
        self.running = True
        self.handle_client(client)

    def stop(self):
        """
        Stop the server and close the connection.
        """
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        self.server.close()