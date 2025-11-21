import React from 'react';
import { Card, CardContent, CardMedia, Typography, Button, Box, Rating, Chip } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProductCard = ({ product }) => {
    const navigate = useNavigate();
    const { token } = useAuth();

    const handleView = async () => {
        // Track view
        if (token) {
            try {
                await fetch('/auth/track/view', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ product_name: product.name })
                });
            } catch (e) {
                console.error("Tracking error", e);
            }
        }

        // Navigate to comparison or details
        navigate(`/compare?q=${encodeURIComponent(product.name)}`);
    };

    return (
        <Card sx={{
            maxWidth: 345,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            transition: 'transform 0.2s, box-shadow 0.2s',
            '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 6
            },
            borderRadius: 2
        }}>
            <Box sx={{ position: 'relative' }}>
                <CardMedia
                    component="img"
                    height="200"
                    image={product.image_url || "https://via.placeholder.com/200"}
                    alt={product.name}
                    sx={{ objectFit: 'contain', p: 2, bgcolor: '#f5f5f5' }}
                />
                {product.score > 0.8 && (
                    <Chip
                        label="Recommended"
                        color="secondary"
                        size="small"
                        sx={{ position: 'absolute', top: 10, right: 10 }}
                    />
                )}
            </Box>
            <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Typography gutterBottom variant="h6" component="div" sx={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    lineHeight: 1.2,
                    height: '2.4em'
                }}>
                    {product.name}
                </Typography>

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Rating value={product.rating || 4.5} readOnly precision={0.5} size="small" />
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                        ({product.reviews || 100})
                    </Typography>
                </Box>

                <Box sx={{ mt: 'auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6" color="primary" fontWeight="bold">
                        {product.currency || '₹'}{product.price.toLocaleString()}
                    </Typography>
                    <Button variant="contained" size="small" onClick={handleView}>
                        Compare
                    </Button>
                </Box>
            </CardContent>
        </Card>
    );
};

export default ProductCard;
