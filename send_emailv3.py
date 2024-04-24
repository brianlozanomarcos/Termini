import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet

def decrypt_password():
    # Leer la clave desde el archivo
    with open('clave.key', 'rb') as key_file:
        key = key_file.read()

    # Cargar la clave
    cipher_suite = Fernet(key)

    # Leer la contraseña cifrada desde el archivo
    with open('contraseña.enc', 'rb') as password_file:
        encrypted_password = password_file.read()

    # Descifrar la contraseña
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def send_email():
    # Configuración del servidor SMTP
    smtp_server = 'mail.gmx.es'
    smtp_port = 587  # Puerto SMTP (normalmente 587 para TLS)
    smtp_username = 'termini.1@gmx.es'
    smtp_password = decrypt_password()

    # Detalles del mensaje
    sender_email = 'termini.1@gmx.es'
    receiver_email = 'termini.1@gmx.es'
    subject = 'Informe de Información del Equipo'
    body = 'Adjunto encontrarás el informe de la información del equipo.'

    # Crear el objeto del mensaje
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Adjuntar el cuerpo del mensaje
    message.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo informacion_equipo.txt
    filename = 'informacion_equipo.txt'
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    message.attach(part)

    # Iniciar la conexión SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Habilitar el cifrado TLS
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print('Correo enviado exitosamente.')

if __name__ == "__main__":
    send_email()
