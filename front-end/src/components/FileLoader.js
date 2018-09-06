import {Component} from 'inferno'
import '../css/FileLoader.css'

class FileLoader extends Component {
    constructor() {
        super()

        this.state = {
            hideUpload: true,
            fileName: "",
            file: null
        }
    }

    render () {
        return (
            <div className="form-container">
                <form>
                    <input id="input_file" type="file" name="input_file" className="inputfile" accept=".pdf"
                        onChange={(e) => {
                            const files = e.target.files.length 
                            
                            // if has at least one file, then display the upload button and the name of the
                            // pdf file to be uploaded
                            if(files > 0) {
                                const f = e.target.files[0]
                                const filename = f.name
                                this.setState({
                                    hideUpload: false,
                                    fileName: filename,
                                    file: f
                                })
                            }
                            
                        }}
                    />
                    <label for="input_file">{this.state.hideUpload ? "Choose a pdf file" : "Change pdf file"}</label>
                    <button id="up_button" hidden={this.state.hideUpload} 
                    onClick={(e) => {
                        e.preventDefault()

                        const f = this.state.file

                        // if there is a file stored in state
                        if(f) {
                            // start loading state
                            // TODO!!

                            var fd = new FormData()
                            fd.append('file', f)
                            
                            // post it to the backend
                            fetch("/fileupload", {
                                method: 'POST',
                                body: fd
                              })
                              .then( response => response.json())
                              .then(json => {
                                  console.log(json);
                                  // if it was successful, display search ui
                                  // else show error message and ask for a different pdf file
                              })
                        }

                    }}>{"Upload " + this.state.fileName}</button>
                </form>
            </div>
        )
    }
}

export default FileLoader