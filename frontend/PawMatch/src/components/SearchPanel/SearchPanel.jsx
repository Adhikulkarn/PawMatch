import React, { useState } from 'react';
import Button from '../Button/Button';
import './SearchPanel.css';

export const SearchPanel = () => {
  const [keyword, setKeyword] = useState('');
  const [species, setSpecies] = useState('');
  const [breed, setBreed] = useState('');
  const [location, setLocation] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    console.log('Search submit:', { keyword, species, breed, location });
  };

  return (
    <section className="search-panel-section">
      <div className="container">
        <form className="search-panel-card glass-panel" onSubmit={handleSearch}>
          <div className="search-grid">
            {/* Keyword Search */}
            <div className="search-field">
              <label htmlFor="search-keyword" className="field-label">
                <svg className="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Keyword Search
              </label>
              <input
                id="search-keyword"
                type="text"
                className="field-input"
                placeholder="Search name, trait, e.g., 'Friendly'"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
              />
            </div>

            {/* Species Select */}
            <div className="search-field">
              <label htmlFor="search-species" className="field-label">
                <svg className="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                Species
              </label>
              <select
                id="search-species"
                className="field-select"
                value={species}
                onChange={(e) => setSpecies(e.target.value)}
              >
                <option value="">All Species</option>
                <option value="dog">Dogs</option>
                <option value="cat">Cats</option>
                <option value="rabbit">Rabbits</option>
                <option value="bird">Birds</option>
              </select>
            </div>

            {/* Breed Select */}
            <div className="search-field">
              <label htmlFor="search-breed" className="field-label">
                <svg className="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7 7h10M7 12h10m-5 5h5" />
                </svg>
                Breed
              </label>
              <select
                id="search-breed"
                className="field-select"
                value={breed}
                onChange={(e) => setBreed(e.target.value)}
              >
                <option value="">All Breeds</option>
                <option value="golden-retriever">Golden Retriever</option>
                <option value="tabby-cat">Tabby Cat</option>
                <option value="french-bulldog">French Bulldog</option>
                <option value="persian-cat">Persian Cat</option>
                <option value="beagle">Beagle</option>
                <option value="australian-shepherd">Australian Shepherd</option>
              </select>
            </div>

            {/* Location Input */}
            <div className="search-field">
              <label htmlFor="search-location" className="field-label">
                <svg className="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Location
              </label>
              <input
                id="search-location"
                type="text"
                className="field-input"
                placeholder="City, State or Postal Code"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>

            {/* Search Submit Button */}
            <div className="search-submit-wrapper">
              <Button type="submit" variant="primary" size="lg" fullWidth className="search-btn">
                <svg className="btn-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search
              </Button>
            </div>
          </div>
        </form>
      </div>
    </section>
  );
};

export default SearchPanel;
