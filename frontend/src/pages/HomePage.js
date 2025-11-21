import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Grid, CircularProgress, Paper, Chip } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import ProductCard from '../components/ProductCard';

const HomePage = () => {
    const { user, token } = useAuth();
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                const res = await fetch('/recommendations?n=4', { headers });
                const data = await res.json();
                if (data.status === 'success') {
                    setRecommendations(data.data.recommendations);
                }
            } catch (error) {
                console.error("Error fetching recommendations:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, [token]);

    return (
        <Box>
            {/* Hero Section */}
            <Paper
                sx={{
                    p: 6,
                    mb: 4,
                    background: 'linear-gradient(45deg, #1a237e 30%, #283593 90%)',
                    color: 'white',
                    borderRadius: 0
                }}
            >
                <Container maxWidth="lg">
                    <Typography variant="h3" gutterBottom fontWeight="bold">
                        {user ? `Welcome back, ${user.username}!` : 'Welcome to AI-Recommender'}
                    </Typography>
                    <Typography variant="h5" sx={{ opacity: 0.9 }}>
                        Discover the best prices and personalized picks just for you.
                    </Typography>
                </Container>
            </Paper>

            <Container maxWidth="lg">
                {/* Featured Categories */}
                <Box sx={{ mb: 4, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {['Electronics', 'Mobiles', 'Laptops', 'Headphones', 'Cameras'].map((cat) => (
                        <Chip
                            key={cat}
                            label={cat}
                            onClick={() => { }}
                            sx={{ fontSize: '1rem', py: 2, px: 1 }}
                            clickable
                        />
                    ))}
                </Box>

                {/* Recommendations Section */}
                <Typography variant="h4" gutterBottom fontWeight="bold" sx={{ mb: 3 }}>
                    Recommended for You
                </Typography>

                {loading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                        <CircularProgress />
                    </Box>
                ) : (
                    <Grid container spacing={3}>
                        {recommendations.map((item, index) => (
                            <Grid item xs={12} sm={6} md={3} key={index}>
                                <ProductCard product={item} />
                            </Grid>
                        ))}
                    </Grid>
                )}
            </Container>
        </Box>
    );
};

export default HomePage;
