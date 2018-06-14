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
      current_player: WHITE,
      game_playing: false,
      board: Utilities.defaultBoardState,
      render: false // Set this value whenever you need to force a render()
    };

    this.game_data = {
      white_player: "",
      black_player: "",
      game_type: "",
      current_move: undefined
    };

    this.sessionID = ""
  }

  handleMove = (old_pos, new_pos) => {
    console.log(old_pos);
    console.log(new_pos);
    this.game_data.current_move = [old_pos, new_pos];
    this.setState({render: true});
  }

  onPlayClick = (game_type) => {
    switch(game_type) {
      case "twoRandomBots":
        this.game_data.black_player = BOT;
        this.game_data.white_player = BOT;
        break;

      case "oneBotOneHuman":
        this.game_data.black_player = BOT;
        this.game_data.white_player = HUMAN;
        break;

      default:
        break;
    }
    this.setState({ current_screen: BOARD });
    this.setState({ game_playing: true});
    this.setState({ board: Utilities.defaultBoardState })
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
    console.log(this.state.board);
    let current_screen;
    if(this.state.current_screen === BOARD){
      if(this.game_data.white_player === BOT && this.game_data.black_player === BOT) {
        current_screen = <Board className={BOARD} board={this.state.board}/>;
      } else if(this.game_data.white_player === HUMAN && this.game_data.black_player === BOT) {
        console.log("White is a HUMAN and black is BOT");
        current_screen = <Board classname={BOARD} board={this.state.board} handleMove={this.handleMove}/>
      } else if(this.game_data.white_player === BOT && this.game_data.black_player === HUMAN) {
        current_screen = <Board classname={BOARD} board={this.state.board} handleMove={this.handleMove}/>
      } else if(this.game_data.white_player === HUMAN && this.game_data.black_player === HUMAN) {
        current_screen = <Board classname={BOARD} board={this.state.board} handleMove={this.handleMove}/>
      } else {
        current_screen = <Board className={BOARD} board={this.state.board}/>;
      }
    }
    return (
      <div className="App">
        <Navigation onPlayClick={this.onPlayClick} onStatsClick={this.onStatsClick} onSigninClick={this.onSigninClick}/>
        {current_screen}
        <div className="f5">Icons made by <a href="https://www.flaticon.com/authors/ddara" title="dDara">dDara</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0">CC 3.0 BY</a></div>
      </div>
    );
  }

  componentDidUpdate() {
    let current_player = this.state.current_player;
    let {white_player, black_player, game_type, current_move} = this.game_data;
    console.log("Updating component");
    if(this.state.game_playing) {
      switch (game_type) {
        case "twoRandomBots":
          fetch("http://localhost:5000/playTwoRandomBots",{
            method: "GET",
            credentials: "include"
          })
          .then(Utilities.handleErrors)
          .then(response => response.json())
          .then(data => {
            // console.log("Data: ", data);
            if(data === "Game Over") {
              this.setState({ game_playing: false});
            } else {
              this.setState({ board: data });
            }
          });
          break;
        case "oneBotOneHuman":
          if((current_player === WHITE && white_player === HUMAN) || (current_player === BLACK && black_player === HUMAN)) {
            if(current_move !== undefined) {
              fetch("http://localhost:5000/oneBotOneHuman",  {
                method: "POST",
                credentials: "include",
                body: JSON.stringify({"game_type": game_type, "move": current_move}),
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
              this.game_data.current_move = undefined;
            }
          }
          break
        //TODO: Add more cases for (Bot vs Human), and (Human vs Human)
        default:

      }
    }
  }
}

export default App;
