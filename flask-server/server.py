# from flask import Flask, request
# from flask_cors import CORS
# import os

# import matplotlib.pyplot as plt
# import numpy as np

# from impedance.models.circuits import CustomCircuit
# from impedance import preprocessing

# app = Flask(__name__)

# app = Flask(__name__)
# CORS(app)

# @app.route("/members")
# def members():
#     return {
#         "members": ["member1", "member2"]
#     }

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return 'No file part', 400

#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file', 400

#     # Here you can process the file as needed
#     # For example, save it to disk
#     file.save('./exampleData.csv')

#     ########################################################################

#     frequencies, Z = preprocessing.readCSV('./exampleData.csv')
#     # keep only the impedance data in the first quandrant
#     frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

#     circuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200], circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-Wo_1')
#     circuit.fit(frequencies, Z)

#     # plot_path = os.path.join('./plots', 'impedance_plot.png')
#     # circuit.plot(f_data=frequencies, Z_data=Z, save_plot=plot_path)
#     print("circuit", circuit)

#     return 'File uploaded successfully', 200




# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, request, jsonify
from flask_cors import CORS
import os

import matplotlib.pyplot as plt
import numpy as np

from impedance.models.circuits import CustomCircuit
from impedance import preprocessing

app = Flask(__name__)

app = Flask(__name__)
CORS(app)
import matplotlib
matplotlib.use('agg')

@app.route("/members")
def members():
    return {
        "members": ["member1", "member2"]
    }

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return 'No file part', 400

#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file', 400

#     # Here you can process the file as needed
#     # For example, save it to disk
#     file.save('./exampleData.csv')

#     ########################################################################

#     frequencies, Z = preprocessing.readCSV('./exampleData.csv')
#     # keep only the impedance data in the first quandrant
#     frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

#     circuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200], circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-Wo_1')
#     # circuit.fit(frequencies, Z)
#     print("circuit", circuit)
#     impedance = circuit.predict(frequencies)

#     # Generate the Bode plot
#     plt.figure()
#     plt.semilogx(frequencies, np.abs(impedance))
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Magnitude (Ohm)')
#     plt.title('Bode Plot')
    
#     # Ensure 'static' directory exists
#     os.makedirs('./static', exist_ok=True)

#     # Save the plot as an image file
#     plot_path = './static/bode_plot.png'
#     plt.savefig(plot_path)

#     # Close the plot to free up memory
#     plt.close()

#     # Return the path to the saved plot
#     # return jsonify({'plot_url': plot_path})
   

#     return 'File uploaded successfully', 200




# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import numpy as np
import plotly.graph_objs as go

from impedance.models.circuits import CustomCircuit
from impedance import preprocessing

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Here you can process the file as needed
    # For example, save it to disk
    file.save('./exampleData.csv')
    return 'File uploaded successfully', 200 




@app.route('/plot_image')
def plot_image():

    frequencies, Z = preprocessing.readCSV('./exampleData.csv')
    # keep only the impedance data in the first quandrant
    frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

    circuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200], circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-Wo_1')
    # circuit.fit(frequencies, Z)
    print("circuit", circuit)
    impedance = circuit.predict(frequencies)

    # Generate the Bode plot
    plt.figure()
    plt.semilogx(frequencies, np.abs(impedance))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (Ohm)')
    plt.title('Bode Plot')
    
    # Ensure 'static' directory exists
    os.makedirs('./static', exist_ok=True)

    # Save the plot as an image file
    plot_path = './static/bode_plot.png'
    plt.savefig(plot_path)

    # Generate the equivalent circuit model
    # circuit_model_path = './static/circuit_model.png'
    # circuit_model = circuit.circuit_to_svg()
    # circuit_model.write_png(circuit_model_path)

    # Close the plot to free up memory
    plt.close()

    # Create the Bode plot using Plotly
    trace = go.Scatter(x=np.log10(frequencies), y=np.log10(np.abs(impedance)), mode='lines', name='Magnitude (dB)')
    layout = go.Layout(title='Bode Plot', xaxis=dict(title='Log(Frequency)'), yaxis=dict(title='Log(Magnitude)'))
    fig = go.Figure(data=[trace], layout=layout)

    # Ensure 'static' directory exists
    os.makedirs('./static', exist_ok=True)
    
    # Save the plot as an HTML file
    plot_path = './static/bode_plot.html'
    fig.write_html(plot_path)

    # Serve the saved plot image
    return send_file('./static/bode_plot.png', mimetype='image/png')

@app.route('/circuit_model_image')
def circuit_model_image():

    frequencies, Z = preprocessing.readCSV('./exampleData.csv')
    # keep only the impedance data in the first quandrant
    frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

    circuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200], circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-Wo_1')
    # circuit.fit(frequencies, Z)
    # print("circuit", circuit)
    # impedance = circuit.predict(frequencies)

    # # Generate the Bode plot
    # plt.figure()
    # plt.semilogx(frequencies, np.abs(impedance))
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Magnitude (Ohm)')
    # plt.title('Bode Plot')
    
    # Ensure 'static' directory exists
    os.makedirs('./static', exist_ok=True)

    # Save the plot as an image file
    # plot_path = './static/bode_plot.png'
    # plt.savefig(plot_path)

    # Generate the equivalent circuit model plot
    circuit_model = circuit.plot(f_data=frequencies, Z_data=Z, show=False)
    circuit_model_path = './static/circuit_model.png'
    circuit_model.savefig(circuit_model_path)
    
    plt.close(circuit_model)




    # Serve the saved circuit model image
    return send_file('./static/circuit_model.png', mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
