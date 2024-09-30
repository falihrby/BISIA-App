// src/components/Footer.js

import React from 'react';
import { NavLink } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css'; // Custom styles

const Footer = () => {
  return (
    <footer className="bg-white text-center text-lg-start w-100">
      <section className="container py-3">
        <div className="row">
          {/* Company Info */}
          <div className="col-md-4 mx-auto mb-4">
            <NavLink className="navbar-brand d-flex align-items-center mb-3" to="/">  
                <img src="/bisia-logo+teks.png" alt="BISIA Logo" className="footer-logo" />
            </NavLink>
            <p className="footer-text">
                Platform No. 1 untuk belajar dan menerjemahkan Bahasa Isyarat Indonesia dengan mudah.
            </p>
          </div>

          {/* Quick Links */}
          <div className="col-md-4 mx-auto mb-4">
            <h6 className="fw-bold mb-4">Tautan</h6>
            <p><NavLink to="/" className="text-reset footer-link">Terjemah</NavLink></p>
            <p><NavLink to="/dictionary" className="text-reset footer-link">Kamus</NavLink></p>
          </div>
        </div>
      </section>

      {/* Copyright */}
      <div className="text-center bg-light py-3 w-100">
        © 2024 SIBIA. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;
