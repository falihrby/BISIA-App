// frontend/src/pages/Home.js
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './Home.css';

const Home = () => {
  const [isCameraOn, setIsCameraOn] = useState(false);

  const startWebcam = () => {
    setIsCameraOn(true);
  };

  const stopWebcam = () => {
    setIsCameraOn(false);
  };

  return (
    <div className="content-wrapper">
      <main className="container-fluid mt-3">
        <div className="row justify-content-between align-items-start">
          <section className="col-md-6 mb-4 text-start">
            <header className="text-dark">
              <h1 className="h2 fw-bold">Real-time Hand Landmarks</h1>
              <p className="mt-2">Turn on the camera to view hand landmarks in real-time.</p>
            </header>

            <div className="mt-4">
              {isCameraOn ? (
                <button className="btn btn-danger px-4 py-2" onClick={stopWebcam}>Turn Off Camera</button>
              ) : (
                <button className="btn btn-primary px-4 py-2" onClick={startWebcam}>Turn On Camera</button>
              )}
              <p className="mt-2 text-muted small">Ensure your browser allows camera access.</p>
            </div>
          </section>

          <aside className="col-md-5 mb-4 text-start">
            <div className="webcam-container">
              {/* Display processed video stream from the backend */}
              {isCameraOn ? (
                <img
                  src="http://localhost:5000/video_feed"
                  alt="Real-time hand landmark detection"
                  className="w-100 rounded"
                />
              ) : (
                <div className="camera-off-overlay">
                  <i className="bi bi-camera-video-off-fill"></i>
                </div>
              )}
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
};

export default Home;
