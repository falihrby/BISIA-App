// src/components/ScrollToTop.js

import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const ScrollToTop = () => {
  const { pathname } = useLocation(); // Get current location

  useEffect(() => {
    window.scrollTo(0, 0); // Scroll to top whenever the route changes
  }, [pathname]); // Re-run effect on path change

  return null;
};

export default ScrollToTop;
