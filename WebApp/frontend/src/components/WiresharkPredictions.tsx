import Box from '@mui/material/Box';
import StatusLabel from './StatusLabel';
import socket from '../socket';
import { useEffect, useState } from 'react';

const GREEN = "#0be881"
const RED = "#ff3f34"
const YELLOW = "#ffa801"

export default function WiresharkPredictions() {
    const [connectionStatus, setConnectionStatus] = useState(false);
    const [predictions, setPredictions] = useState("");
    const [alert, setAlert] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
    const [alertType, setAlertType] = useState("");
    const [alertTime, setAlertTime] = useState("");
    const [alertSource, setAlertSource] = useState("");
    const [alertDestination, setAlertDestination] = useState("");
    const [alertProtocol, setAlertProtocol] = useState("");
    const [alertInfo, setAlertInfo] = useState("");
    const [alertSeverity, setAlertSeverity] = useState("");
    const [alertCategory, setAlertCategory] = useState("");
    const [alertSignature, setAlertSignature] = useState("");
    const [alertReference, setAlertReference] = useState("");
    const [alertResolution, setAlertResolution] = useState("");

    useEffect(() => {
        // Connect to the socket
        socket.on('connect', () => {
            setConnectionStatus(true);
        });

        socket.on('disconnect', () => {
            setConnectionStatus(false);
        });

        // Listen for wireshark data
        socket.on('wireshark_data', (data) => {
            setPredictions(data);
        });

        // Listen for dangerous data
        socket.on('dangerous', (data) => {
            setAlert(data);
        });

        // Clean up the effect
        return () => {
            socket.off('connect');
            socket.off('disconnect');
            socket.off('wireshark_data');
            socket.off('dangerous');
        };
    }, []);

    return (
        <Box gap={4} p={2} display="flex" flexWrap={"wrap"}>
            <StatusLabel label="Wireshark Status"value={connectionStatus ? "Connected" : "Disconnected"} valueColor={connectionStatus ? GREEN : RED} />
            <StatusLabel label="Alert" value={alert ? "Anomalous activity detected" : "No anomalous activity detected"} valueColor={alert ? RED : GREEN} />
        </Box>
    );
}