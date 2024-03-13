from flask import Flask, request, jsonify, send_file, render_template
import schemdraw
import matplotlib
matplotlib.use('agg')  # Set Matplotlib backend before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
from impedance.models.circuits import CustomCircuit
from impedance import preprocessing
from flask_cors import CORS
import os
import plotly.graph_objs as go

# Define the initial guesses for the parameters
initial_guesses = {
    'R_0': 1.00e-02,
    'R_1': 5.00e-03,
    'C_1': 1.00e-01,
    'R_2': 5.00e-03,
    'C_2': 1.00e-01,
    'Wo_1_0': 1.00e-03,
    'Wo_1_1': 200
}

# Define the minimum and maximum values for each parameter (for visual indication)
min_max_values = {
    'R_0': (1e-3, 1e1),
    'R_1': (1e-3, 1e1),
    'C_1': (1e-3, 1e1),
    'R_2': (1e-3, 1e1),
    'C_2': (1e-3, 1e1),
    'Wo_1_0': (1e-4, 1e-2),
    'Wo_1_1': (10, 1000)
}

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
    # Read data from the CSV file
    frequencies, Z = preprocessing.readCSV('./exampleData.csv')
    # keep only the impedance data in the first quandrant
    frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

    # Fit the data to a CustomCircuit model
    circuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200], circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-Wo_1')
    impedance = circuit.predict(frequencies)

    # Ensure 'static' directory exists
    os.makedirs('./static', exist_ok=True)

    # Generate the equivalent circuit model using schemdraw
    d = schemdraw.Drawing()
    # Draw the circuit components based on the extracted parameters from the CSV file
    # For example:
    d.add(schemdraw.elements.Resistor(label='R0'))
    d.add(schemdraw.elements.Resistor(label='R1', d='right'))
    d.add(schemdraw.elements.Capacitor(label='C1', d='down'))
    d.add(schemdraw.elements.Resistor(label='R1', d='left'))
    d.add(schemdraw.elements.Capacitor(label='C1', d='up'))
    d.add(schemdraw.elements.Dot())
    d.add(schemdraw.elements.Line('right', l=d.unit*2))
    d.add(schemdraw.elements.Capacitor(label='Wo1'))

    # Save the circuit model plot as an image
    circuit_model_path = './static/circuit_model.png'
    d.save(circuit_model_path)

    # Serve the saved circuit model image
    return send_file(circuit_model_path, mimetype='image/png')

@app.route('/table')
def index():
    # Read data from the CSV file
    frequencies, Z = preprocessing.readCSV('./exampleData.csv')
    # keep only the impedance data in the first quadrant
    frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

    # Fit the data to the CustomCircuit model
    circuit = CustomCircuit(initial_guess=list(initial_guesses.values()), circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-Wo_1')
    # circuit.fit(frequencies, Z)
    print("circuit", circuit)
    impedance = circuit.predict(frequencies)

    # Generate parameter values based on the initial guesses
    parameter_values = {key: [initial_guesses[key]] for key in initial_guesses}

    # Generate visually indicated values
    visual_indicators = {}
    for key in initial_guesses:
        min_val, max_val = min_max_values[key]
        val = initial_guesses[key]
        visual_indicator = 'Normal'
        if val < min_val:
            visual_indicator = 'Below Min'
        elif val > max_val:
            visual_indicator = 'Above Max'
        visual_indicators[key] = visual_indicator

    # Generate the HTML table
    table_html = "<table>"
    table_html += "<tr><th>Parameter</th><th>Value</th><th>Explanation</th><th>Visual Indicator</th></tr>"
    for key in initial_guesses:
        min_val, max_val = min_max_values[key]
        val = initial_guesses[key]
        explanation = ''  # Add explanation here if needed
        visual_indicator = visual_indicators[key]
        table_html += f"<tr><td>{key}</td><td>{val}</td><td>{explanation}</td><td>{visual_indicator}</td></tr>"
    table_html += "</table>"

    # Save the table as an image
    plt.figure(figsize=(8, 6))
    plt.axis('off')
    plt.table(cellText=table_html, loc='center')
    table_image_path = './static/table_image.png'
    plt.savefig(table_image_path)
    plt.close()

    # Send the path of the table image to the frontend
    return send_file(table_image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
