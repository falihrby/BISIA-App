// src/Home.js

import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './Home.css';

const Home = () => {
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [videoError, setVideoError] = useState(false);
  const [gestureResult, setGestureResult] = useState(''); // State for the latest gesture
  const [loading, setLoading] = useState(false); // State for loading detection

  const startWebcam = async () => {
    try {
      await fetch('http://localhost:5000/start_camera'); // Start camera feed
      setIsCameraOn(true);
      setVideoError(false);
      setLoading(true); // Start loading when camera is turned on
    } catch (error) {
      setVideoError(true);
    }
  };

  const stopWebcam = async () => {
    try {
      await fetch('http://localhost:5000/stop_camera'); // Stop camera feed
      setIsCameraOn(false);
      setLoading(false); // Stop loading when camera is off
    } catch (error) {
      setVideoError(true);
    }
  };

  useEffect(() => {
    if (isCameraOn) {
      // Fetch the gesture result periodically while the camera is on
      const interval = setInterval(async () => {
        try {
          const response = await fetch('http://localhost:5000/gesture_result'); // Fetch the latest gesture result from backend
          const data = await response.json();
          if (data.gesture) {
            setGestureResult(data.gesture); // Replace the gesture result with the latest one
          }
          setLoading(false); // Stop loading once the result is received
        } catch (error) {
          setGestureResult(''); // Clear gesture result on error
          setLoading(false); // Stop loading on error
        }
      }, 1000); // Fetch result every 1 second
      return () => clearInterval(interval);
    }
  }, [isCameraOn]);

  return (
    <div className="content-wrapper">
      <main className="container-fluid mt-3">
        <div className="row justify-content-between align-items-start">
          <section className="col-md-6 mb-4 text-start">
            <header className="text-dark">
              <h1 className="h2 fw-bold">Terjemahkan <span className="gradient-text">Bahasa Isyaratmu</span></h1>
              <p className="mt-2">Ubah gerakan tangan menjadi kalimat dengan cepat dan tepat.</p>
            </header>

            {/* New Translation Result Block */}
            <div className="mt-4">
              <label htmlFor="translationResult" className="form-label text-muted fs-6">
                Hasil terjemahan
              </label>
              <div
                id="translationResult"
                role="textbox"
                aria-readonly="true"
                tabIndex={0}
                className="translation-result p-3 border rounded text-muted bg-light"
                style={{ minHeight: '150px', fontSize: '3rem', textAlign: 'center' }}
              >
                {loading ? 'Mendeteksi...' : gestureResult || '-'}
              </div>
            </div>

            <div className="mt-4">
              {isCameraOn ? (
                <button className="btn btn-danger px-4 py-2" onClick={stopWebcam}>Matikan Kamera</button>
              ) : (
                <button className="btn btn-primary px-4 py-2" onClick={startWebcam}>Nyalakan Kamera</button>
              )}
              <p className="mt-2 text-muted small">Klik 'izinkan' saat melihat perintah di browser dan pastikan pencahayaan cukup.</p>
            </div>
          </section>

          <aside className="col-md-5 mb-4 text-start">
            <div className="webcam-container">
              {isCameraOn ? (
                <img
                  src="http://localhost:5000/video_feed"
                  alt="Real-time hand landmark detection"
                  className="w-100 rounded"
                  onError={() => setVideoError(true)}
                />
              ) : (
                <div className="camera-off-overlay">
                  <i className="bi bi-camera-video-off-fill"></i>
                </div>
              )}
              {videoError && <p className="text-danger">Failed to load the video feed. Check the backend connection.</p>}
            </div>

            <div className="mt-2 p-2 bg-light border border-info rounded lh-sm">
              <small>
                Privasi kamu penting bagi kami
                <span className="text-primary">. Kami tidak menyimpan atau mengirimkan data dari aktivitas ini. Informasi pribadi kamu tetap aman sepanjang proses.</span>
              </small>
            </div>
          </aside>
        </div>

        <div className="sign-language-info my-5 p-4">
          <h4 className="text-center text-white mb-5">Sudah Tahu Bahasa Isyarat Ini?</h4>
          <div className="d-flex flex-wrap justify-content-around align-items-center mt-4"> 
            {[{ imageSrc: '/kalimat-isyarat/halo.png', text: 'Halo' },
              { imageSrc: '/kalimat-isyarat/sekarang.png', text: 'Sekarang' },
              { imageSrc: '/kalimat-isyarat/lihat.png', text: 'Lihat' },
              { imageSrc: '/kalimat-isyarat/tanya.png', text: 'Tanya' },
              { imageSrc: '/kalimat-isyarat/terimakasih.png', text: 'Terimakasih' }
            ].map((item, index) => (
              <div className="text-center mx-3 mb-3" key={index}>
                <img src={item.imageSrc} className="rounded-circle mb-2" alt={item.text} />
                <p>{item.text}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
