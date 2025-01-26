'use client'

import ToggleColorMode from './components/ToggleColorMode';
import { createContext, useMemo, useState } from "react"
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box, Grid, Typography, Menu, MenuItem, IconButton } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import MenuIcon from '@mui/icons-material/Menu';

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

export default function Home() {

  const [mode, setMode] = useState<'light' | 'dark'>('dark');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

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
            <IconButton edge="start" color="inherit" aria-label="menu" onClick={handleMenuOpen}>
              <MenuIcon />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItem onClick={handleMenuClose}>
              <a href="https://github.com/Fredswqa190/HoyaHacks2025-negative_" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
                Download
              </a>
              </MenuItem>
            </Menu>
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
                    opacity: 1;
                  }
                  50% {
                    opacity: 0;
                  }
                }
              `}
            </style>
            
            <Grid item xs={12} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '50vh' }}>
                <Grid container direction="column" alignItems="center" justifyContent="center">
                <Typography variant="h3" component="h2" sx={{ fontWeight: 'bold', textAlign: 'center' }}>
                  The next generation of security<span style={{ animation: 'blink 1s step-end infinite' }}>_</span>
                </Typography>
                <Typography variant="h6" component="h3" sx={{ textAlign: 'center', marginTop: '20px' }}>
                  With physical and digital security in mind, negative_ helps you understand both your network and your physical environment.
                </Typography>
                <Grid item></Grid>
                  <a href="https://github.com/Fredswqa190/HoyaHacks2025-negative_" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
                    <Box
                      component="button"
                      sx={{
                      backgroundColor: theme.palette.primary.main,
                      color: theme.palette.primary.contrastText,
                      padding: '10px 20px',
                      borderRadius: '5px',
                      textTransform: 'uppercase',
                      fontWeight: 'bold',
                      cursor: 'pointer',
                      marginTop: '20px', 
                      '&:hover': {
                        backgroundColor: theme.palette.primary.dark,
                      },
                      }}
                    >
                      Download
                    </Box>
                  </a>
                </Grid>
                </Grid>

          </Grid>
        </Box>
      </ThemeProvider>
    </ColorModeContext.Provider>
    </>
  );
}