import React from 'react';
import './App.css';
import CanvasDraw from "react-canvas-draw";
const axios = require('axios');

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      predictions: null,
      binary_image : null
    }
  }
  sortByValue(jsObj) {
    var sortedArray = [];
    for (var i in jsObj)
      sortedArray.push([parseFloat(jsObj[i]) * 100, i]);
    return sortedArray.sort((a, b) => b[0] - a[0]);
  }
  postImageData(imageData) {
    imageData = JSON.parse(imageData);

    let points = []
    imageData.lines.forEach(line => {
      points = points.concat(line.points)
    });

    let width = imageData.width;
    let height = imageData.height;
    let that = this;
    
    axios.post('http://10.0.0.46:5000/predict', {
      points,
      width,
      height
    })
      .then(function (response) {
        let {predictions,filename} = response.data
        predictions = that.sortByValue(predictions)
        console.table(predictions)
        that.setState({
          predictions: predictions,
          binary_image: 'http://10.0.0.46:5000/'+filename
        })
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  resetAll() {
    this.setState({ predictions: null, binary_image: null });
    this.saveableCanvas.clear()
  }

  render() {
    const { predictions, binary_image } = this.state;

    return (
      <div class="container">
        <nav class="navbar">

        </nav>
        <div class="row">
          <div class="col">
            <CanvasDraw ref={canvasDraw => (this.saveableCanvas = canvasDraw)} />
          </div>
          <div class="col">
            <h4 class="display-4 text-center">The character is</h4>
            <h1 class="display-1 text-center">{this.state.predictions && predictions[0][1]}</h1>
          </div>
          <div>
          </div>
        </div>
        <div className="row">
          <div class="col-md-6">
            <button type="button" class="btn btn-primary" onClick={() => { this.postImageData(this.saveableCanvas.getSaveData()) }}> Find </button>
            <button type="button" class="btn btn-primary" onClick={() => { this.resetAll() }}> Clear </button>
          </div>
          <div class="col-md-6 text-center">
            <div className="row">
              {this.state.predictions &&
                <div className="col">
                  <p>
                    <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#moreDetails" aria-expanded="false">More details</button>
                  </p>
                  <div class="collapse multi-collapse" id="moreDetails">
                    <table class="table table-dark" >
                      <thead>
                        <tr>
                          <th scope="col">Character</th>
                          <th scope="col">Percentage</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>{predictions[0][1]}</td>
                          <td>{predictions[0][0]}</td>
                        </tr>
                        <tr>
                          <td>{predictions[1][1]}</td>
                          <td>{predictions[1][0]}</td>
                        </tr>
                        <tr>
                          <td>{predictions[2][1]}</td>
                          <td>{predictions[2][0]}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              }
              {this.state.predictions &&
                <div className="col">
                  <p>
                    <button class="btn btn-primary" type="button" > Processed Image</button>
                  </p>
                  <img src={binary_image} alt="preprocessed" className="rounded mx-auto d-block" width='200'/>
                </div>
              }
            </div>
          </div>
        </div>
      </div >
    )
  }
}


export default App;
