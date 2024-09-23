import socketio
import tkinter as tk
from threading import Thread

# Crear una instancia del cliente de Socket.IO
sio = socketio.Client()

# Crear la aplicación GUI
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat en Python")
        
        # Área de texto para mostrar mensajes
        self.chat_area = tk.Text(root, state='disabled', width=50, height=20)
        self.chat_area.pack(pady=10)
        
        # Entrada de texto para escribir mensajes
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(side='left', padx=10)
        
        # Botón para enviar mensajes
        self.send_button = tk.Button(root, text="Enviar", command=self.send_message)
        self.send_button.pack(side='left')
        
        # Botón para listar usuarios
        self.list_button = tk.Button(root, text="Listar Usuarios", command=self.list_users)
        self.list_button.pack(side='right')
    
    # Función para enviar mensajes al servidor
    def send_message(self):
        message = self.message_entry.get()
        if message:
            sio.emit('chat message', message)
            self.message_entry.delete(0, tk.END)
    
    # Función para listar usuarios conectados
    def list_users(self):
        sio.emit('list users')

    # Función para agregar mensajes a la ventana del chat
    def display_message(self, user, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{user}: {message}\n")
        self.chat_area.config(state='disabled')

    # Función para mostrar la lista de usuarios conectados
    def display_user_list(self, users):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"Usuarios conectados: {', '.join(users)}\n")
        self.chat_area.config(state='disabled')

# Eventos de Socket.IO
@sio.event
def connect():
    print("Conexión exitosa al servidor")
    username = input("Ingresa tu nombre de usuario: ")
    sio.emit('new user', username)

@sio.on('chat message')
def on_message(data):
    app.display_message(data['user'], data['message'])

@sio.on('user list')
def on_user_list(users):
    app.display_user_list(users)

@sio.event
def disconnect():
    print("Desconectado del servidor")

# Función para manejar la conexión en un hilo separado
def connect_to_server():
    host = input("Ingresa la IP del servidor (e.g., localhost): ")
    port = input("Ingresa el puerto del servidor (e.g., 3000): ")
    
    try:
        sio.connect(f'http://{host}:{port}')
    except Exception as e:
        print(f"No se pudo conectar al servidor: {e}")

if __name__ == '__main__':
    # Crear la ventana de Tkinter
    root = tk.Tk()
    app = ChatApp(root)
    
    # Iniciar el hilo para la conexión con el servidor
    Thread(target=connect_to_server).start()
    
    # Ejecutar la interfaz gráfica
    root.mainloop()
