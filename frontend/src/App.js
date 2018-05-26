import React, { Component } from 'react';
import './App.css';
import Navigation from './components/Navigation/Navigation';
import Board from './components/Board/Board'

class App extends Component {
  constructor() {
    super();
    this.state = {
      game_playing: false,
      game_type: "",
      current_screen: "board",
      board: [[-4, -2, -3, -5, -6, -3, -2, -4],
              [-1, -1, -1, -1, -1, -1, -1, -1],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ 1, 1, 1, 1, 1, 1, 1, 1], 
              [ 4, 2, 3, 5, 6, 3, 2, 4]]
    }
  }

  onPlayClick = (game_type) => {
    console.log("working");
    console.log(game_type);
    this.setState({ current_screen: "board" });
    this.setState({ game_playing: true});
    this.setState({ game_type: game_type});
  }

  onStatsClick = () => {
    this.setState({ current_screen: "stats" });
    this.setState({ game_playing: false});
    console.log("clicked stats tab");
  }

  onSigninClick = () => {
    this.setState({ current_screen: "signin" });
    this.setState({ game_playing: false });
    console.log("clicked signing tab");
  }

  render() {
    console.log("rendering!");
    let current_screen = <Board board={this.state.board}/>;
    // if(this.current_screen === "board"){
    //   let current_screen = <Board playing={this.state.game_playing}/>;
    // }
    return (
      <div className="App">
        <Navigation onPlayClick={this.onPlayClick} onStatsClick={this.onStatsClick} onSigninClick={this.onSigninClick}/>
        {current_screen}
        <div className="f5">Icons made by <a href="https://www.flaticon.com/authors/ddara" title="dDara">dDara</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0">CC 3.0 BY</a></div>
      </div>
    );
  }

  componentDidUpdate() {
    console.log(this.state.game_playing);
    if(this.state.game_playing) {
      switch (this.state.game_type) {
        case "Bot vs Bot (Random)":
          fetch('http://localhost:5000/twoRandomBots')
          .then(response => response.json())
          .then(data => {
            if(data === "Game Over") {
              this.setState({ game_playing: false});
            } else {
              this.setState({ board: data });
            }
          });
          break;
        default:

      }
    }
  }
}

export default App;
