import {Component} from 'inferno'
import '../css/SearchUI.css'


const SearchBar = ({setStatus, setResults}) => {
    return (
        <input id="search_bar" type="text" placeholder="Search" className="search-bar" onKeyUp={e => {
            const val = e.target.value

            const qry = val && val !== "" ? val : "-"
            // send the query to the API on the backend
            fetch("/query/api/" + qry)
            .then(response => response.json())
            .then(json => {
                setStatus(json.status)
                setResults(json.results)
            })
            .catch(() => {
                console.log("Search Bar: Couldn't fetch query from backend.");
                setStatus("")
                setResults("")
            })
            
        }}/>
    )
}

class SearchUI extends Component {
    constructor() {
        super()

        this.state = {
            status: "",
            results: ""
        }
    }

    render() {
        return (
            <div className="search-ui-container" style={this.props.show ? "" : "display: none"}>
                <button onClick={() => { 
                    document.getElementById('search_bar').value = ""
                    this.props.newFile()
                }
                }>New file</button>
                <SearchBar 
                    setStatus={s => { this.setState({status: s}) }} 
                    setResults={r => { this.setState({results: r}) }}
                />
                <h2 className="status" dangerouslySetInnerHTML={{__html: this.state.status}}></h2>
                <div className="result-container">
                    <h2 className="result" dangerouslySetInnerHTML={{__html: this.state.results}}></h2>
                </div>
            </div>
        )
    }
}

export default SearchUI