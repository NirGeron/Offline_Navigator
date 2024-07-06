import socket
import csv

def read_csv_lines(file_path, start_line, num_lines):
    """Reads a specified number of lines from a CSV file starting from a given line."""
    lines = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for _ in range(start_line):
                next(reader, None)  # Skip lines up to start_line
            for _ in range(num_lines):
                lines.append(next(reader))
    except StopIteration:
        print(f"Reached end of file, returning {len(lines)} lines.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return lines

def start_server(file_path, num_lines, host='127.0.0.1', port=65432):
    """Starts a TCP server to send lines from a CSV file to connected clients in batches."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f'Server listening on {host}:{port}')

        start_line = 0  # Initial start line

        while True:
            client_socket, addr = server_socket.accept()
            print(f'Connected by {addr}')

            try:
                lines = read_csv_lines(file_path, start_line, num_lines)
                if not lines:
                    print("All lines have been sent. Closing server.")
                    break  # Exit if no more lines to send

                response = "\n".join([",".join(line) for line in lines])
                client_socket.sendall(response.encode())
                start_line += 1  # Move to the next batch start point

            except Exception as e:
                print(f'Error: {e}')
            finally:
                client_socket.close()

    except Exception as e:
        print(f'Error setting up server: {e}')
    finally:
        server_socket.close()

if __name__ == '__main__':
    file_path = 'gps.csv'  # Path to your CSV file
    num_lines = 5  # Number of lines to send in each batch
    start_server(file_path, num_lines)

