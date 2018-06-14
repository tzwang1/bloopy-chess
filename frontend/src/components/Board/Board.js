import React from 'react';
import './Board.css';
import DarkTile from './Tile/DarkTile';
import LightTile from './Tile/LightTile';

const Board = (props) => {
    // console.log("Board props", props);
    let board = props.board;
    // console.log(board);
    let board_component = [];
    for(let i = 0; i < 8; i++) {
        for(let j = 0; j < 8; j++) {
            if(i % 2 === 0) {
                if(j % 2 === 0) {
                    board_component.push(<DarkTile key={[i,j]} piece={board[i][j]} pos={[i,j]} handleMove={props.handleMove} gamePlaying={props.game_playing} currentPlayer={props.current_player}/>);
                } else {
                    board_component.push(<LightTile key={[i,j]} piece={board[i][j]} pos={[i,j]} handleMove={props.handleMove} gamePlaying={props.game_playing} currentPlayer={props.current_player}/>);
                }
            } else {
                if(j % 2 === 0){
                    board_component.push(<LightTile key={[i,j]} piece={board[i][j]} pos={[i,j]} handleMove={props.handleMove} gamePlaying={props.game_playing} currentPlayer={props.current_player}/>);
                } else {
                    board_component.push(<DarkTile key={[i,j]} piece={board[i][j]} pos={[i,j]} handleMove={props.handleMove} gamePlaying={props.game_playing} currentPlayer={props.current_player}/>);
                }
            }
        }
    }
    return(
        <div className="Board pa3"> 
            {board_component}
        </div>
    );
}

export default Board;