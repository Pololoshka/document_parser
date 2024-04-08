import "./App.css";
import Home from "./components/Home";
import Bar from "./components/Bar";

function App() {
  return (
    <div className="App">
      <Bar content={<Home />} />
    </div>
  );
}

export default App;
