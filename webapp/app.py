from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkMessage', methods = ['POST'])
def checkMessage():
    message = request.form['message']
    # TODO: Procesar el mensaje con el modelo entrenado de la IA
    return message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
