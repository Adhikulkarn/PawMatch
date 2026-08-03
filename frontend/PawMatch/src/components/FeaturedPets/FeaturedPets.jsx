import React, { useState } from 'react';
import PetCard from '../PetCard/PetCard';
import Button from '../Button/Button';
import './FeaturedPets.css';

// Import local image assets
import pet1 from '../../assets/images/pets/pet-1.jpg';
import pet2 from '../../assets/images/pets/pet-2.jpg';
import pet3 from '../../assets/images/pets/pet-3.jpg';
import pet4 from '../../assets/images/pets/pet-4.jpg';
import pet5 from '../../assets/images/pets/pet-5.jpg';
import pet6 from '../../assets/images/pets/pet-6.jpg';

export const FeaturedPets = () => {
  const [activeTab, setActiveTab] = useState('all');

  const petsData = [
    {
      id: '1',
      name: 'Bella',
      species: 'dog',
      breed: 'Golden Retriever',
      age: '2 yrs',
      gender: 'Female',
      shelter: 'Haven Rescue',
      location: 'Austin, TX',
      image: pet1,
      badge: 'Featured',
      badgeType: 'available',
    },
    {
      id: '2',
      name: 'Milo',
      species: 'cat',
      breed: 'Ginger Tabby Kitten',
      age: '4 mos',
      gender: 'Male',
      shelter: 'Warm Paws Shelter',
      location: 'Seattle, WA',
      image: pet2,
      badge: 'Urgent',
      badgeType: 'urgent',
    },
    {
      id: '3',
      name: 'Bruno',
      species: 'dog',
      breed: 'French Bulldog',
      age: '1 yr',
      gender: 'Male',
      shelter: 'Metro Animal Haven',
      location: 'Chicago, IL',
      image: pet3,
      badge: 'New Arrival',
      badgeType: 'available',
    },
    {
      id: '4',
      name: 'Luna',
      species: 'cat',
      breed: 'Persian Cat',
      age: '3 yrs',
      gender: 'Female',
      shelter: 'Feline Friends Care',
      location: 'Denver, CO',
      image: pet4,
      badge: 'Popular',
      badgeType: 'available',
    },
    {
      id: '5',
      name: 'Charlie',
      species: 'dog',
      breed: 'Beagle',
      age: '1.5 yrs',
      gender: 'Male',
      shelter: 'Country Paws Rescue',
      location: 'Nashville, TN',
      image: pet5,
      badge: 'Featured',
      badgeType: 'available',
    },
    {
      id: '6',
      name: 'Daisy',
      species: 'dog',
      breed: 'Australian Shepherd',
      age: '2.5 yrs',
      gender: 'Female',
      shelter: 'Pacific Animal Rescue',
      location: 'San Francisco, CA',
      image: pet6,
      badge: 'Urgent',
      badgeType: 'urgent',
    },
  ];

  const filteredPets = activeTab === 'all'
    ? petsData
    : petsData.filter((pet) => pet.species === activeTab);

  return (
    <section id="adopt" className="section featured-pets-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Discover Companions</span>
          <h2 className="heading-lg">Featured Pets Available For Adoption</h2>
          <p className="section-description">
            Meet loving pets from verified local shelters across the country ready to find their forever homes.
          </p>

          {/* Filter Tabs */}
          <div className="filter-tabs">
            <button
              type="button"
              className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
              onClick={() => setActiveTab('all')}
            >
              All Companions
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'dog' ? 'active' : ''}`}
              onClick={() => setActiveTab('dog')}
            >
              Dogs
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'cat' ? 'active' : ''}`}
              onClick={() => setActiveTab('cat')}
            >
              Cats
            </button>
          </div>
        </div>

        {/* Pets Grid */}
        <div className="pets-grid">
          {filteredPets.map((pet) => (
            <PetCard key={pet.id} pet={pet} />
          ))}
        </div>

        {/* View All CTA */}
        <div className="pets-view-all text-center">
          <Button variant="primary" size="lg">
            Explore All 12,000+ Pets
          </Button>
        </div>
      </div>
    </section>
  );
};

export default FeaturedPets;
