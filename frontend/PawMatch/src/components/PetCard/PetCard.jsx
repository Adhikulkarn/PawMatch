import React, { useState } from 'react';
import Button from '../Button/Button';
import './PetCard.css';

export const PetCard = ({ pet }) => {
  const [isLiked, setIsLiked] = useState(pet.isLiked || false);

  const toggleLike = (e) => {
    e.stopPropagation();
    setIsLiked(!isLiked);
  };

  return (
    <div className="pet-card">
      {/* Pet Image Container */}
      <div className="pet-card-image-wrapper">
        <img src={pet.image} alt={pet.name} className="pet-card-image" loading="lazy" />
        
        {/* Status Tag */}
        {pet.badge && <span className={`pet-badge badge-${pet.badgeType || 'available'}`}>{pet.badge}</span>}

        {/* Favorite Heart Button */}
        <button
          type="button"
          className={`favourite-btn ${isLiked ? 'liked' : ''}`}
          onClick={toggleLike}
          aria-label={isLiked ? `Remove ${pet.name} from favorites` : `Add ${pet.name} to favorites`}
        >
          <svg className="heart-icon" viewBox="0 0 24 24" fill={isLiked ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
      </div>

      {/* Pet Card Content */}
      <div className="pet-card-content">
        <div className="pet-card-header">
          <h3 className="pet-name">{pet.name}</h3>
          <span className="pet-gender-age">{pet.gender} • {pet.age}</span>
        </div>

        <p className="pet-breed">{pet.breed}</p>

        {/* Shelter & Location */}
        <div className="pet-card-location">
          <svg className="location-pin-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span className="location-text">{pet.shelter} • {pet.location}</span>
        </div>

        {/* Card Action Button */}
        <Button variant="outline" size="sm" fullWidth className="view-details-btn">
          View Details
        </Button>
      </div>
    </div>
  );
};

export default PetCard;
