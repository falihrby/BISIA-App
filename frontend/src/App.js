// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './pages/Home';
import Dictionary from './pages/Dictionary';
import Footer from './components/Footer';
import ScrollToTop from './components/ScrollToTop'; 
import 'bootstrap/dist/css/bootstrap.min.css'; 
import './App.css';

function App() {
  return (
    <div className="text-center">
      <ScrollToTop /> {/* This ensures scroll-to-top behavior */}
      <NavBar />
      <div className="container mt-5">
        <Routes>
          <Route path="/" element={<Home />} />           {/* Home Page */}
          <Route path="/dictionary" element={<Dictionary />} /> {/* Dictionary Page */}
        </Routes>
      </div>
      <Footer />  {/* Add Footer at the bottom */}
    </div>
  );
}

export default App;
