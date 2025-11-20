import React from 'react';
import {
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Chip
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
                        <TableCell>Site</TableCell>
                        <TableCell align="right">Price</TableCell>
                        <TableCell align="right">Source</TableCell>
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
                                {row.site}
                                {row.price === minPrice && (
                                    <Chip label="Best Price" color="success" size="small" sx={{ ml: 1 }} />
                                )}
                            </TableCell>
                            <TableCell align="right">
                                <span style={{ fontWeight: row.price === minPrice ? 'bold' : 'normal', color: row.price === minPrice ? 'green' : 'inherit' }}>
                                    ${row.price.toFixed(2)}
                                </span>
                            </TableCell>
                            <TableCell align="right">{row.source}</TableCell>
                            <TableCell align="right">
                                <a href={row.product_url} target="_blank" rel="noopener noreferrer">
                                    View
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
