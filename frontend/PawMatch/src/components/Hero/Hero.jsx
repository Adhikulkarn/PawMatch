import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../Button/Button';
import { useAuth } from '../../contexts/AuthContext';
import heroImg from '../../assets/images/hero/hero-golden-retriever.jpg';
import './Hero.css';

export const Hero = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleAdoptClick = () => {
    if (isAuthenticated) {
      const adoptElement = document.getElementById('adopt');
      if (adoptElement) {
        adoptElement.scrollIntoView({ behavior: 'smooth' });
      } else {
        navigate('/dashboard');
      }
    } else {
      navigate('/login');
    }
  };

  const handleRegisterShelterClick = () => {
    navigate('/register');
  };

  return (
    <section id="home" className="hero-section">
      {/* Background Image Layer */}
      <div className="hero-bg-wrapper">
        <img
          src={heroImg}
          alt="Golden Retriever puppy resting in sunlit meadow"
          className="hero-bg-img"
        />
        <div className="hero-overlay"></div>
      </div>

      {/* Hero Content Overlay */}
      <div className="container hero-container">
        <div className="hero-content-box">
          <div className="hero-badge">
            <span className="badge-dot"></span>
            <span>Over 12,000+ Pets Waiting For A Loving Home</span>
          </div>

          <h1 className="hero-heading">
            Meet the friend who will <span className="text-editorial">change everything.</span>
          </h1>

          <p className="hero-description">
            Discover your perfect companion from verified shelters. We match loving homes with pets in need through transparent, compassionate adoption.
          </p>

          <div className="hero-cta-group">
            <Button variant="primary" size="lg" className="hero-primary-btn" onClick={handleAdoptClick}>
              Adopt a Pet
              <svg className="cta-arrow" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </Button>
            <Button variant="outline" size="lg" className="hero-secondary-btn" onClick={handleRegisterShelterClick}>
              Register a Shelter
            </Button>
          </div>

          {/* Trust Badges */}
          <div className="hero-trust-badges">
            <div className="trust-badge-item">
              <div className="trust-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div className="trust-text">
                <span className="trust-title">Verified Shelters</span>
                <span className="trust-subtitle">100% Vetted Partners</span>
              </div>
            </div>

            <div className="trust-badge-divider"></div>

            <div className="trust-badge-item">
              <div className="trust-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <div className="trust-text">
                <span className="trust-title">Safe Adoption</span>
                <span className="trust-subtitle">Protected Process</span>
              </div>
            </div>

            <div className="trust-badge-divider"></div>

            <div className="trust-badge-item">
              <div className="trust-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div className="trust-text">
                <span className="trust-title">Trusted Community</span>
                <span className="trust-subtitle">Active Foster Network</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
