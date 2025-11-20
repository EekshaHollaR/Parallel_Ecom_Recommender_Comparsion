import React, { useState } from 'react';
import { Paper, InputBase, IconButton } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const SearchBar = ({ onSearch, placeholder = "Search..." }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <Paper
            component="form"
            onSubmit={handleSubmit}
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: '100%', maxWidth: 600 }}
        >
            <InputBase
                sx={{ ml: 1, flex: 1 }}
                placeholder={placeholder}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
                <SearchIcon />
            </IconButton>
        </Paper>
    );
};

export default SearchBar;
