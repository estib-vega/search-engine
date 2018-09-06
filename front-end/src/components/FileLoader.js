import {Component} from 'inferno'
import '../css/FileLoader.css'

// file input tag
// when  file is selected, the button for uploading is shown
const FileInput = ({loader, disabled}) => {
    return (
        <input disabled={disabled} 
            id="input_file" 
            type="file" 
            name="input_file" 
            className="inputfile" 
            accept=".pdf"
            onChange={ (e) => {
                const files = e.target.files.length 
                
                // if has at least one file, then display the upload button and the name of the
                // pdf file to be uploaded
                if(files > 0) {
                    const f = e.target.files[0]
                    const filename = f.name
                    loader.setState({
                        hideUpload: false,
                        fileName: filename,
                        file: f
                    })
                }
                
            }}
        />
    )
}

// button for upload
// sends the file to the back end and awaits an answer
const UploadButton = ({loader, startSearch, disabled, hidden}) => {
    return (
        <button disabled={disabled} hidden={hidden}
            onClick={ (e) => {
                e.preventDefault()

                const f = loader.state.file

                // if there is a file stored in state
                if(f) {
                    // start loading state
                    loader.setState({loadingState: true})

                    var fd = new FormData()
                    fd.append('file', f)
                    
                    // post it to the backend
                    fetch("/fileupload", {
                        method: 'POST',
                        body: fd
                    })
                    .then( response => response.json())
                    .then( json => {
                        // if it was successful, display search ui
                        // else show error message and ask for a different pdf file
                        if(json.msg === "succesfull") {
                            startSearch()
                        }
                        else {
                            console.log('Upload button: Server responded with unsuccessful.');
                        }

                        loader.setState({
                            hideUpload: true,
                            fileName: "",
                            file: null,
                            loadingState: false
                        })
                    })
                    .catch( () => {
                        console.log("Upload button: Unsuccessful postage of data.")
                        loader.setState({
                            hideUpload: true,
                            fileName: "",
                            file: null,
                            loadingState: false
                        })
                    })
                }

        }}>{disabled? "Loading..." : "Upload " + loader.state.fileName}</button>
    )
}


class FileLoader extends Component {
    constructor() {
        super()

        this.state = {
            hideUpload: true,
            fileName: "",
            file: null,
            loadingState: false
        }
    }

    render () {
        return (
            <div className="form-container" style={this.props.show ? "" : "display: none"}>
                <form>
                    <FileInput loader={this} disabled={this.state.loadingState}/>
                    <label for="input_file" className={this.state.loadingState? "loadlabel" : ""}>{this.state.hideUpload ? "Choose a pdf file" : "Change pdf file"}</label>
                    <UploadButton loader={this} hidden={this.state.hideUpload} startSearch={this.props.startSearch} disabled={this.state.loadingState}/>
                </form>
            </div>
        )
    }
}

export default FileLoader