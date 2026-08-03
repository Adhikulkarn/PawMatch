import React, { useState, useEffect } from 'react';
import Logo from '../Logo/Logo';
import Button from '../Button/Button';
import './Navbar.css';

export const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'Home', href: '#home' },
    { name: 'Adopt Pets', href: '#adopt' },
    { name: 'How It Works', href: '#how-it-works' },
    { name: 'Shelters', href: '#shelters' },
    { name: 'About', href: '#about' },
    { name: 'Contact', href: '#contact' },
  ];

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <header className={`navbar-header ${isScrolled ? 'scrolled glass-panel' : ''}`}>
      <div className="container navbar-container">
        {/* Logo */}
        <Logo size="medium" />

        {/* Desktop Navigation Links */}
        <nav className="desktop-nav" aria-label="Main Navigation">
          <ul className="nav-list">
            {navLinks.map((link) => (
              <li key={link.name} className="nav-item">
                <a href={link.href} className="nav-link">
                  {link.name}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* Auth Buttons Desktop */}
        <div className="nav-auth-actions">
          <Button variant="ghost" size="sm" className="login-btn">
            Login
          </Button>
          <Button variant="primary" size="sm" className="signup-btn">
            Sign Up
          </Button>
        </div>

        {/* Mobile Hamburger Button */}
        <button
          type="button"
          className={`mobile-hamburger ${isMobileMenuOpen ? 'open' : ''}`}
          onClick={toggleMobileMenu}
          aria-label={isMobileMenuOpen ? 'Close Navigation Menu' : 'Open Navigation Menu'}
          aria-expanded={isMobileMenuOpen}
        >
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
        </button>

        {/* Mobile Menu Drawer */}
        <div className={`mobile-drawer ${isMobileMenuOpen ? 'active' : ''}`}>
          <div className="drawer-overlay" onClick={closeMobileMenu}></div>
          <div className="drawer-content">
            <div className="drawer-header">
              <Logo size="small" />
              <button
                type="button"
                className="drawer-close-btn"
                onClick={closeMobileMenu}
                aria-label="Close menu"
              >
                &times;
              </button>
            </div>
            <nav className="mobile-nav">
              <ul className="mobile-nav-list">
                {navLinks.map((link) => (
                  <li key={link.name} className="mobile-nav-item">
                    <a href={link.href} className="mobile-nav-link" onClick={closeMobileMenu}>
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
            <div className="mobile-auth-actions">
              <Button variant="outline" fullWidth size="md" onClick={closeMobileMenu}>
                Login
              </Button>
              <Button variant="primary" fullWidth size="md" onClick={closeMobileMenu}>
                Sign Up
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
