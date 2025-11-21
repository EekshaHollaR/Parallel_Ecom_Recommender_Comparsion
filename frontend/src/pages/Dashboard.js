import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, Box } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import axios from 'axios';

const Dashboard = () => {
    const [metrics, setMetrics] = useState({
        rps: 0,
        cache_hit_rate: 0,
        cache_hits: 0,
        cache_misses: 0
    });
    const [history, setHistory] = useState([]);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const response = await axios.get('http://localhost:5000/metrics');
                const data = response.data;
                setMetrics(data);

                setHistory(prev => {
                    const newHistory = [...prev, { ...data, time: new Date().toLocaleTimeString() }];
                    if (newHistory.length > 20) newHistory.shift(); // Keep last 20 points
                    return newHistory;
                });
            } catch (error) {
                console.error("Error fetching metrics:", error);
            }
        };

        const interval = setInterval(fetchMetrics, 2000); // Poll every 2 seconds
        return () => clearInterval(interval);
    }, []);

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Real-time Analytics Dashboard
            </Typography>

            <Grid container spacing={3}>
                {/* RPS Chart */}
                <Grid item xs={12} md={8} lg={9}>
                    <Paper
                        sx={{
                            p: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            height: 240,
                        }}
                    >
                        <Typography component="h2" variant="h6" color="primary" gutterBottom>
                            Requests Per Second (RPS)
                        </Typography>
                        <ResponsiveContainer>
                            <LineChart data={history}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="time" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="rps" stroke="#8884d8" activeDot={{ r: 8 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>

                {/* Current Stats */}
                <Grid item xs={12} md={4} lg={3}>
                    <Paper
                        sx={{
                            p: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            height: 240,
                            justifyContent: 'center',
                            alignItems: 'center'
                        }}
                    >
                        <Typography component="h2" variant="h6" color="primary" gutterBottom>
                            Cache Hit Rate
                        </Typography>
                        <Typography component="p" variant="h3">
                            {metrics.cache_hit_rate}%
                        </Typography>
                        <Typography color="text.secondary" sx={{ flex: 1 }}>
                            Hits: {metrics.cache_hits} | Misses: {metrics.cache_misses}
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Dashboard;
