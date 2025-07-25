from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, AWS Diagnostic Tool!'

if __name__ == '__main__':
    print("Starting simple Flask test...")
    app.run(host='0.0.0.0', port=5002, debug=True) 