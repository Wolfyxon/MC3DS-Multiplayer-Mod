import subprocess, os, socket, requests

if __name__ != "__main__":
    print(f"{os.path.basename(__file__)} is not meant to be used as a module")
    exit(1)

crypt_path = 'crypt.exe'

if os.path.isfile(crypt_path):
    keys_call = subprocess.run([crypt_path, 'generate_key'], capture_output=True)
    key = keys_call.stdout.decode('utf-8')
else:
    print(f'"{crypt_path}" not found')
    exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8000

response = requests.get('https://api.ipify.org')
public_ip = response.text
print(f"Your IP Address:   {public_ip}.")
print(f"Your Port Number:  {port}.")
print(f"Hostname:          {host}.\n")
server_socket.bind((host, port))
server_socket.listen(1)

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected User:    {addr}")

        data = client_socket.recv(1024)
        print(f'Received data:     {data.decode()}')

except KeyboardInterrupt:
    client_socket.send('Server was Stopped Abruptly.\n')
    server_socket.close()