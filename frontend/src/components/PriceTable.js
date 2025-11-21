import React from 'react';
import {
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Chip, Avatar, Rating, Box, Typography
} from '@mui/material';

const PriceTable = ({ results }) => {
    if (!results || results.length === 0) return null;

    // Find minimum price to highlight
    const minPrice = Math.min(...results.map(r => r.price));

    return (
        <TableContainer component={Paper} sx={{ mt: 3 }}>
            <Table aria-label="price comparison table">
                <TableHead>
                    <TableRow>
                        <TableCell>Product</TableCell>
                        <TableCell>Site</TableCell>
                        <TableCell>Rating</TableCell>
                        <TableCell align="right">Price</TableCell>
                        <TableCell align="right">Link</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {results.map((row, index) => (
                        <TableRow
                            key={index}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">
                                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                    <Avatar variant="square" src={row.image_url} sx={{ mr: 2, width: 50, height: 50 }} />
                                </Box>
                            </TableCell>
                            <TableCell>{row.site}</TableCell>
                            <TableCell>
                                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                    <Rating value={row.rating} readOnly precision={0.1} size="small" />
                                    <Typography variant="caption" sx={{ ml: 1 }}>
                                        ({row.reviews})
                                    </Typography>
                                </Box>
                            </TableCell>
                            <TableCell align="right">
                                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                                    <span style={{ fontWeight: row.price === minPrice ? 'bold' : 'normal', color: row.price === minPrice ? 'green' : 'inherit' }}>
                                        {row.currency || '$'}{row.price.toFixed(2)}
                                    </span>
                                    {row.price === minPrice && (
                                        <Chip label="Best Price" color="success" size="small" sx={{ mt: 0.5 }} />
                                    )}
                                </Box>
                            </TableCell>
                            <TableCell align="right">
                                <a href={row.product_url} target="_blank" rel="noopener noreferrer">
                                    View Deal
                                </a>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default PriceTable;
