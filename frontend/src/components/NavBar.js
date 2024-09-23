import React, { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'; 
import './NavBar.css'; 

function NavBar() {
  const [shadow, setShadow] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 0) {
        setShadow(true);  
      } else {
        setShadow(false); 
      }
    };

    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <nav className={`navbar navbar-expand-lg navbar-light bg-custom fixed-top ${shadow ? 'navbar-scroll-shadow' : ''}`}>
      <div className="container-fluid navbar-padding">
        <NavLink className="navbar-brand d-flex align-items-center" to="/">  
          <img src="/bisia-logo+teks.png" alt="BISIA Logo" style={{ height: '60px', width: 'auto' }} />
        </NavLink>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto" style={{ gap: '20px' }}>
            <li className="nav-item">
              {/* Removed exact, used function to apply active class */}
              <NavLink 
                className={({ isActive }) => isActive ? 'nav-link fw-bolder' : 'nav-link'} 
                to="/"
              >
                Beranda
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink 
                className={({ isActive }) => isActive ? 'nav-link fw-bolder' : 'nav-link'} 
                to="/courses"
              >
                Kursus
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink 
                className={({ isActive }) => isActive ? 'nav-link fw-bolder' : 'nav-link'} 
                to="/dictionary"
              >
                Kamus
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
