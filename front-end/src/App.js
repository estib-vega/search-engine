import { Component } from 'inferno';
import './registerServiceWorker';
import './css/App.css';
import FileLoader from './components/FileLoader'

class App extends Component {
  render() {
    return (
      <div className="App">
        <h1>Simple PDF Search Engine</h1>
        <h2>This implementation is based in microsearch by <a href="https://www.youtube.com/watch?v=cY7pE7vX6MU">toastdriven</a></h2>
        <FileLoader/>
      </div>
    );
  }
}

export default App;
