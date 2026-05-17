import socket
import threading
import signal
import select
import time
import os

# Konfiguracja serwera
HOST = ''
PORT = 0

if HOST == '':
    HOST = input("Podaj adres serwera\n")
if PORT == 0:
    PORT = int(input("Podaj numer portu\n")) 

clients = []
client_names = {}
log_file = "server_log.txt"
server = None
lock = threading.Lock()  
threads = []

# Funkcja obsługująca komunikację z klientem
def handle_client(client_socket, client_address):
    print(f"Nowe połączenie od {client_address}")
    with open(log_file, 'a') as log:
        log.write(f"Nowe połączenie od {client_address}\n")
        
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if '\x00' not in message:
                print(f"Otrzymano wiadomość od {client_address}: {message}")
                with open(log_file, 'a') as log:
                    log.write(f"{client_address}: {message}\n")
                broadcast_message(f"{client_names[client_socket]}: {message}", client_socket)
    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, socket.timeout, OSError):
        pass
    finally:
        with lock:
            clients.remove(client_socket)
        client_socket.close()
        print(f"Połączenie z {client_address} zakończone")
        with open(log_file, 'a') as log:
            log.write(f"Połączenie z {client_address} zakończone\n")

# Funkcja rozsyłająca wiadomości do wszystkich klientów
def broadcast_message(message, exclude_socket):
    with lock:
        for client in clients:
            if client != exclude_socket:
                try:
                    client.send(message.encode('utf-8'))
                except BrokenPipeError:
                    pass

# Funkcja obsługująca przerwanie z klawiatury
def signal_handler(sig, frame):
    print("\nPrzerywam działanie serwera...")
    with open(log_file, 'a') as log:
        log.write("Serwer zakończył działanie\n")
    with lock:
        for client in clients:
            client.close()
    if server:
        server.close()
    for t in threads:
        t.join()
    os._exit(0)
    
# Funkcja do sprawdzania stanu połączenia
def keep_alive(client_socket):
    while True:
        try:
            client_socket.send(b'\x00')  
            time.sleep(5)
        except Exception:
            break  

# Główna funkcja serwera
def main():
    global server
    try:
        signal.signal(signal.SIGINT, signal_handler)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
    except OSError:
        print("Błędny port, port jest zajęty lub adres jest błędny")
        os._exit(0)
    
    print(f"Serwer nasłuchuje na {HOST}:{PORT}")

    while True:
        try:
            readable, _, _ = select.select([server], [], [], 1.0)
            if server in readable:
                client_socket, client_address = server.accept()
                client_socket.settimeout(20)
                with lock:
                    clients.append(client_socket)
                client_names[client_socket] = client_socket.recv(1024).decode('utf-8')
                client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_handler.start()
                
                threads.append(client_handler)

                keep_alive_thread = threading.Thread(target=keep_alive, args=(client_socket,))
                keep_alive_thread.start()
                
                threads.append(keep_alive_thread)
        except select.error:
            break

if __name__ == "__main__":
    main()
