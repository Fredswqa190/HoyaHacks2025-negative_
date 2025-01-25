import { io } from "socket.io-client";

const socket = io("localhost:4003/", {
    transports: ["websocket"],
    autoConnect: false,
    cors: {
        origin: "http://localhost:3000/",
    },
});

export default socket