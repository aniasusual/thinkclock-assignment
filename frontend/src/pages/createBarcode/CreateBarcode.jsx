import React, { useRef, useState } from 'react';
import "./createBarcode.scss";
// import Barcode from 'react-barcode';
import { ArrowBack, GetApp } from '@material-ui/icons'
import { Link } from "react-router-dom";
import { Fab } from '@material-ui/core'
import { useBarcode } from '@createnextapp/react-barcode'
import axios from "axios"




const CreateBarcode = () => {
    const [image, setImage] = useState(null);
    const [cellId, setCellId] = useState('null');
    const [manufacturer, setManufacturer] = useState('Molicel');
    const [model, setModel] = useState('INR21700-P45B');
    const [type, setType] = useState('Li-ion');
    const [formFactor, setformFactor] = useState('Cylindrical-21700');
    const [mass, setMass] = useState('70');
    const [height, setHeight] = useState('70.15');
    const [diameter, setDiameter] = useState('21.55');
    const [volume, setVolume] = useState('25.59');

    const [plotImageUrl, setPlotImageUrl] = useState('');
    const [modelImageUrl, setModelImageUrl] = useState('');


    const [file, setFile] = useState(null);


    const { inputRef } = useBarcode({
        value: cellId && cellId,
        options: {
            background: '#ffffff',
            // background: 'white',
        }
    });


    const downloadBarcode = () => {
        // const canvas = barcodeRef.current; // Reference to the barcode canvas
        const canvas = document.getElementById("mybarcode");
        if (!canvas) {
            console.error("Canvas element not found.");
            return;
        }
        const pngUrl = canvas
            .toDataURL("image/png")
            .replace("image/png", "image/octet-stream");
        let downloadLink = document.createElement("a");
        downloadLink.href = pngUrl;
        downloadLink.download = "barcode.png";
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    };


    // Function to generate a random 10-digit number
    const generateRandomNumber = () => {
        return Math.floor(1000000000 + Math.random() * 9000000000);
    };

    // Function to handle form submission
    const handleSubmit = (event) => {
        event.preventDefault();

        // Generate unique Cell ID and Bar Code
        const newCellId = generateRandomNumber();

        setCellId(newCellId);
    };

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        try {
            const formData = new FormData();
            formData.append('file', file);
            const response = await axios.post('http://127.0.0.1:5000/upload', formData);
            // console.log(response.data);
            // Handle success
            console.log("File uploaded successfully");
        } catch (error) {
            // Handle error
        }
    };

    const handleResults = async () => {
        const fetchBodePlot = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/plot_image');
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setPlotImageUrl(url);
            } catch (error) {
                console.error('Error fetching Bode plot image:', error);
            }
        };

        const fetchModel = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/circuit_model_image');
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setModelImageUrl(url); // Assuming you have a state variable named 'modelImageUrl' to store the URL of the circuit model image
            } catch (error) {
                console.error('Error fetching circuit model image:', error);
            }
        };

        fetchBodePlot();
        fetchModel();

        // Cleanup function to revoke the object URLs
        return () => {
            URL.revokeObjectURL(plotImageUrl);
            URL.revokeObjectURL(modelImageUrl);
        };
    };



    return (
        <div id='createBarcode' className={cellId !== "null" ? "showBar" : "hideBar"}>
            <Link to="/" id='backArrow'>
                <Fab style={{ marginRight: 10 }} color="secondary">
                    <ArrowBack />
                </Fab>
            </Link>
            <div id="cellInformationForm">
                <h2>Cell Information Form</h2>
                <form onSubmit={handleSubmit}>

                    <div className='formItems'>
                        <label htmlFor="image">Upload Cell Image:</label>
                        <input type="file" id="image" name="image" accept="image/*" onChange={(e) => setImage(e.target.files && e.target.files[0])} required />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="cellId">Cell ID:</label>
                        <input type="text" id="cellId" name="cellId" value={cellId} readOnly />
                    </div>

                    <div className='formItems'>
                        <label for="cellCondition">Choose Cell Condition: </label>
                        <select name="cellCondition" id="cellCondition">
                            {/* <option value="" disabled selected>Select option</option> */}
                            <option value="recycled" selected>Recycled</option>
                            <option value="new">New</option>
                        </select>
                    </div>

                    <div className='formItems'>
                        <label htmlFor="manufacturer">Manufacturer: </label>
                        <input type="text" id="manufacturer" name="manufacturer" value={manufacturer} onChange={(e) => setManufacturer(e.target.value)} />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="model">Model: </label>
                        <input type="text" id="model" name="model" value={model} onChange={(e) => setModel(e.target.value)} />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="type">Type: </label>
                        <input type="text" id="type" name="type" value={type} onChange={(e) => setType(e.target.value)} />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="formFactor">Form factor:</label>
                        <input type="text" id="formFactor" name="formFactor" value={formFactor} onChange={(e) => setformFactor(e.target.value)} />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="mass">Mass(g): </label>
                        <input type="text" id="mass" name="mass" value={mass} onChange={(e) => setMass(e.target.value)} />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="height">Height (mm): </label>
                        <input type="text" id="height" name="height" value={height} onChange={(e) => setHeight(e.target.value)} />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="diameter">Diameter (mm): </label>
                        <input type="text" id="diameter" name="diameter" value={diameter} onChange={(e) => setDiameter(e.target.value)} />
                    </div>

                    <div className='formItems'>
                        <label htmlFor="volume">Volume (cm^3): </label>
                        <input type="text" id="volume" name="volume" value={volume} onChange={(e) => setVolume(e.target.value)} />
                    </div>

                    {/* <div className='formItems'>
                        <label htmlFor="csvFile">Upload csv file: </label>
                        <button onClick={uploadFile}>Upload File</button>
                    </div> */}

                    <div>
                        <label htmlFor="csvFile">Upload csv file: </label>
                        <input type="file" onChange={handleFileChange} required />
                        {/* <button onClick={handleFileUpload}>Upload</button> */}
                    </div>

                    <input type="submit" value="Submit" id='submitBut' onClick={handleFileUpload} />
                </form>

            </div>

            <div id='barcodeDisplay' style={cellId !== "null" ? { display: "block" } : { display: "none" }}>
                {/* <h1>Bar code</h1> */}
                {/* <Barcode value={cellId} ref={barcodeRef} /> */}
                <canvas id="mybarcode" ref={inputRef} />

                <Fab onClick={downloadBarcode} style={{ marginLeft: 10 }} color="secondary">
                    <GetApp />
                </Fab>
            </div>

            <div className="results">
                <button onClick={handleResults}>click to see results</button>
                <h1>Click to interact</h1>
                {plotImageUrl && <Link to="http://127.0.0.1:5000/static/bode_plot.html"> <img src={plotImageUrl} alt="Bode Plot" /></Link>}
            </div>


        </div>
    );
}

export default CreateBarcode;
