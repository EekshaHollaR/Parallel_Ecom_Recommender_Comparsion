import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import PriceTable from '../components/PriceTable';
import Loader from '../components/Loader';
import ErrorBanner from '../components/ErrorBanner';
import api from '../api';
import { useAuth } from '../context/AuthContext';

const PriceComparePage = () => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [searchParams, setSearchParams] = useSearchParams();
    const { token } = useAuth();

    const handleSearch = async (productName) => {
        setLoading(true);
        setError(null);
        setSearchParams({ q: productName });

        // Track search
        if (token) {
            try {
                await fetch('/auth/track/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ query: productName })
                });
            } catch (e) {
                console.error("Tracking error", e);
            }
        }

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

    useEffect(() => {
        const query = searchParams.get('q');
        if (query) {
            handleSearch(query);
        }
    }, []); // Run once on mount if query exists

    return (
        <Container maxWidth="lg">
            <Typography variant="h4" gutterBottom fontWeight="bold" sx={{ mb: 3 }}>
                Price Comparison
            </Typography>

            <Paper sx={{ p: 4, mb: 4, borderRadius: 2 }}>
                <Typography variant="body1" gutterBottom sx={{ mb: 2 }}>
                    Search for a product to compare prices across Amazon, Flipkart, and Croma.
                </Typography>
                <SearchBar onSearch={handleSearch} placeholder="Enter Product Name (e.g., Sony Headphones)" />
            </Paper>

            {loading && <Loader message="Scraping prices from multiple stores..." />}
            {error && <ErrorBanner message={error} />}

            {!loading && !error && results && (
                <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="h5" fontWeight="bold">
                            Results for "{results.product}"
                        </Typography>
                        <Typography variant="caption" sx={{ bgcolor: '#e3f2fd', p: 1, borderRadius: 1 }}>
                            Latency: {results.total_latency_ms} ms
                        </Typography>
                    </Box>
                    <PriceTable results={results.results} />
                </Box>
            )}
        </Container>
    );
};

export default PriceComparePage;
