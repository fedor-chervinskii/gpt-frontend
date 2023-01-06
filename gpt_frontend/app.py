from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/example')
def example():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run()
