import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBmoLmv_kIKPmnLd3kc1b8PsDh9w15WKUg",
  authDomain: "advertisementhub-2257f.firebaseapp.com",
  projectId: "advertisementhub-2257f",
  storageBucket: "advertisementhub-2257f.appspot.com",
  messagingSenderId: "1043840614052",
  appId: "1:1043840614052:web:da73c599b7db9fcda97031"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
auth.languageCode = 'en';

const provider = new GoogleAuthProvider();