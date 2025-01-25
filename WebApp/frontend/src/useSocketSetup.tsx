import { useEffect } from "react";
import socket from "./socket"

const useSocketSetup = () => {
    useEffect(() => {
        socket.connect();
        
        // return () => {
        //     socket.disconnect();
        // };

    }, []);
}

export default useSocketSetup;