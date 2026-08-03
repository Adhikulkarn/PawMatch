import React, { useState } from 'react';
import Logo from '../Logo/Logo';
import Button from '../Button/Button';
import './Footer.css';

export const Footer = () => {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail('');
    }
  };

  return (
    <footer id="contact" className="footer-section">
      <div className="container">
        {/* Upper Footer: Brand & Newsletter */}
        <div className="footer-top-grid">
          {/* Brand Info */}
          <div className="footer-brand-col">
            <Logo size="large" light />
            <p className="footer-brand-desc">
              PawMatch is the nationwide pet adoption ecosystem connecting loving homes with verified animal shelters. Dedicated to transparent, compassionate pet care and welfare.
            </p>
            {/* Social Media Links */}
            <div className="footer-socials">
              <a href="#" className="social-link" aria-label="Instagram">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                  <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                </svg>
              </a>
              <a href="#" className="social-link" aria-label="Facebook">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
                </svg>
              </a>
              <a href="#" className="social-link" aria-label="X Twitter">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
                </svg>
              </a>
              <a href="#" className="social-link" aria-label="LinkedIn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                  <rect x="2" y="9" width="4" height="12"></rect>
                  <circle cx="4" cy="4" r="2"></circle>
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="footer-links-col">
            <h4 className="footer-col-title">Quick Links</h4>
            <ul className="footer-links-list">
              <li><a href="#home">Home</a></li>
              <li><a href="#adopt">Adopt Pets</a></li>
              <li><a href="#how-it-works">How It Works</a></li>
              <li><a href="#shelters">Shelters</a></li>
              <li><a href="#about">About Us</a></li>
              <li><a href="#">Success Stories</a></li>
            </ul>
          </div>

          {/* Support Links */}
          <div className="footer-links-col">
            <h4 className="footer-col-title">Support &amp; Legal</h4>
            <ul className="footer-links-list">
              <li><a href="#">Help Center</a></li>
              <li><a href="#">Adoption Guide</a></li>
              <li><a href="#">Shelter Portal</a></li>
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Terms of Service</a></li>
              <li><a href="#">Cookie Settings</a></li>
            </ul>
          </div>

          {/* Newsletter Column */}
          <div className="footer-newsletter-col">
            <h4 className="footer-col-title">Stay Connected</h4>
            <p className="newsletter-desc">
              Subscribe to get notified about new adoption listings, shelter updates, and pet care guides.
            </p>

            {subscribed ? (
              <div className="newsletter-success">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <span>Thank you for subscribing!</span>
              </div>
            ) : (
              <form className="newsletter-form" onSubmit={handleSubscribe}>
                <input
                  type="email"
                  className="newsletter-input"
                  placeholder="Enter your email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <Button type="submit" variant="primary" size="md" className="newsletter-btn">
                  Subscribe
                </Button>
              </form>
            )}
          </div>
        </div>

        {/* Lower Footer: Copyright */}
        <div className="footer-bottom-bar">
          <p className="copyright-text">
            &copy; {new Date().getFullYear()} PawMatch Inc. All rights reserved. Built with compassion for pets nationwide.
          </p>
          <div className="bottom-links">
            <a href="#">Privacy</a>
            <span className="dot">•</span>
            <a href="#">Terms</a>
            <span className="dot">•</span>
            <a href="#">Security</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
