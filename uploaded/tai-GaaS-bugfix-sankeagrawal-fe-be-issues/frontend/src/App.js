import React from 'react';
import Store from './Store';
import HomePage from './HomePage';
import { createTheme } from '@mui/material';
import { ThemeProvider } from '@emotion/react';

const theme = createTheme({
  palette: {primary: {main: "#FF4B4B"}},
  components: {
    MuiButtonBase: {
      defaultProps: {
        sx: {fontFamily: ['Roboto', 'Helvetica', 'Arial', 'sans-serif'].join(',')}
      }
    }
  }
});

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <Store>
        <HomePage />
      </Store>
    </ThemeProvider>
  );
}