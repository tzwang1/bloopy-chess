import React from 'react';
//import Piece from './Piece/Piece';
import './Board.css';
import DarkTile from './DarkTile';
import LightTile from './LightTile';

const Board = () => {
    let board = [];
    for(let i = 0; i < 8; i++) {
        for(let j = 0; j < 8; j++) {
            if(i % 2 === 0) {
                if(j % 2 === 0) {
                    board.push(<DarkTile/>);
                } else {
                    board.push(<LightTile/>);
                }
            } else {
                if(j % 2 === 0){
                    board.push(<LightTile/>);
                } else {
                    board.push(<DarkTile/>);
                }
            }
        }
    }
    return(
        <div className="Board"> 
            {board}
        </div>
    );
}

export default Board;