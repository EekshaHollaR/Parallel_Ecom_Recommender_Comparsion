import React, { useState } from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';
import SearchBar from '../components/SearchBar';
import RecommendationList from '../components/RecommendationList';
import Loader from '../components/Loader';
import ErrorBanner from '../components/ErrorBanner';
import api from '../api';

const RecommendationPage = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (userId) => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.get(`/recommendations?user_id=${userId}`);
            if (response.data.status === 'success') {
                setRecommendations(response.data.data.recommendations);
            } else {
                setError(response.data.message);
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to fetch recommendations');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                User Recommendations
            </Typography>

            <Paper sx={{ p: 3, mb: 4 }}>
                <Typography variant="body1" gutterBottom>
                    Enter a User ID to get personalized AI recommendations.
                </Typography>
                <SearchBar onSearch={handleSearch} placeholder="Enter User ID (e.g., 0)" />
            </Paper>

            {loading && <Loader message="Generating recommendations..." />}
            {error && <ErrorBanner message={error} />}

            {!loading && !error && (
                <RecommendationList recommendations={recommendations} />
            )}
        </Container>
    );
};

export default RecommendationPage;
