const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

let users = {};  // Guardar los usuarios conectados

// Ruta principal
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Evento de conexión
io.on('connection', (socket) => {
    console.log('Nuevo usuario conectado');

    // Evento cuando un usuario ingresa con su nombre
    socket.on('new user', (username) => {
        users[socket.id] = username;

        // Emitir un mensaje a todos informando que un nuevo usuario se ha conectado
        io.emit('chat message', { user: 'Sistema', message: `${username} se ha conectado.` });

        // Emitir la lista actualizada de usuarios
        io.emit('user list', Object.values(users));
    });

    // Evento para mensajes de chat
    socket.on('chat message', (msg) => {
        io.emit('chat message', { user: users[socket.id], message: msg });
    });

    // Evento para listar usuarios
    socket.on('list users', () => {
        socket.emit('user list', Object.values(users));
    });

    // Evento de desconexión
    socket.on('disconnect', () => {
        if (users[socket.id]) {
            const username = users[socket.id];
            console.log(`${username} se ha desconectado`);
            
            // Emitir un mensaje a todos informando que un usuario se ha desconectado
            io.emit('chat message', { user: 'Sistema', message: `${username} se ha desconectado.` });

            delete users[socket.id];

            // Emitir la lista actualizada de usuarios
            io.emit('user list', Object.values(users));
        }
    });
});

server.listen(3000, () => {
    console.log('Servidor escuchando en el puerto 3000');
});
