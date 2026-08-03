import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';

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

import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import VerifyEmailPage from './pages/VerifyEmailPage';
import ProfilePage from './pages/ProfilePage';
import DashboardPage from './pages/DashboardPage';
import RBACAdminPage from './pages/RBACAdminPage';

import './App.css';

function LandingPage() {
  return (
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
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="app-container">
          <Navbar />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route path="/reset-password" element={<ResetPasswordPage />} />
            <Route path="/verify-email" element={<VerifyEmailPage />} />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/rbac"
              element={
                <ProtectedRoute requiredRole="ADMINISTRATOR">
                  <RBACAdminPage />
                </ProtectedRoute>
              }
            />
          </Routes>
          <Footer />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
