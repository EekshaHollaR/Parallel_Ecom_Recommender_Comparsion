import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container, Box, CssBaseline } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import HomePage from './pages/HomePage';
import RecommendationPage from './pages/RecommendationPage';
import PriceComparePage from './pages/PriceComparePage';

const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
        background: {
            default: '#f5f7fa',
        },
    },
});

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <Box sx={{ flexGrow: 1 }}>
                    <AppBar position="static">
                        <Toolbar>
                            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                                <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
                                    AI Recommender
                                </Link>
                            </Typography>
                            <Button color="inherit" component={Link} to="/">Home</Button>
                            <Button color="inherit" component={Link} to="/recommendations">Recommendations</Button>
                            <Button color="inherit" component={Link} to="/compare">Compare Prices</Button>
                        </Toolbar>
                    </AppBar>

                    <Container sx={{ py: 4 }}>
                        <Routes>
                            <Route path="/" element={<HomePage />} />
                            <Route path="/recommendations" element={<RecommendationPage />} />
                            <Route path="/compare" element={<PriceComparePage />} />
                        </Routes>
                    </Container>
                </Box>
            </Router>
        </ThemeProvider>
    );
}

export default App;
