from flask import Flask, request, render_template
# import jsonify
import backend.backend as backend

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    state = None
    if request.method == 'POST':
        state = request.form.get('state')
    return render_template('index.html', state=state)

@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.json
    state_name = data.get('state')
    # Process the state name as needed
    # For example, you can pass it to your model function
    # and return the result
    # result = {'message': f'Received state: {state_name}'}
    result = backend.pred_disaster(state_name)
    return result

if __name__ == '__main__':
    app.run(debug=True)
