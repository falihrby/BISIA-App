import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';  

function Dictionary() {
  return (
    <div className="content-wrapper">
      <div className="container text-center mt-3">
        <h1>Dictionary</h1>
        <p>Look up terms and definitions quickly in our extensive dictionary.</p>
        
        <div className="my-4">
          <input
            type="text"
            placeholder="Search for a term..."
            className="form-control input-search"
          />
        </div>
        
        <section className="mt-4">
          <p>Start typing to find the definition of a term!</p>
        </section>
      </div>
    </div>
  );
}

export default Dictionary;
