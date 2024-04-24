import os
import socket
import uuid

def get_system_info():
    system_info = {}

    # Nombre de usuario
    system_info['username'] = os.getlogin()

    # Dirección IP
    system_info['ip_address'] = socket.gethostbyname(socket.gethostname())

    # Dirección MAC
    system_info['mac_address'] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])

    # Nombre del host
    system_info['hostname'] = socket.gethostname()

    return system_info

def save_to_file(info):
    with open('informacion_equipo.txt', 'w') as file:
        for key, value in info.items():
            file.write(f"{key}: {value}\n")

if __name__ == "__main__":
    system_info = get_system_info()
    print("Información del sistema:")
    for key, value in system_info.items():
        print(f"{key}: {value}")

    save_to_file(system_info)
    print("La información ha sido guardada en el archivo 'informacion_equipo.txt'.")
