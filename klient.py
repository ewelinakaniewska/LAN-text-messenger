import socket
import threading
import time
import os

# Konfiguracja klienta
HOST = ''
PORT = 0

if HOST == '':
    HOST = input("Podaj adres serwera\n")
if PORT == 0:
    PORT = int(input("Podaj numer portu\n")) 

# Funkcja odbierająca wiadomości z serwera
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Serwer zamknął połączenie.")
                break
            if '\x00' not in message:
                print(message)
        except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
            print(f"Połączenie zostało utracone")
            break
        except Exception as e:
            print(f"Niespodziewany wyjątek")
            break
    client_socket.close()
    os._exit(0)

# Funkcja do sprawdzania stanu połączenia

def keep_alive(client_socket):
    while True:
        try:
            client_socket.send(b'\x00') 
            time.sleep(5)
        except (BrokenPipeError, ConnectionResetError, OSError):
            client_socket.close()
            os._exit(0)

# Główna funkcja klienta
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client_socket.settimeout(20) 
    
    try:
        client_socket.connect((HOST, PORT))
    except (ConnectionRefusedError, OSError):
        print(f"Nie można połączyć się z serwerem {HOST}:{PORT}")
        os._exit(0)
    try: 
        username = input("Podaj nazwę użytkownika: ")
        client_socket.send(username.encode('utf-8'))
    
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        keep_alive_thread = threading.Thread(target=keep_alive, args=(client_socket,))
        keep_alive_thread.start()
    
   
        while True:
            message = input()
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        pass  
    except Exception as e:
        print(f"Wystąpił nieoczekiwany wyjątek: {e}")
    finally:
        client_socket.close()
        os._exit(0)

if __name__ == "__main__":
    main()
