import React from 'react';
import Navbar from './components/Navbar/Navbar';
import Hero from './components/Hero/Hero';
import SearchPanel from './components/SearchPanel/SearchPanel';
import FeaturedPets from './components/FeaturedPets/FeaturedPets';
import HowItWorks from './components/HowItWorks/HowItWorks';
import Features from './components/Features/Features';
import Statistics from './components/Statistics/Statistics';
import ShelterBanner from './components/ShelterBanner/ShelterBanner';
import Testimonials from './components/Testimonials/Testimonials';
import CTA from './components/CTA/CTA';
import Footer from './components/Footer/Footer';
import './App.css';

function App() {
  return (
    <div className="app-container">
      {/* Sticky Navigation Bar */}
      <Navbar />

      {/* Main Landing Page Sections */}
      <main className="main-content">
        <Hero />
        <SearchPanel />
        <FeaturedPets />
        <HowItWorks />
        <Features />
        <Statistics />
        <ShelterBanner />
        <Testimonials />
        <CTA />
      </main>

      {/* Footer Section */}
      <Footer />
    </div>
  );
}

export default App;
