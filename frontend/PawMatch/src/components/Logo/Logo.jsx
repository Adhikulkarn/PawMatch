import React from 'react';
import './Logo.css';

export const Logo = ({ size = 'medium', light = false, className = '' }) => {
  return (
    <a href="#" className={`pawmatch-logo logo-${size} ${light ? 'light' : ''} ${className}`} aria-label="PawMatch Home">
      <div className="logo-icon-wrapper">
        <svg
          className="logo-svg"
          viewBox="0 0 48 48"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          {/* Minimalist Dog Nose / Snout */}
          <path
            d="M24 14C28.4183 14 32 17.5817 32 22C32 26.4183 27.5 29.5 24 32C20.5 29.5 16 26.4183 16 22C16 17.5817 19.5817 14 24 14Z"
            fill="currentColor"
            className="snout-path"
          />
          {/* Nostril accents */}
          <circle cx="21" cy="21" r="1.5" fill={light ? '#1C1917' : '#FFFFFF'} />
          <circle cx="27" cy="21" r="1.5" fill={light ? '#1C1917' : '#FFFFFF'} />

          {/* Left Whiskers */}
          <path
            d="M12 21C8.5 20.5 5 19 3 17.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M13 24C9 24.5 5.5 24 3 23.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M14 27C10.5 28.5 7 29 4.5 29.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />

          {/* Right Whiskers */}
          <path
            d="M36 21C39.5 20.5 43 19 45 17.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M35 24C39 24.5 42.5 24 45 23.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M34 27C37.5 28.5 41 29 43.5 29.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />

          {/* Subtle Paw Accent Heart above */}
          <path
            d="M24 10C24 10 21.5 7 19.5 8.5C17.5 10 19 12.5 24 15C29 12.5 30.5 10 28.5 8.5C26.5 7 24 10 24 10Z"
            fill="currentColor"
            opacity="0.85"
          />
        </svg>
      </div>
      <span className="logo-brand-name">
        Paw<span className="brand-highlight">Match</span>
      </span>
    </a>
  );
};

export default Logo;
