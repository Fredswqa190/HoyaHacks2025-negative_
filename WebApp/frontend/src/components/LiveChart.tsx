import { LineChart } from '@mui/x-charts/LineChart';
import Box from '@mui/material/Box';
import socket from '../socket';
import { useState, useEffect } from 'react';

interface LiveChartProps {
    title: string
    dataKey: string
}

export default function LiveChart(props: LiveChartProps) {
    const [times, setTimes] = useState([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]);
    const [lastTime, setLastTime] = useState(new Date().getTime());
    const [yAxis, setYAxis] = useState([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]);

    useEffect(() => {
        socket.on("sensor_data", (data) => {
            const newYAxis = yAxis;
            newYAxis.shift();
            newYAxis.push(data[props.dataKey])

            const currentTime = new Date().getTime();
            const secs = Math.round((currentTime - lastTime) / 1000)
            const newTimes = times;
            newTimes.shift()
            newTimes.push(secs)

            setTimes(newTimes);
            setLastTime(currentTime);
            setYAxis(newYAxis);
        });

        return () => {
            socket.off("sensor_data");
        }

    }, [])

    return (
        <Box p={2} sx={{display: 'flex', flexDirection: 'column'}}>
            <h3>{props.title}</h3>
            <LineChart
                xAxis={[{ data: times }]}
                series={[
                    {
                    data: yAxis,
                    area: true,
                    },
                ]}
                width={500}
                height={300}
                grid={{ vertical: true, horizontal: true }}
            />
        </Box>
    );
}