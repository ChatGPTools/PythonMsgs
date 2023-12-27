# Chat Server e Client in Python

Questo script Python fornisce un'applicazione di chat a riga di comando con funzionalità di server e client. L'applicazione consente agli utenti di scambiare messaggi tra un server e diversi client utilizzando i socket.

## Funzionalità

- **Interazione Server-Client:** Stabilisce la comunicazione tra un server e diversi client.
- **Codifica dei Messaggi:** Supporta la codifica dei messaggi utilizzando Base64 o UTF-8.
- **Selezione Dinamica della Codifica:** Gli utenti possono scegliere il metodo di codifica durante l'esecuzione.
- **Chiusura Pulita:** Gestisce il segnale di interruzione (Ctrl + C) per una chiusura corretta.

## Prerequisiti

1. **Installazione di Python:** Assicurarsi che Python sia installato sul sistema. È possibile scaricare l'ultima versione da [python.org](https://www.python.org/).
   
2. **Librerie Necessarie:** Installare le librerie Python necessarie eseguendo il seguente comando:
   ```bash
   pip install keyboard

## Utilizzo

**Clonare il repository:**
```bash
git clone https://github.com/ChatGPTools/PythonMsgs.git
```

**Navigare nella directory del progetto**

**Eseguire il server:**
```bash
python msgs.py
```
**Seguire le istruzioni a schermo per avviare il server.**

**Eseguire il client su un'altra macchina (o sulla stessa macchina con un terminale diverso):**
```bash
python msgs.py
```

**Inserire l'indirizzo IP del server e la porta quando richiesto.**
**Seguire le istruzioni a schermo per interagire con l'applicazione di chat.**
