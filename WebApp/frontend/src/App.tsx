import ToggleColorMode from './components/ToggleColorMode';
import useSocketSetup from "./useSocketSetup"
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { createContext, useMemo, useState } from "react"
import LiveChart from './components/LiveChart';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import SensorStatus from './components/SensorStatus';
import { Container, Grid, Typography } from '@mui/material';
import Chatbot from './components/chat';
import WiresharkGraph from './components/WiresharkGraph';
import Alerts from './components/Alerts';
import Dashboard from './components/Dashboard';

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

export default function App() {
  const [mode, setMode] = useState<'light' | 'dark'>('dark');
  
  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
      }}),
    [mode],
  );

  useSocketSetup();

  return (
    <>
      <ColorModeContext.Provider value={colorMode}>
        <ThemeProvider theme={theme}>
          <CssBaseline enableColorScheme />
          <Box sx={{display: 'flex', flexDirection: 'column', minHeight: "100vh", minWidth: "70%", paddingRight: "40px"}}>
            <Box sx={{ position: 'relative', zIndex: 1000 }}>
              <ToggleColorMode />
            </Box>
            {/* <Counter/> */}
            <Grid container spacing={0} direction="column" alignItems="center" justifyContent="center" sx={{ paddingTop: '20px', position: 'sticky', top: 0, backgroundColor: theme.palette.background.default }}>
                <h1>negative<span style={{ animation: 'blink 1s step-end infinite' }}>_</span></h1>

            <style>
              {`
                @keyframes blink {
                  from, to {
                    visibility: hidden;
                  }
                  50% {
                    visibility: visible;
                  }
                }
              `}
            </style>
            </Grid>

            <Box sx={{ position: 'fixed', top: 150, right: 20 }}>
              <Chatbot />
            </Box>

            <Box sx={{ height: 'auto', width: '70%', overflow: 'auto', marginTop: '2em' }}>
              <Dashboard/>
              <Alerts/>
              <WiresharkGraph />
            </Box>

            <Box sx={{ height: 'auto', width: '70%', overflow: 'auto' }}>
              <Typography variant="h6" justifyContent="center" gutterBottom sx={{ textAlign: 'center' }}>
                Live Sensor Data
              </Typography>
              <Grid container justifyContent="center" alignItems="center" sx={{ flex: 1 }}>
                <SensorStatus />              
              </Grid>
              <Grid container justifyContent="center" alignItems="center">
                <Grid marginTop="2em" container columns={2} direction="row" > 
                  <LiveChart title="Temperature" dataKey="temperature"/>
                  <LiveChart title="CO2" dataKey="co2"/>
                </Grid >
                <Grid marginTop="2em" container columns={2} direction="row" >
                  <LiveChart title="Sound Level" dataKey="soundlevel"/>
                  <LiveChart title="Volatile Organic Compounds" dataKey="voc"/>
                </Grid >
              </Grid>
            </Box>
          </Box>
        </ThemeProvider>
      </ColorModeContext.Provider>
    </>
  );
}