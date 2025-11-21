import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Container, TextField, Button, Typography, Box, Alert } from '@mui/material';
import axios from 'axios';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        try {
            await axios.post('http://localhost:5000/auth/signup', {
                username,
                password
            });
            setSuccess('Account created! Redirecting to login...');
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            setError(err.response?.data?.msg || 'Signup failed');
        }
    };

    return (
        <Container maxWidth="xs">
            <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Typography component="h1" variant="h5">
                    Sign Up
                </Typography>
                {error && <Alert severity="error" sx={{ mt: 2, width: '100%' }}>{error}</Alert>}
                {success && <Alert severity="success" sx={{ mt: 2, width: '100%' }}>{success}</Alert>}
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        label="Username"
                        autoFocus
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        label="Password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        Sign Up
                    </Button>
                    <Link to="/login" style={{ textDecoration: 'none' }}>
                        <Typography variant="body2" color="primary" align="center">
                            Already have an account? Sign In
                        </Typography>
                    </Link>
                </Box>
            </Box>
        </Container>
    );
};

export default Signup;
