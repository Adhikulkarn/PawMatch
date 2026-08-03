import React from 'react';
import Button from '../Button/Button';
import './CTA.css';

export const CTA = () => {
  return (
    <section className="cta-section">
      <div className="container">
        <div className="cta-card">
          <div className="cta-content text-center">
            <span className="cta-badge">Begin Your Journey Today</span>
            <h2 className="cta-heading">Ready to meet your new best friend?</h2>
            <p className="cta-description">
              Thousands of adorable pets in verified shelters across the country are waiting for a loving home like yours.
            </p>
            <div className="cta-button-group">
              <Button variant="primary" size="lg" className="cta-main-btn">
                Adopt Now
                <svg className="cta-icon-svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Button>
              <Button variant="outline" size="lg" className="cta-sub-btn">
                Create Account
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTA;
