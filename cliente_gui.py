import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Función para recibir mensajes del servidor
def recibir_mensajes(socket_cliente, display_chat):
    while True:
        try:
            mensaje = socket_cliente.recv(1024).decode('utf-8')
            if mensaje:
                # Mostrar el mensaje en la interfaz gráfica
                display_chat.config(state=tk.NORMAL)
                display_chat.insert(tk.END, f"Servidor: {mensaje}\n")
                display_chat.config(state=tk.DISABLED)
                display_chat.yview(tk.END)
        except:
            print("Conexión cerrada")
            socket_cliente.close()
            break

# Función para enviar mensajes al servidor
def enviar_mensaje(socket_cliente, entrada_mensaje, display_chat):
    mensaje = entrada_mensaje.get()
    # Mostrar el mensaje en la interfaz gráfica
    display_chat.config(state=tk.NORMAL)
    display_chat.insert(tk.END, f"Tú: {mensaje}\n")
    display_chat.config(state=tk.DISABLED)
    display_chat.yview(tk.END)
    socket_cliente.send(mensaje.encode('utf-8'))
    entrada_mensaje.delete(0, tk.END)

# Función para inicializar el cliente y la interfaz gráfica
def iniciar_cliente():
    # Crear el socket del cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 5555))  # Usar el puerto 5555

    # Configuración de la interfaz gráfica
    raiz = tk.Tk()
    raiz.title("Chat Cliente")

    # Área de texto con desplazamiento para mostrar los mensajes del chat
    display_chat = scrolledtext.ScrolledText(raiz, wrap=tk.WORD, state=tk.DISABLED)
    display_chat.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    # Campo de entrada para escribir mensajes
    entrada_mensaje = tk.Entry(raiz, width=50)
    entrada_mensaje.pack(padx=20, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

    # Botón para enviar mensajes
    boton_enviar = tk.Button(raiz, text="Enviar", command=lambda: enviar_mensaje(cliente, entrada_mensaje, display_chat))
    boton_enviar.pack(padx=20, pady=5, side=tk.RIGHT)

    # Crear un hilo para recibir mensajes del servidor
    threading.Thread(target=recibir_mensajes, args=(cliente, display_chat)).start()

    raiz.mainloop()

if __name__ == "__main__":
    iniciar_cliente()
