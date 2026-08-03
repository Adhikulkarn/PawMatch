import React from 'react';
import './Testimonials.css';

import user1 from '../../assets/images/testimonials/user-1.jpg';
import user2 from '../../assets/images/testimonials/user-2.jpg';
import user3 from '../../assets/images/testimonials/user-3.jpg';

export const Testimonials = () => {
  const testimonials = [
    {
      id: '1',
      name: 'Sarah Jenkins',
      role: 'Adopted Barnaby (Golden Retriever)',
      avatar: user1,
      rating: 5,
      story:
        'Finding Barnaby through PawMatch was the best decision of our lives. The shelter verification gave us complete confidence, and the digital application process was smooth and stress-free!',
    },
    {
      id: '2',
      name: 'Marcus Chen',
      role: 'Adopted Milo (Ginger Kitten)',
      avatar: user2,
      rating: 5,
      story:
        'As a first-time cat owner, PawMatch made matching with Milo so easy. The shelter was communicative, transparent, and supportive every single step of the way.',
    },
    {
      id: '3',
      name: 'Emily & David Watson',
      role: 'Adopted Daisy (Beagle Rescue)',
      avatar: user3,
      rating: 5,
      story:
        'PawMatch connected us with a local shelter when we were looking for a senior dog. Daisy has brought so much warmth and joy to our family home!',
    },
  ];

  return (
    <section className="section testimonials-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Heartwarming Stories</span>
          <h2 className="heading-lg">Adoption Success Stories</h2>
          <p className="section-description">
            Read real experiences from happy families who met their best friends through PawMatch.
          </p>
        </div>

        {/* Testimonials Cards Grid */}
        <div className="testimonials-grid">
          {testimonials.map((t) => (
            <div key={t.id} className="testimonial-card">
              {/* Star Rating */}
              <div className="star-rating" aria-label={`Rating: ${t.rating} out of 5 stars`}>
                {[...Array(t.rating)].map((_, i) => (
                  <svg key={i} className="star-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>

              {/* Story Quote */}
              <p className="testimonial-quote">&ldquo;{t.story}&rdquo;</p>

              {/* Author Details */}
              <div className="testimonial-author">
                <img src={t.avatar} alt={t.name} className="author-avatar" />
                <div className="author-info">
                  <h3 className="author-name">{t.name}</h3>
                  <span className="author-role">{t.role}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
