import React from 'react';
import { Grid, Box, Typography } from '@mui/material';
import WiresharkPredictions from './WiresharkPredictions';

const Dashboard: React.FC = () => {
  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h6" gutterBottom>
        SIEM Dashboard
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <WiresharkPredictions />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;