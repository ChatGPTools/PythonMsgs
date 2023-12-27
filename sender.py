import socket
import keyboard

def send_messages(target_ip, target_port):
    # Crea un socket del client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connetti al server
    client_socket.connect((target_ip, target_port))
    print(f"Connesso al server {target_ip}:{target_port}")

    while True:
        print("Opzioni:")
        print("1. Invia un messaggio")
        print("2. Esci")

        choice = input("Scelta: ")

        if choice == "1":
            try:
                # Inserisci il messaggio da inviare
                message = input("Inserisci il messaggio: ")

                # Invia il messaggio al server
                client_socket.send(message.encode("utf-8"))
            except:
                pass  # Gestisce eventuali errori durante l'invio del messaggio
        elif choice == "2":
            # Invia un messaggio di uscita e chiudi la connessione
            client_socket.send("exit".encode("utf-8"))
            break
        else:
            print("Scelta non valida. Riprova.")

        # Controlla se è stato premuto un tasto per interrompere manualmente l'esecuzione
        if keyboard.is_pressed("q"):
            break

    # Chiudi la connessione con il server
    client_socket.close()

if __name__ == "__main__":
    target_ip = input("Inserisci l'indirizzo IP del server: ")
    target_port = int(input("Inserisci la porta del server: "))
    send_messages(target_ip, target_port)
