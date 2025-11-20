import React, { useState } from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';
import SearchBar from '../components/SearchBar';
import PriceTable from '../components/PriceTable';
import Loader from '../components/Loader';
import ErrorBanner from '../components/ErrorBanner';
import api from '../api';

const PriceComparePage = () => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (productName) => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.get(`/compare_price?product=${productName}`);
            if (response.data.status === 'success') {
                setResults(response.data.data);
            } else {
                setError(response.data.message);
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to fetch prices');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Price Comparison
            </Typography>

            <Paper sx={{ p: 3, mb: 4 }}>
                <Typography variant="body1" gutterBottom>
                    Search for a product to compare prices across stores.
                </Typography>
                <SearchBar onSearch={handleSearch} placeholder="Enter Product Name (e.g., Sony Headphones)" />
            </Paper>

            {loading && <Loader message="Scraping prices..." />}
            {error && <ErrorBanner message={error} />}

            {!loading && !error && results && (
                <Box>
                    <Typography variant="h6">
                        Results for "{results.product}"
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                        Latency: {results.total_latency_ms} ms
                    </Typography>
                    <PriceTable results={results.results} />
                </Box>
            )}
        </Container>
    );
};

export default PriceComparePage;
