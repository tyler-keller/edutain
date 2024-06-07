import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { getStorage } from "firebase/storage";
import { writable } from "svelte/store";

const firebaseConfig = {
  apiKey: "AIzaSyDnjYoSejcfxTsDre4SlrYo6awAx8rOaGE",
  authDomain: "edutain-5d994.firebaseapp.com",
  projectId: "edutain-5d994",
  storageBucket: "edutain-5d994.appspot.com",
  messagingSenderId: "13942862049",
  appId: "1:13942862049:web:f7768539dc2669defc47a0",
  measurementId: "G-KZHQRZXDCZ"
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth();
export const db = getFirestore();
export const storage = getStorage();

// user store from fireship course

function userStore() {
  let unsubscribe = () => {};

  // create a writable store w/ subscribe method
  // set initial value to current user or null
  const { subscribe } = writable(auth?.currentUser ?? null, (set) => {
    // subscribe to auth state changes and set user on change
    unsubscribe = onAuthStateChanged(auth, (user) => {
      set(user);
    });

    return () => unsubscribe();
  });

  return {
    subscribe,
  };
}

export const user = userStore();