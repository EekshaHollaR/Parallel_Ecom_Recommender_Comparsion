import React from 'react';
import { Grid, Typography } from '@mui/material';
import ProductCard from './ProductCard';

const RecommendationList = ({ recommendations }) => {
    if (!recommendations || recommendations.length === 0) {
        return <Typography variant="body1">No recommendations found.</Typography>;
    }

    return (
        <Grid container spacing={3} sx={{ mt: 2 }}>
            {recommendations.map((rec, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                    <ProductCard product={rec} />
                </Grid>
            ))}
        </Grid>
    );
};

export default RecommendationList;
