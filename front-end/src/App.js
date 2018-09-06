import { Component } from 'inferno';
import './registerServiceWorker';
import './css/App.css';
import FileLoader from './components/FileLoader'
import SearchUI from './components/SearchUI'

class App extends Component {
  constructor() {
    super()

    this.state = {
      showLoader: true
    }


  }


  render() {
    return (
      <div className="app">
        <h1>Simple PDF Search Engine</h1>
        <h2>This implementation is based in <a href="https://www.youtube.com/watch?v=cY7pE7vX6MU">microsearch</a> by toastdriven.</h2>
        <FileLoader show={this.state.showLoader} startSearch={() => {this.setState({showLoader: false})}}/>
        <SearchUI show={!this.state.showLoader} newFile={() => {this.setState({showLoader: true})}}/>
      </div>
    );
  }
}

export default App;
