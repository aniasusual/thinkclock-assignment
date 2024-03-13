import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

import Home from './pages/home/Home'
import CreateBarcode from './pages/createBarcode/CreateBarcode';
import BarcodeScanner from './pages/barcodeScanner/BarcodeScanner';

function App() {

  return (
    <div className="App">
      <div className="App-header">

        <Router>
          <Routes>

            <Route path="/" element={<Home />} />
            <Route path="/barcode_generator" element={<CreateBarcode />} />
            <Route path="/barcode_scanner" element={<BarcodeScanner />} />

          </Routes>
        </Router>

      </div>
    </div>
  );
}

export default App;
