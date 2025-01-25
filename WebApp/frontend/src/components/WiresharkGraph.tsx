import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Box, Typography } from '@mui/material';
import socket from '../socket';

interface PacketData {
  time: string;
  packets: number;
}

const WiresharkGraph: React.FC = () => {
  const [data, setData] = useState<PacketData[]>([]);

  useEffect(() => {
    const handlePacketCount = (packetCount: any) => {
      const currentTime = new Date().toLocaleTimeString();
      setData((prevData) => {
        const newData = [...prevData, { time: currentTime, packets: packetCount }];
        if (newData.length > 10) {
          newData.shift();
        }
        return newData;
      });
    };

    socket.on('packet_count', handlePacketCount);

    return () => {
      socket.off('packet_count', handlePacketCount);
    };
  }, []);

  return (
    <Box sx={{ width: '100%', padding: 2 }}>
      <Typography variant="h6" justifyContent="center" gutterBottom sx={{ textAlign: 'center' }}>
        Wireshark Data Graph
      </Typography>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis dataKey="packets" />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="packets" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default WiresharkGraph;