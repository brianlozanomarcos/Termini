import subprocess

# Ejecutar el script de recolección de información
print("Ejecutando el script de recolección de información...")
subprocess.run(["python", "recollect.py"])

# Una vez que el script de recolección de información haya terminado,
# ejecutar el script de envío de correo
print("Ejecutando el script de envío de correo...")
subprocess.run(["python", "send_emailv3.py"])
