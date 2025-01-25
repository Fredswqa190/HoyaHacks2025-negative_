import ToggleColorMode from './components/ToggleColorMode';
import useSocketSetup from "./useSocketSetup"
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { createContext, useMemo, useState } from "react"
import LiveChart from './components/LiveChart';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import SensorStatus from './components/SensorStatus';
import { Container, Grid, Typography, Paper, Fab } from '@mui/material';
import Chatbot from './components/chat';
import WiresharkGraph from './components/WiresharkGraph';
import Alerts from './components/Alerts';
import Dashboard from './components/Dashboard';
import ChatIcon from '@mui/icons-material/Chat';
import CloseIcon from '@mui/icons-material/Close';

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

export default function App() {
  const [mode, setMode] = useState<'light' | 'dark'>('dark');
  const [chatOpen, setChatOpen] = useState(false);
  
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
          <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: "100vh", paddingRight: "40px", backgroundColor: theme.palette.background.default }}>
            <Box sx={{ position: 'relative', zIndex: 1000, padding: '10px' }}>
              <ToggleColorMode />
            </Box>
            <Grid container spacing={0} direction="column" alignItems="center" justifyContent="center" sx={{ paddingTop: '20px', position: 'sticky', top: 0, backgroundColor: theme.palette.background.default }}>
                <Typography variant="h2" component="h1" sx={{ fontWeight: 'bold', textAlign: 'center' }}>
                  negative<span style={{ animation: 'blink 1s step-end infinite' }}>_</span>
                </Typography>
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

            <Box sx={{ position: 'fixed', bottom: 20, right: 20 }}>
              <Fab color="primary" onClick={() => setChatOpen(!chatOpen)}>
                {chatOpen ? <CloseIcon /> : <ChatIcon />}
              </Fab>
              {chatOpen && (
                <Box sx={{ position: 'fixed', bottom: 80, right: 20, width: 300, height: 400, backgroundColor: 'white', boxShadow: 3, borderRadius: 2, overflow: 'hidden' }}>
                  <Chatbot />
                </Box>
              )}
            </Box>

            <Container sx={{ marginTop: '2em', marginBottom: '2em' }}>
              <Paper elevation={3} sx={{ padding: '20px', marginBottom: '2em' }}>
                <Dashboard />
              </Paper>
              <Paper elevation={3} sx={{ padding: '20px', marginBottom: '2em' }}>
                <Alerts />
              </Paper>
              <Paper elevation={3} sx={{ padding: '20px', marginBottom: '2em' }}>
                <WiresharkGraph />
              </Paper>
            </Container>

            <Container sx={{ marginBottom: '2em' }}>
              <Typography variant="h6" gutterBottom sx={{ textAlign: 'center' }}>
                Live Sensor Data
              </Typography>
              <Grid container justifyContent="center" alignItems="center" sx={{ flex: 1 }}>
                <SensorStatus />
              </Grid>
              <Grid container justifyContent="center" alignItems="center">
                <Grid marginTop="2em" container columns={2} direction="row" spacing={2}>
                  <Grid item xs={12} md={6}>
                    <LiveChart title="Temperature" dataKey="temperature" />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <LiveChart title="CO2" dataKey="co2" />
                  </Grid>
                </Grid>
                <Grid marginTop="2em" container columns={2} direction="row" spacing={2}>
                  <Grid item xs={12} md={6}>
                    <LiveChart title="Sound Level" dataKey="soundlevel" />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <LiveChart title="Volatile Organic Compounds" dataKey="voc" />
                  </Grid>
                </Grid>
              </Grid>
            </Container>
          </Box>
        </ThemeProvider>
      </ColorModeContext.Provider>
    </>
  );
}