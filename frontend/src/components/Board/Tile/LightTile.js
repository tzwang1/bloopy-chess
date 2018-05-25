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

const LightTile = (props) => {
    let piece;
    switch(props.piece) {
        case -1:
            piece = <BlackPawn />;
            break;
        case -2:
            piece = <BlackKnight />;
            break;
        case -3:
            piece = <BlackBishop />;
            break;
        case -4:
            piece = <BlackRook />;
            break;
        case -5:
            piece = <BlackQueen />;
            break;
        case -6:
            piece = <BlackKing />;
            break;
        case 1:
            piece = <WhitePawn />;
            break;
        case 2:
            piece = <WhiteKnight />;
            break;
        case 3:
            piece = <WhiteBishop />;
            break;
        case 4:
            piece = <WhiteRook />;
            break;
        case 5:
            piece = <WhiteQueen />;
            break;
        case 6:
            piece = <WhiteKing />;
            break;
        default:
    }
    return(
        <div className='LightTile'>
            {piece}
        </div>
    );   
}

export default LightTile