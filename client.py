import socket


def request_csv_lines(host='127.0.0.1', port=65432):
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("No more data from server. Closing connection.")
                break
            print("Received data from server:")
            print(data)
        except Exception as e:
            print(f'Error: {e}')
        finally:
            client_socket.close()


if __name__ == '__main__':
    request_csv_lines()
