import React, { useRef, useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css'; 
import './Home.css'; 

const Home = () => {
  const videoRef = useRef(null);
  const [isCameraOn, setIsCameraOn] = useState(false);  

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setIsCameraOn(true);  
    } catch (err) {
      console.error('Error accessing the webcam:', err);
    }
  };

  const stopWebcam = () => {
    const video = videoRef.current;
    if (video && video.srcObject) {
      const tracks = video.srcObject.getTracks();
      tracks.forEach(track => track.stop());  
      video.srcObject = null;  
    }
    setIsCameraOn(false);  
  };

  useEffect(() => {
    // Cleanup function to stop the webcam when component unmounts
    return () => {
      stopWebcam();
    };
  }, []);

  return (
    <div className="content-wrapper">
      <main className="container-fluid mt-3">
        <div className="row justify-content-between align-items-start">
          {/* Left container */}
          <section className="col-md-6 mb-4 text-start">
            <header className="text-dark">
              <h1 className="h2 fw-bold">Terjemahkan <span className="gradient-text">Bahasa Isyaratmu</span></h1>
              <p className="mt-2">
                Ubah gerakan tangan menjadi kalimat dengan cepat dan tepat.
              </p>
            </header>

            <div className="mt-4">
              <label htmlFor="translationResult" className="form-label text-muted fs-6">
                Hasil terjemahan
              </label>
              <div
                id="translationResult"
                role="textbox"
                aria-readonly="true"
                tabIndex={0}
                className="translation-result p-3 border rounded text-muted bg-light small text-muted"
                style={{ minHeight: '150px', fontSize: '0.9rem' }}
              >
                Terjemahan gerakan tangan kamu akan muncul disini...
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

          {/* Right container with webcam box */}
          <aside className="col-md-5 mb-4 text-start" style={{ position: 'relative' }}>
            <div className={`webcam-container ${!isCameraOn ? 'bg-secondary' : ''}`}>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-100 rounded"
              ></video>
              {!isCameraOn && (
                <div className="camera-off-overlay">
                  <i className="bi bi-camera-video-off-fill"></i>
                </div>
              )}
            </div>

            {/* Vector Image */}
            <img 
              src={`${process.env.PUBLIC_URL}/vector-1.png`} 
              alt="Vector Graphic" 
              className="vector-img" 
            />

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
      </main>
    </div>
  );
};

export default Home;
