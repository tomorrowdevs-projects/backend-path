# Dockerizing an Image Processing Service

**Objective:** Containerize an image processing service.

**Real-world Scenario:** You have developed an application that requires image processing. By containerizing this service, you ensure it is easily deployable and manageable.

**Example Code:**
```python
# app.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    # Image processing code
    return 'Image processed successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
