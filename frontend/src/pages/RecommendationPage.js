import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';
import RecommendationList from '../components/RecommendationList';
import Loader from '../components/Loader';
import ErrorBanner from '../components/ErrorBanner';
import { useAuth } from '../context/AuthContext';

const RecommendationPage = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { token, user } = useAuth();

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                // Default to 6 items for the page
                const res = await fetch('/api/recommendations?n=6', { headers });
                const data = await res.json();

                if (data.status === 'success') {
                    setRecommendations(data.data.recommendations);
                } else {
                    setError(data.message);
                }
            } catch (err) {
                setError('Failed to fetch recommendations');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, [token]);

    return (
        <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" gutterBottom fontWeight="bold">
                    Explore
                </Typography>
                <Typography variant="h6" color="text.secondary">
                    {user ? `Curated picks for ${user.username}` : 'Trending items you might like'}
                </Typography>
            </Box>

            {loading && <Loader message="Curating your personalized feed..." />}
            {error && <ErrorBanner message={error} />}

            {!loading && !error && (
                <RecommendationList recommendations={recommendations} />
            )}
        </Container>
    );
};

export default RecommendationPage;
