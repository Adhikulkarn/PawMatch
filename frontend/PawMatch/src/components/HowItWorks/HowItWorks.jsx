import React from 'react';
import './HowItWorks.css';

export const HowItWorks = () => {
  const steps = [
    {
      number: '01',
      title: 'Create Account',
      description: 'Set up your profile and share your household preferences to help us connect you with compatible pets.',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
    },
    {
      number: '02',
      title: 'Browse Pets',
      description: 'Filter through thousands of verified shelter pets by species, breed, location, and temperament.',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      ),
    },
    {
      number: '03',
      title: 'Submit Application',
      description: 'Connect directly with verified shelters and submit a streamlined, secure digital adoption application.',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
    },
    {
      number: '04',
      title: 'Welcome Home',
      description: 'Finalize meet-and-greet sessions, complete adoption handover, and bring your new companion home with support.',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      ),
    },
  ];

  return (
    <section id="how-it-works" className="section how-it-works-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Simple 4-Step Process</span>
          <h2 className="heading-lg">How PawMatch Adoption Works</h2>
          <p className="section-description">
            We simplify pet adoption into four transparent and compassionate steps for adopters and rescue partners.
          </p>
        </div>

        {/* Timeline Steps */}
        <div className="timeline-container">
          <div className="timeline-line"></div>
          
          <div className="timeline-grid">
            {steps.map((step) => (
              <div key={step.number} className="timeline-card-wrapper">
                <div className="timeline-card">
                  <div className="step-badge">{step.number}</div>
                  <div className="step-icon-box">{step.icon}</div>
                  <h3 className="step-title">{step.title}</h3>
                  <p className="step-description">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
