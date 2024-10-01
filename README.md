# BISIA Application

<img src="frontend/public/bisia-logo+teks.png" alt="BISIA Logo" width="300"/>

## Project Objective
The **BISIA Application** aims to create an interactive platform to help users, especially the deaf, learn **Indonesian Sign Language (BISINDO)**. The primary feature of the application is real-time hand gesture detection using the device’s camera, allowing users to practice and receive feedback on their sign language skills.

---

## Main Features

### 1. Hand Gesture Detection Using Camera:
- **Interactive Learning**: 
  Users can use their device's camera to detect and analyze hand gestures while practicing sign language.
  
- **AI and Computer Vision**: 
  The system is powered by AI (using TensorFlow and MediaPipe) and computer vision technologies to ensure real-time feedback on the user’s hand gestures.
  
- **Real-Time Feedback**: 
  The application provides instant feedback on the user's gestures, allowing users to adjust their signs for better accuracy. Detected gestures are displayed on the screen for easy reference.

### 2. Indonesian Sign Language Dictionary:
- A comprehensive **Indonesian Sign Language (BISINDO)** dictionary is available. Users can search and learn individual signs for both **letters** and **numbers** using the search feature.
  
- **Searchable Database**: 
  Users can input letters or numbers to search for corresponding signs. The system offers results based on user input and provides images of the hand gestures for easier learning.

---

## Technologies Used
### Frontend:
- **React.js**: 
  The frontend is built using React.js for a dynamic and responsive user interface.
  
- **Bootstrap**: 
  Bootstrap is used for responsive design and ensuring a mobile-friendly experience.
  
- **React Router**: 
  Enables smooth navigation between different pages such as the **Home** and **Dictionary** pages.
  
- **WebRTC**: 
  Enables real-time webcam access to allow gesture recognition in the browser.

### Backend:
- **Python (Flask)**: 
  Flask is used to handle backend services, including gesture recognition, webcam streaming, and gesture result fetching.
  
- **OpenCV and MediaPipe**: 
  OpenCV handles webcam input, and **MediaPipe** is used to process hand landmarks and detect gestures in real-time.
  
- **Flask-CORS**: 
  Enables Cross-Origin Resource Sharing to ensure seamless frontend-backend communication.

### AI and Gesture Recognition:
- **TensorFlow.js**: 
  Although initially considered for gesture recognition, **MediaPipe** (in combination with Python's OpenCV) is used to track hand movements and identify gestures.
  
- **Custom Gesture Detection**: 
  Each letter of the **BISINDO alphabet** is mapped to custom detection algorithms that recognize specific hand positions. The gestures are detected based on hand landmarks tracked by MediaPipe, processed in real-time by the backend.
  
---

## Contribution

We welcome contributions from the community. If you would like to contribute to this project, please open a new issue or submit a pull request after making changes.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

For further questions or technical support, please contact us at [falihrahmat534@gmail.com](mailto:falihrahmat534@gmail.com).

Visit our website: [BISIA App]( )

![Beranda Screenshot](frontend/public/screenshoot-beranda.png)

![Kamus Screenshot](frontend/public/screenshoot-kamus.png)