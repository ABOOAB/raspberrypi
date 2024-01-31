
import logo from './logo.svg';
import './App.css';

function App() {
  
  
  const on = () => {
    fetch('http://192.168.166.241:5000/on')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Handle successful response
      })
      .catch(error => {
        console.error('Error during fetch:', error);
      });
  };

  const off = () => {
    fetch('http://192.168.166.241:5000/off')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Handle successful response
      })
      .catch(error => {
        console.error('Error during fetch:', error);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
       
        <button onClick={on}> open the door</button>
        <button onClick={off}> close the door</button>
      </header>
    </div>
  );
}

export default App;