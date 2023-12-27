import socket
import keyboard

def receive_messages(listen_ip, listen_port):
    # Crea un socket del server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa il socket all'indirizzo IP e alla porta
    server_socket.bind((listen_ip, listen_port))

    # Abilita il server per accettare connessioni
    server_socket.listen(1)
    print(f"In ascolto su {listen_ip}:{listen_port}")

    # Accetta una connessione dal client
    client_socket, addr = server_socket.accept()
    print(f"Connessione accettata da {addr[0]}:{addr[1]}")

    while True:
        print("Opzioni:")
        print("1. Ricevi un messaggio")
        print("2. Esci")

        choice = input("Scelta: ")

        if choice == "1":
            try:
                # Ricevi il messaggio dal client
                message = client_socket.recv(1024).decode("utf-8")

                # Stampa il messaggio ricevuto
                print(f"Ricevuto dal client: {message}")
            except:
                pass  # Gestisce eventuali errori durante la ricezione del messaggio
        elif choice == "2":
            # Invia un messaggio di uscita e chiudi la connessione
            client_socket.send("exit".encode("utf-8"))
            break
        else:
            print("Scelta non valida. Riprova.")

        # Controlla se è stato premuto un tasto per interrompere manualmente l'esecuzione
        if keyboard.is_pressed("q"):
            break

    # Chiudi la connessione con il client
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    listen_ip = input("Inserisci l'indirizzo IP del server: ")
    listen_port = int(input("Inserisci la porta del server: "))
    receive_messages(listen_ip, listen_port)
