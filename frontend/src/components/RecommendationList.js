import React from 'react';
import { Grid, Card, CardContent, Typography, CardMedia, Chip } from '@mui/material';

const RecommendationList = ({ recommendations }) => {
    if (!recommendations || recommendations.length === 0) {
        return <Typography variant="body1">No recommendations found.</Typography>;
    }

    return (
        <Grid container spacing={3} sx={{ mt: 2 }}>
            {recommendations.map((rec, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                        <CardMedia
                            component="img"
                            height="140"
                            image={`https://via.placeholder.com/300x140?text=Item+${rec.item_id}`}
                            alt={`Item ${rec.item_id}`}
                        />
                        <CardContent>
                            <Typography gutterBottom variant="h6" component="div">
                                Item #{rec.item_id}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                Relevance Score:
                            </Typography>
                            <Chip
                                label={rec.score.toFixed(4)}
                                color="primary"
                                variant="outlined"
                                sx={{ mt: 1 }}
                            />
                        </CardContent>
                    </Card>
                </Grid>
            ))}
        </Grid>
    );
};

export default RecommendationList;
