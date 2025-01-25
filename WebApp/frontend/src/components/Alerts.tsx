import React, { useEffect, useState } from 'react';
import { Box, Typography, List, ListItem, ListItemText } from '@mui/material';
import socket from '../socket';
import StatusLabel from './StatusLabel';

const GREEN = "#0be881";
const RED = "#ff3f34";

const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [currentTime, setCurrentTime] = useState<string>(new Date().toLocaleTimeString());

  useEffect(() => {
    socket.on('alert', (alert) => {
      setAlerts((prevAlerts) => [alert, ...prevAlerts]);
    });

    return () => {
      socket.off('alert');
    };
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h6" gutterBottom>
        Real-time Alerts
      </Typography>
      {alerts.length === 0 ? (
        <StatusLabel label={currentTime} value="No alerts." valueColor={GREEN} />
      ) : (
        <List>
          {alerts.map((alert, index) => (
            <ListItem key={index}>
              <ListItemText primary={alert.message} secondary={alert.timestamp} />
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default Alerts;