import React, { Component } from 'react';
import './App.css';
import Navigation from './components/Navigation/Navigation';
import Board from './components/Board/Board'
import Utilities from './Utilities';

// Initialize some global constants

// Constants for chess games
const defaultBoardState = Utilities.defaultBoardState;
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
      board: defaultBoardState,
      // render: false // Set this value whenever you need to force a render()
    };

    this.game_data = {
      white_player: "",
      black_player: "",
      game_type: "",
      new_game: false,
      current_move: undefined
    };

    this.sessionID = ""
  }

  handleMove = (old_pos, new_pos) => {
    this.game_data.current_move = [old_pos, new_pos];
    
    let curBoard = this.state.board;
    let curPiece = curBoard[old_pos[0]][old_pos[1]];
    curBoard[old_pos[0]][old_pos[1]] = 0
    curBoard[new_pos[0]][new_pos[1]] = curPiece;
    this.setState({ board: curBoard });
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
    this.setState({ game_playing: true });
    // For some reason setting board to defaultBoardState does NOT work!! 
    this.setState({ board: [[-4, -2, -3, -5, -6, -3, -2, -4],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0], 
                            [ 0, 0, 0, 0, 0, 0, 0, 0], 
                            [ 1, 1, 1, 1, 1, 1, 1, 1], 
                            [ 4, 2, 3, 5, 6, 3, 2, 4]] })
    this.game_data.game_type =  game_type;
    this.game_data.new_game = true;

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
    console.log("Board state: ", this.state.board);
    let current_screen;
    if(this.state.current_screen === BOARD){
      if(this.game_data.white_player === BOT && this.game_data.black_player === BOT) {
        current_screen = <Board className={BOARD} board={this.state.board}/>;
      
      } else if(this.game_data.white_player === HUMAN && this.game_data.black_player === BOT) {
        console.log("White is a HUMAN and black is BOT");
        current_screen = <Board classname={BOARD} board={this.state.board} handleMove={this.handleMove} gamePlaying={this.state.game_playing} curPlayer={this.state.current_player}/>
      
      } else if(this.game_data.white_player === BOT && this.game_data.black_player === HUMAN) {
        current_screen = <Board classname={BOARD} board={this.state.board} handleMove={this.handleMove} gamePlaying={this.state.game_playing} curPlayer={this.state.current_player}/>
      
      } else if(this.game_data.white_player === HUMAN && this.game_data.black_player === HUMAN) {
        current_screen = <Board classname={BOARD} board={this.state.board} handleMove={this.handleMove} gamePlaying={this.state.game_playing} curPlayer={this.state.current_player}/>
      
      } else {
        current_screen = <Board className={BOARD} board={this.state.board} gamePlaying={this.state.game_playing} curPlayer={this.state.current_player}/>;
      }
    }
    return (
      <div className="App">
        <Navigation onPlayClick={this.onPlayClick} onStatsClick={this.onStatsClick} onSigninClick={this.onSigninClick}/>
        {current_screen}
      </div>
    );
  }

  componentDidUpdate() {
    let current_player = this.state.current_player;
    let white_player = this.game_data.white_player;
    let black_player = this.game_data.black_player;
    let game_type = this.game_data.game_type;
    let current_move = this.game_data.current_move;
    let new_game = this.game_data.new_game;

    if(this.state.game_playing) {
      switch (game_type) {
        case "twoRandomBots":
          fetch(`http://localhost:5000/playTwoRandomBots?new_game=${new_game}`,{
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
              if(this.game_data.new_game) {
                this.game_data.new_game = false;
              }
              this.setState({ board: data });
            }
          });
          break;
        case "oneBotOneHuman":
          if((current_player === WHITE && white_player === HUMAN) || (current_player === BLACK && black_player === HUMAN)) {
            if(current_move !== undefined) {
              console.log("New game state: ",new_game);
              fetch("http://localhost:5000/oneBotOneHuman",  {
                method: "POST",
                credentials: "include",
                body: JSON.stringify({"game_type": game_type, "move": current_move, "new_game": new_game }),
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
                  if(this.game_data.new_game) {
                    this.game_data.new_game = false;
                  }
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
