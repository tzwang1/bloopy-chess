import React from 'react';
import './Tile.css';
import BlackPawn from '../Pieces/BlackPawn';
import BlackKnight from '../Pieces/BlackKnight';
import BlackBishop from '../Pieces/BlackBishop';
import BlackRook from '../Pieces/BlackRook';
import BlackQueen from '../Pieces/BlackQueen';
import BlackKing from '../Pieces/BlackKing';

import WhitePawn from '../Pieces/WhitePawn';
import WhiteKnight from '../Pieces/WhiteKnight';
import WhiteBishop from '../Pieces/WhiteBishop';
import WhiteRook from '../Pieces/WhiteRook';
import WhiteQueen from '../Pieces/WhiteQueen';
import WhiteKing from '../Pieces/WhiteKing';

import TileSize from './TileSize';

const DarkTile = (props) => {
    let piece;
    switch(props.piece) {
        case -1:
            piece = <BlackPawn pos={props.pos} tileSize={TileSize}/>;
            break;
        case -2:
            piece = <BlackKnight pos={props.pos} tileSize={TileSize}/>;
            break;
        case -3:
            piece = <BlackBishop pos={props.pos} tileSize={TileSize}/>;
            break;
        case -4:
            piece = <BlackRook pos={props.pos} tileSize={TileSize}/>;
            break;
        case -5:
            piece = <BlackQueen pos={props.pos} tileSize={TileSize}/>;
            break;
        case -6:
            piece = <BlackKing pos={props.pos} tileSize={TileSize}/>;
            break;
        case 1:
            piece = <WhitePawn pos={props.pos} tileSize={TileSize}/>;
            break;
        case 2:
            piece = <WhiteKnight pos={props.pos} tileSize={TileSize}/>;
            break;
        case 3:
            piece = <WhiteBishop pos={props.pos} tileSize={TileSize}/>;
            break;
        case 4:
            piece = <WhiteRook pos={props.pos} tileSize={TileSize}/>;
            break;
        case 5:
            piece = <WhiteQueen pos={props.pos} tileSize={TileSize}/>;
            break;
        case 6:
            piece = <WhiteKing pos={props.pos} tileSize={TileSize}/>;
            break;
        default:
    }
    // console.log("Rendering DarkTile");
    return(
        <div className='DarkTile'>
                {piece}
        </div>
    );
}

export default DarkTile