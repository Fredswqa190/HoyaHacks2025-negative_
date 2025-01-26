'use client'

import Image from "next/image";
import ToggleColorMode from './components/ToggleColorMode';
import { createContext, useMemo, useState, useContext } from "react"
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box, Grid, Typography } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';


export const ColorModeContext = createContext({ toggleColorMode: () => {} });

export default function Home() {

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
          </Box>
        </ThemeProvider>
      </ColorModeContext.Provider>
    </>
    );
  }
