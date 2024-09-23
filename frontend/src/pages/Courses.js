import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';  

function Courses() {
  return (
    <div className="content-wrapper">
      <div className="container mt-3">
        <h1 className="text-center">Our Courses</h1>
        <p className="text-center">Explore a variety of courses to enhance your skills in different areas.</p>
        
        <section className="mt-4">
          <h2 className="text-center">Available Courses</h2>
          <ul className="list-group list-group-flush mx-auto w-50">
            <li className="list-group-item">Introduction to Web Development</li>
            <li className="list-group-item">Advanced React Techniques</li>
            <li className="list-group-item">Database Management with SQL</li>
            <li className="list-group-item">Python for Data Science</li>
          </ul>
        </section>
      </div>
    </div>
  );
}

export default Courses;
