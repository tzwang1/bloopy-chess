import React from 'react';
import './Board.css';
import DarkTile from './Tile/DarkTile';
import LightTile from './Tile/LightTile';

class Board extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            playing: false,
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
    
    render() {
        let board = [];
        for(let i = 0; i < 8; i++) {
            for(let j = 0; j < 8; j++) {
                if(i % 2 === 0) {
                    if(j % 2 === 0) {
                        board.push(<DarkTile key={[i,j]} piece={this.state.board[i][j]}/>);
                    } else {
                        board.push(<LightTile key={[i,j]} piece={this.state.board[i][j]}/>);
                    }
                } else {
                    if(j % 2 === 0){
                        board.push(<LightTile key={[i,j]} piece={this.state.board[i][j]}/>);
                    } else {
                        board.push(<DarkTile key={[i,j]} piece={this.state.board[i][j]}/>);
                    }
                }
            }
        }
        return(
            <div className="Board pa3"> 
                {board}
            </div>
        );
    }
}

export default Board;