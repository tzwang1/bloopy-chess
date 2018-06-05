import React, { Component } from 'react';
import './App.css';
import Navigation from './components/Navigation/Navigation';
import Board from './components/Board/Board'
import Utilities from './Utilities';

// Initialize some global constants

// Constants for chess games
const BOT = "bot";
const HUMAN = "human";
const WHITE = "white";
const BLACK = "black"

// Constants for the type of screen to display
const BOARD = "board";
const SIGNIN = "signin";
const STATS = "stats";

class App extends Component {
  constructor() {
    super();
    this.state = {
      current_screen: BOARD,
      game_playing: false,
      board: [[-4, -2, -3, -5, -6, -3, -2, -4],
              [-1, -1, -1, -1, -1, -1, -1, -1],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ 1, 1, 1, 1, 1, 1, 1, 1], 
              [ 4, 2, 3, 5, 6, 3, 2, 4]]
    };

    this.game_data = {
      white_player: "",
      black_player: "",
      current_player: WHITE,
      game_type: "",
      current_move: undefined
    };

    this.sessionID = ""
  }

  onPlayClick = (game_type) => {
    console.log("working");
    console.log(game_type);
    switch(game_type) {
      case "twoRandomBots":
        this.game_data.black_player = BOT;
        this.game_data.white_player = BOT;
        fetch(`http://localhost:5000/startGame/?game_type=${game_type}`, {
          method: 'GET',
          credentials: 'include'
        })
        .then(Utilities.handleErrors)
        .then(response => response.json())
        .then(data => {
          this.setState({ board: data });
        })
        .catch(error => console.log(error))
        break;
      case "oneBotOneHuman":
        console.log("Starting a game between a Bot and a human");
        this.game_data.black_player = BOT;
        this.game_data.white_player = HUMAN;
        fetch(`http://localhost:5000/startGame/?game_type=${game_type}`,{
          method: 'GET',
          credentials: 'include'
        })
        .then(Utilities.handleErrors)
        break;
      default:
        break;
    }
    this.setState({ current_screen: BOARD });
    this.setState({ game_playing: true});
    this.game_data.game_type =  game_type;
  }

  onStatsClick = () => {
    this.setState({ current_screen: STATS });
    this.setState({ game_playing: false});
    console.log("clicked stats tab");
  }

  onSigninClick = () => {
    this.setState({ current_screen: SIGNIN });
    this.setState({ game_playing: false });
    console.log("clicked signing tab");
  }

  render() {
    console.log("rendering!");
    console.log(this.state.game_playing);
    let current_screen = <Board className={BOARD} board={this.state.board}/>;
    // if(this.current_screen === BOARD){
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
    console.log("Updating component");
    if(this.state.game_playing) {
      switch (this.game_data.game_type) {
        case "twoRandomBots":
          fetch("http://localhost:5000/playTwoRandomBots",{
            method: "GET",
            credentials: "include"
          })
          .then(Utilities.handleErrors)
          .then(response => response.json())
          .then(data => {
            console.log("Data: ", data);
            if(data === "Game Over") {
              this.setState({ game_playing: false});
            } else {
              this.setState({ board: data });
            }
          });
          break;
        case "oneBotOneHuman":
          let {white_player, black_player, current_player, game_type, current_move} = this.game_data;
          if(current_player === WHITE && white_player === HUMAN)
            fetch("http://localhost:5000/oneBotOneHuman",  {
              method: "POST",
              credentials: "include",
              body: JSON.stringify({"move": {"old_pos": [1,1], "new_pos": [2,2] }}),
              headers:{
                'Content-Type': 'application/json'
              }
            })
            .then(Utilities.handleErrors)
            .then(response =>  response.json())
            .then(data => {
              console.log("Data: ", data);
              if(data === "Game Over") {
                this.setState({ game_playing: false});
              } else {
                this.setState({ board: data });
              }
            });
          break
        //TODO: Add more cases for (Bot vs Human), and (Human vs Human)
        default:

      }
    }
  }
}

export default App;
