import { render, screen, fireEvent } from '@testing-library/react';
import SearchBar from '../components/SearchBar';
import Loader from '../components/Loader';
import ErrorBanner from '../components/ErrorBanner';

test('SearchBar renders and handles input', () => {
    const handleSearch = jest.fn();
    render(<SearchBar onSearch={handleSearch} placeholder="Search..." />);

    const input = screen.getByPlaceholderText(/Search.../i);
    fireEvent.change(input, { target: { value: 'test query' } });

    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(handleSearch).toHaveBeenCalledWith('test query');
});

test('Loader renders message', () => {
    render(<Loader message="Please wait..." />);
    const element = screen.getByText(/Please wait.../i);
    expect(element).toBeInTheDocument();
});

test('ErrorBanner renders error message', () => {
    render(<ErrorBanner message="Something went wrong" />);
    const element = screen.getByText(/Something went wrong/i);
    expect(element).toBeInTheDocument();
});
