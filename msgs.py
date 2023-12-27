import socket
import keyboard
import base64
import signal
import sys

def encode_message(message, encoding_method):
    if encoding_method == "base64":
        return base64.b64encode(message.encode("utf-8")).decode("utf-8")
    elif encoding_method == "utf-8":
        return message
    else:
        raise ValueError("Metodo di codifica non valido")

def decode_message(encoded_message, encoding_method):
    if encoding_method == "base64":
        return base64.b64decode(encoded_message).decode("utf-8")
    elif encoding_method == "utf-8":
        return encoded_message
    else:
        raise ValueError("Metodo di decodifica non valido")

def receive_messages(listen_ip, listen_port, encoding_method):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_ip, listen_port))
    server_socket.listen(1)
    print(f"In ascolto su {listen_ip}:{listen_port}")

    client_socket, addr = server_socket.accept()
    print(f"Connessione accettata da {addr[0]}:{addr[1]}")

    while True:
        print("Opzioni:")
        print("1. Ricevi un messaggio")
        print("2. Codifica/Decodifica messaggio")
        print("3. Invia un messaggio")
        print("4. Cambia metodo di codifica/decodifica")
        print("5. Esci")

        choice = input("Scelta: ")

        if choice == "1":
            try:
                encoded_message = client_socket.recv(1024).decode("utf-8")
                decoded_message = decode_message(encoded_message, encoding_method)
                print(f"Ricevuto dal client: {decoded_message}")
            except Exception as e:
                print(f"Errore durante la ricezione del messaggio: {e}")
        elif choice == "2":
            sub_choice = input("1. Codifica\n2. Decodifica\nScelta: ")
            user_message = input("Inserisci il messaggio: ")

            if sub_choice == "1":
                encoded_message = encode_message(user_message, encoding_method)
                print(f"Messaggio codificato: {encoded_message}")
            elif sub_choice == "2":
                decoded_message = decode_message(user_message, encoding_method)
                print(f"Messaggio decodificato: {decoded_message}")
            else:
                print("Scelta non valida. Riprova.")
        elif choice == "3":
            user_message = input("Inserisci il messaggio da inviare: ")
            encoded_message = encode_message(user_message, encoding_method)
            client_socket.send(encoded_message.encode("utf-8"))
        elif choice == "4":
            encoding_method = input("Inserisci il metodo di codifica/decodifica (base64/utf-8): ").lower()
            print(f"Metodo di codifica/decodifica cambiato a {encoding_method}")
        elif choice == "5":
            client_socket.send("exit".encode("utf-8"))
            break
        else:
            print("Scelta non valida. Riprova.")

        if keyboard.is_pressed("q"):
            break

    client_socket.close()
    server_socket.close()

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
        receive_messages(listen_ip, listen_port, encoding_method)
    elif role == "C":
        server_ip = input("Inserisci l'indirizzo IP del server: ")
        server_port = int(input("Inserisci la porta del server: "))
        encoding_method = input("Inserisci il metodo di codifica/decodifica (base64/utf-8): ").lower()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        while True:
            user_message = input("Inserisci il messaggio da inviare: ")
            encoded_message = encode_message(user_message, encoding_method)
            client_socket.send(encoded_message.encode("utf-8"))

            if user_message.lower() == "exit":
                break

            try:
                encoded_message = client_socket.recv(1024).decode("utf-8")
                decoded_message = decode_message(encoded_message, encoding_method)
                print(f"Ricevuto dal server: {decoded_message}")
            except Exception as e:
                print(f"Errore durante la ricezione del messaggio: {e}")

            if keyboard.is_pressed("q"):
                break

        client_socket.close()
    else:
        print("Ruolo non valido. Scegli 'S' per Server o 'C' per Client.")
