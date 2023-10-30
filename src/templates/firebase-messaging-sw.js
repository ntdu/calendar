importScripts("https://www.gstatic.com/firebasejs/8.8.0/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.8.0/firebase-messaging.js");

firebase.initializeApp({
    apiKey: "AIzaSyC-6bZPkSILcGberTGlqOAX7tiow8K6Mxw",
    authDomain: "sopdev-86855.firebaseapp.com",
    databaseURL: "https://sopdev-86855-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "sopdev-86855",
    storageBucket: "sopdev-86855.appspot.com",
    messagingSenderId: "280112674639",
    appId: "1:280112674639:web:bfce500fbf7a60f28db73a",
    measurementId: "G-DKZSNDP153"
});

const messaging = firebase.messaging();
console.log("àhadshhhhhhhhhhhhhhhhhhhhhhhhhhh")
messaging.setBackgroundMessageHandler(function(payload) {
  console.log(payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: payload.notification.image,
    data: {
      url: "https://google.com"
    }
  };

  const link = console.log("Received message:", payload.data.link);
  if (link) {
    self.clients.openWindow(link);
  }

  return self.registration.showNotification(notificationTitle, notificationOptions);
})

self.addEventListener('notificationclick', function (event) {
  console.log("notificationclick", event)
  var urlToRedirect = event.notification.data.url;
  event.notification.close();
  event.waitUntil(self.clients.openWindow(urlToRedirect));
});
