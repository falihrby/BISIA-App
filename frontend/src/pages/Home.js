// src/Home.js

import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './Home.css';

const Home = () => {
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [videoError, setVideoError] = useState(false);
  const [gestureResult, setGestureResult] = useState(''); // Latest gesture result
  const [loading, setLoading] = useState(false); // Loading state for detection

  const startWebcam = async () => {
    try {
      await fetch('http://localhost:5000/start_camera');
      setIsCameraOn(true);
      setVideoError(false);
      setLoading(true);
    } catch (error) {
      setVideoError(true);
    }
  };

  const stopWebcam = async () => {
    try {
      await fetch('http://localhost:5000/stop_camera');
      setIsCameraOn(false);
      setLoading(false);
    } catch (error) {
      setVideoError(true);
    }
  };

  useEffect(() => {
    if (isCameraOn) {
      const interval = setInterval(async () => {
        try {
          const response = await fetch('http://localhost:5000/gesture_result');
          const data = await response.json();
          if (data.gesture) {
            setGestureResult(data.gesture);
          }
          setLoading(false);
        } catch (error) {
          setGestureResult('');
          setLoading(false);
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
              <h1 className="h2 fw-bold">
                Terjemahkan <span className="gradient-text">Bahasa Isyaratmu</span>
              </h1>
              <p className="mt-2">Ubah gerakan tangan menjadi kalimat dengan cepat dan tepat.</p>
            </header>

            {/* Translation Result */}
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
                <button className="btn btn-danger px-4 py-2" onClick={stopWebcam}>
                  Matikan Kamera
                </button>
              ) : (
                <button className="btn btn-primary px-4 py-2" onClick={startWebcam}>
                  Nyalakan Kamera
                </button>
              )}
              <p className="mt-2 text-muted small">
                Klik 'izinkan' saat melihat perintah di browser dan pastikan pencahayaan cukup.
              </p>
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
              {videoError && (
                <p className="text-danger">
                  Failed to load the video feed. Check the backend connection.
                </p>
              )}
            </div>

            <div className="mt-2 p-2 bg-light border border-info rounded lh-sm">
              <small>
                Privasi kamu penting bagi kami
                <span className="text-primary">
                  . Kami tidak menyimpan atau mengirimkan data dari aktivitas ini. Informasi pribadi kamu tetap aman sepanjang proses.
                </span>
              </small>
            </div>
          </aside>
        </div>

        {/* Sign Language Info Section */}
        <div className="sign-language-info my-5 p-4">
          <h4 className="text-center text-white mb-5">Sudah Tahu Bahasa Isyarat Ini?</h4>
          <div className="d-flex flex-wrap justify-content-around align-items-center mt-4">
            {[
              { imageSrc: '/kalimat-isyarat/halo.png', text: 'Halo' },
              { imageSrc: '/kalimat-isyarat/sekarang.png', text: 'Sekarang' },
              { imageSrc: '/kalimat-isyarat/lihat.png', text: 'Lihat' },
              { imageSrc: '/kalimat-isyarat/tanya.png', text: 'Tanya' },
              { imageSrc: '/kalimat-isyarat/terimakasih.png', text: 'Terimakasih' },
            ].map((item, index) => (
              <div className="text-center mx-3 mb-3" key={index}>
                <img src={item.imageSrc} className="rounded-circle mb-2" alt={item.text} />
                <p>{item.text}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Sign Language Learning Buddy Section */}
        <div className="sign-language-learning-buddy row justify-content-between align-items-center mb-4">
          <div className="image-section col-md-6 d-flex justify-content-center">
            <img src="/vector-2.png" alt="Sign Language Learning Buddy" className="rounded-circle" />
          </div>

          <div className="text-section col-md-5 text-start d-flex flex-column justify-content-center">
            <h4 className="fw-bold">Teman Belajar Bahasa Isyarat</h4>
            <p className="mt-1">Belajar Bahasa Isyarat Indonesia dengan cara yang mudah dan menyenangkan.</p>

            <div className="icon-container d-flex align-items-center">
              <img src="/icon-translate.png" alt="Icon" className="icon-image" />
              <div className="text-content ms-3">
                <h6 className="fw-bold">Terjemah Isyarat dengan Kamera</h6>
                <p>Terjemah isyarat real-time dengan kamera.</p>
              </div>
            </div>

            <div className="d-flex align-items-center mt-2">
              <img src="/icon-course.png" alt="Icon" className="icon-image" />
              <div className="text-content ms-3">
                <h6 className="fw-bold">Kursus BISINDO Terstruktur</h6>
                <p>Dari dasar hingga mahir dengan video tutorial.</p>
              </div>
            </div>

            <div className="d-flex align-items-center mt-4">
              <img src="/icon-dictionary.png" alt="Icon" className="icon-image" />
              <div className="text-content ms-3">
                <h6 className="fw-bold">Kamus BISINDO Praktis</h6>
                <p>Temukan isyarat yang kamu butuhkan kapan saja.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
