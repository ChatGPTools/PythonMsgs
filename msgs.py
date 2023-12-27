import socket
import base64
import signal
import sys

class MessageEncoder:
    def encode(self, message, encoding_method):
        if encoding_method == "base64":
            return base64.b64encode(message.encode("utf-8")).decode("utf-8")
        elif encoding_method == "utf-8":
            return message
        else:
            raise ValueError("Metodo di codifica non valido")

    def decode(self, encoded_message, encoding_method):
        if encoding_method == "base64":
            return base64.b64decode(encoded_message).decode("utf-8")
        elif encoding_method == "utf-8":
            return encoded_message
        else:
            raise ValueError("Metodo di decodifica non valido")

class ChatServer:
    def __init__(self, listen_ip, listen_port, encoding_method):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((listen_ip, listen_port))
        self.server_socket.listen(1)
        print(f"In ascolto su {listen_ip}:{listen_port}")

        self.client_socket, addr = self.server_socket.accept()
        print(f"Connessione accettata da {addr[0]}:{addr[1]}")

        self.message_encoder = MessageEncoder()
        self.encoding_method = encoding_method

    def receive_message(self):
        try:
            encoded_message = self.client_socket.recv(1024).decode("utf-8")
            decoded_message = self.message_encoder.decode(encoded_message, self.encoding_method)
            print(f"Ricevuto dal client: {decoded_message}")
        except Exception as e:
            print(f"Errore durante la ricezione del messaggio: {e}")

    def handle_user_input(self, choice):
        if choice == "1":
            self.receive_message()
        elif choice == "2":
            self.message_encoder_options()
        elif choice == "3":
            user_message = input("Inserisci il messaggio da inviare: ")
            encoded_message = self.message_encoder.encode(user_message, self.encoding_method)
            self.client_socket.send(encoded_message.encode("utf-8"))
        elif choice == "4":
            self.change_encoding_method()
        elif choice == "5":
            self.show_current_ip_and_port()
        elif choice == "6":
            self.client_socket.send("exit".encode("utf-8"))
            self.cleanup_and_exit()
        else:
            print("Scelta non valida. Riprova.")

    def message_encoder_options(self):
        sub_choice = input("1. Codifica\n2. Decodifica\nScelta: ")
        user_message = input("Inserisci il messaggio: ")

        if sub_choice == "1":
            encoded_message = self.message_encoder.encode(user_message, self.encoding_method)
            print(f"Messaggio codificato: {encoded_message}")
        elif sub_choice == "2":
            decoded_message = self.message_encoder.decode(user_message, self.encoding_method)
            print(f"Messaggio decodificato: {decoded_message}")
        else:
            print("Scelta non valida. Riprova.")

    def change_encoding_method(self):
        new_encoding_method = input("Inserisci il metodo di codifica/decodifica (base64/utf-8): ").lower()
        print(f"Metodo di codifica/decodifica cambiato a {new_encoding_method}")
        self.encoding_method = new_encoding_method

    def show_current_ip_and_port(self):
        print(f"Indirizzo IP attuale: {self.listen_ip}")
        print(f"Porta attuale: {self.listen_port}")

    def cleanup_and_exit(self):
        self.client_socket.close()
        self.server_socket.close()
        sys.exit(0)

class ChatClient:
    def __init__(self, server_ip, server_port, encoding_method):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))

        self.message_encoder = MessageEncoder()
        self.encoding_method = encoding_method

    def send_message(self, user_message):
        encoded_message = self.message_encoder.encode(user_message, self.encoding_method)
        self.client_socket.send(encoded_message.encode("utf-8"))

    def receive_message(self):
        try:
            encoded_message = self.client_socket.recv(1024).decode("utf-8")
            decoded_message = self.message_encoder.decode(encoded_message, self.encoding_method)
            print(f"Ricevuto dal server: {decoded_message}")
        except Exception as e:
            print(f"Errore durante la ricezione del messaggio: {e}")

    def handle_user_input(self, choice):
        if choice == "1":
            user_message = input("Inserisci il messaggio da inviare: ")
            self.send_message(user_message)
            if user_message.lower() == "exit":
                self.cleanup_and_exit()
        elif choice == "2":
            self.receive_message()
        elif choice == "3":
            self.client_socket.send("exit".encode("utf-8"))
            self.cleanup_and_exit()
        else:
            print("Scelta non valida. Riprova.")

    def cleanup_and_exit(self):
        self.client_socket.close()
        sys.exit(0)

def signal_handler(signal, frame):
    print("\nChiusura in corso...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Gestione del segnale Ctrl + C

    role = input("Sei il Server (S) o il Client (C)? ").upper()

    if role == "S":
        listen_ip = input("Inserisci l'indirizzo IP del server: ")
        listen_port = int(input("Inserisci la porta del server: "))
        encoding_method = input("Inserisci il metodo di codifica/decodifica (base64/utf-8): ").lower()

        server = ChatServer(listen_ip, listen_port, encoding_method)
        while True:
            print("\nOpzioni:")
            print("1. Ricevi un messaggio")
            print("2. Codifica/Decodifica messaggio")
            print("3. Invia un messaggio")
            print("4. Cambia metodo di codifica/decodifica")
            print("5. Mostra l'indirizzo IP e la porta attuali")
            print("6. Esci")

            user_choice = input("Scelta: ")
            server.handle_user_input(user_choice)

    elif role == "C":
        server_ip = input("Inserisci l'indirizzo IP del server: ")
        server_port = int(input("Inserisci la porta del server: "))
        encoding_method = input("Inserisci il metodo di codifica/decodifica (base64/utf-8): ").lower()

        client = ChatClient(server_ip, server_port, encoding_method)
        while True:
            print("\nOpzioni:")
            print("1. Invia un messaggio")
            print("2. Ricevi e mostra messaggi")
            print("3. Esci")

            user_choice = input("Scelta: ")
            client.handle_user_input(user_choice)

    else:
        print("Ruolo non valido. Scegli 'S' per Server o 'C' per Client.")
