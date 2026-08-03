import React from 'react';
import './Statistics.css';

export const Statistics = () => {
  const stats = [
    {
      id: '1',
      value: '500+',
      label: 'Verified Shelters',
      subtitle: 'Strict vetting standards',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5m0 0h4m-4 0V11m0 0h4m-4 0H9" />
        </svg>
      ),
    },
    {
      id: '2',
      value: '12,500+',
      label: 'Pets Available',
      subtitle: 'Across dogs, cats & more',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      ),
    },
    {
      id: '3',
      value: '98%',
      label: 'Happy Adoptions',
      subtitle: 'Successful long-term matches',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    {
      id: '4',
      value: '150+',
      label: 'Cities Reached',
      subtitle: 'Nationwide rescue network',
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 002 2h1.5a2.5 2.5 0 002.5-2.5V11a2 2 0 00-2-2h-1c-1 0-1.5-.5-1.5-1V4.5a2.5 2.5 0 00-2.5-2.5H10A2 2 0 008 3.935z" />
        </svg>
      ),
    },
  ];

  return (
    <section className="statistics-section">
      <div className="container">
        <div className="stats-inner-wrapper">
          <div className="stats-header text-center">
            <span className="stats-subtitle">Impact In Numbers</span>
            <h2 className="stats-heading">Building a Compassionate Pet Welfare Network</h2>
          </div>

          <div className="stats-grid">
            {stats.map((stat) => (
              <div key={stat.id} className="stat-card">
                <div className="stat-icon-wrapper">{stat.icon}</div>
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
                <div className="stat-sublabel">{stat.subtitle}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Statistics;
