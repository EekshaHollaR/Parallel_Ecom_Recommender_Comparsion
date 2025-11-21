
import Dashboard from './pages/Dashboard';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import HomePage from './pages/HomePage';
import PriceComparePage from './pages/PriceComparePage';
import RecommendationPage from './pages/RecommendationPage';
import Login from './pages/Login';
import Signup from './pages/Signup';


function App() {
    return (
        <AuthProvider>
            <Router>
                <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: '#f5f5f5' }}>
                    <Navbar />
                    <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
                        <Routes>
                            <Route path="/" element={<HomePage />} />
                            <Route path="/compare" element={<PriceComparePage />} />
                            <Route path="/recommendations" element={<RecommendationPage />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/signup" element={<Signup />} />
                            <Route
                                path="/dashboard"
                                element={
                                    <ProtectedRoute>
                                        <Dashboard />
                                    </ProtectedRoute>
                                }
                            />
                        </Routes>
                    </Box>
                    {/* Footer could go here */}
                    <Box sx={{ p: 2, bgcolor: '#1a237e', color: 'white', textAlign: 'center' }}>
                        <Typography variant="body2">© 2024 AI-Recommender. All rights reserved.</Typography>
                    </Box>
                </Box>
            </Router>
        </AuthProvider >
    );
}

export default App;
