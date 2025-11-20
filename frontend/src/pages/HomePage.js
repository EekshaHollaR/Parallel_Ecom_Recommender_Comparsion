import React from 'react';
import { Container, Typography, Grid, Card, CardActionArea, CardContent, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import RecommendIcon from '@mui/icons-material/Recommend';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';

const HomePage = () => {
    const navigate = useNavigate();

    return (
        <Container maxWidth="md" sx={{ mt: 8 }}>
            <Box textAlign="center" mb={6}>
                <Typography variant="h2" component="h1" gutterBottom>
                    AI Commerce Engine
                </Typography>
                <Typography variant="h5" color="text.secondary">
                    Parallel Recommender & Real-time Price Comparison
                </Typography>
            </Box>

            <Grid container spacing={4}>
                <Grid item xs={12} md={6}>
                    <Card sx={{ height: '100%' }}>
                        <CardActionArea
                            onClick={() => navigate('/recommendations')}
                            sx={{ height: '100%', p: 2 }}
                        >
                            <CardContent sx={{ textAlign: 'center' }}>
                                <RecommendIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                                <Typography variant="h5" gutterBottom>
                                    AI Recommendations
                                </Typography>
                                <Typography variant="body1" color="text.secondary">
                                    Get personalized product recommendations using our parallel ALS-NCG algorithm.
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Card sx={{ height: '100%' }}>
                        <CardActionArea
                            onClick={() => navigate('/compare')}
                            sx={{ height: '100%', p: 2 }}
                        >
                            <CardContent sx={{ textAlign: 'center' }}>
                                <CompareArrowsIcon sx={{ fontSize: 60, color: 'secondary.main', mb: 2 }} />
                                <Typography variant="h5" gutterBottom>
                                    Price Comparison
                                </Typography>
                                <Typography variant="body1" color="text.secondary">
                                    Compare prices across multiple e-commerce sites in real-time.
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </Grid>
            </Grid>
        </Container>
    );
};

export default HomePage;
