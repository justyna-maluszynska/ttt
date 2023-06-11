#!/bin/env python
from web.app import create_app
from web.extensions import socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)
