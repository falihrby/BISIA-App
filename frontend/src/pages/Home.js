// frontend/src/pages/Home.js
import React, { useRef, useEffect, useState, useCallback } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './Home.css';
import axios from 'axios';

const Home = () => {
  const videoRef = useRef(null);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [gestureResult, setGestureResult] = useState('Terjemahan gerakan tangan kamu akan muncul disini...');
  const [isSending, setIsSending] = useState(false);
  const [loading, setLoading] = useState(false);
  const [processedImage, setProcessedImage] = useState(null);

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

  // Capture frame for real-time processing
  const captureFrame = useCallback(async () => {
    if (videoRef.current && !isSending) {
      setIsSending(true);
      setLoading(true);

      const video = videoRef.current;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const frame = canvas.toDataURL('image/jpeg');

      // Convert base64 frame to Blob
      const blob = await fetch(frame).then(res => res.blob());

      const formData = new FormData();
      formData.append('frame', blob);

      try {
        // POST request to backend to detect gesture and get processed image with landmarks
        const response = await axios.post('http://localhost:5000/detect-gesture', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          responseType: 'blob'  // Expect a binary response
        });

        const imgURL = URL.createObjectURL(response.data);  // Create an object URL for the image blob
        setProcessedImage(imgURL);  // Update state to display processed image
        setGestureResult('Gesture processed');  // Update text for the gesture result
      } catch (error) {
        console.error('Error detecting gesture:', error);
      } finally {
        setIsSending(false);
        setLoading(false);
      }
    }
  }, [isSending]);

  // Real-time loop using requestAnimationFrame
  const processVideo = useCallback(() => {
    if (isCameraOn) {
      captureFrame();  // Capture each frame and process it
      requestAnimationFrame(processVideo);  // Continue the loop for real-time detection
    }
  }, [isCameraOn, captureFrame]);

  useEffect(() => {
    if (isCameraOn) {
      processVideo();  // Start the real-time processing loop
    }
  }, [isCameraOn, processVideo]);

  return (
    <div className="content-wrapper">
      <main className="container-fluid mt-3">
        <div className="row justify-content-between align-items-start">
          <section className="col-md-6 mb-4 text-start">
            <header className="text-dark">
              <h1 className="h2 fw-bold">Terjemahkan <span className="gradient-text">Bahasa Isyaratmu</span></h1>
              <p className="mt-2">Ubah gerakan tangan menjadi kalimat dengan cepat dan tepat.</p>
            </header>

            <div className="mt-4">
              <label htmlFor="translationResult" className="form-label text-muted fs-6">
                Hasil terjemahan
              </label>
              <div id="translationResult" role="textbox" aria-readonly="true" tabIndex={0}
                className="translation-result p-3 border rounded text-muted bg-light small text-muted"
                style={{ minHeight: '150px', fontSize: '0.9rem' }}>
                {loading ? 'Mendeteksi...' : gestureResult}
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
            <div className={`webcam-container ${!isCameraOn ? 'bg-secondary' : ''}`}>
              {/* Display processed image from backend if available */}
              {processedImage ? (
                <img src={processedImage} alt="Processed with landmarks" className="w-100 rounded" />
              ) : (
                <video ref={videoRef} autoPlay playsInline className="w-100 rounded"></video>
              )}
              {!isCameraOn && (
                <div className="camera-off-overlay">
                  <i className="bi bi-camera-video-off-fill"></i>
                </div>
              )}
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
