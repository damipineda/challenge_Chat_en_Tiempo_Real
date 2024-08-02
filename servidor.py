import socket
import threading

# Función para manejar la comunicación con un cliente
def manejar_cliente(socket_cliente):
    while True:
        try:
            # Recibir mensaje del cliente
            mensaje = socket_cliente.recv(1024).decode('utf-8')
            if mensaje:
                # Imprimir el mensaje en el servidor
                print(f"Cliente: {mensaje}")
                # Enviar el mensaje a todos los demás clientes
                enviar_a_todos(mensaje, socket_cliente)
            else:
                # Si no se recibe mensaje, remover al cliente
                remover(socket_cliente)
                break
        except:
            continue

# Función para enviar mensajes a todos los clientes excepto al remitente
def enviar_a_todos(mensaje, socket_cliente):
    for cliente in clientes:
        if cliente != socket_cliente:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                remover(cliente)

# Función para remover un cliente de la lista de clientes conectados
def remover(socket_cliente):
    if socket_cliente in clientes:
        clientes.remove(socket_cliente)

# Configuración del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enlazar el servidor a la dirección y puerto especificados
servidor.bind(('0.0.0.0', 5555))  # Usar el puerto 5555
servidor.listen(100)

# Lista para almacenar los clientes conectados
clientes = []

print("Servidor de chat iniciado...")

# Bucle para aceptar conexiones de clientes
while True:
    socket_cliente, direccion_cliente = servidor.accept()
    clientes.append(socket_cliente)
    print(f"{direccion_cliente} conectado")
    # Crear un hilo para manejar la comunicación con el cliente
    threading.Thread(target=manejar_cliente, args=(socket_cliente,)).start()
