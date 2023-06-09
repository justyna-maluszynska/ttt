var socketio = io.connect(
  "http://" + document.domain + ":" + location.port + "/room"
);
