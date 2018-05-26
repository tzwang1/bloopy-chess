import React from 'react';
import './Play.css';

const Play = ({onPlayClick}) => {
    return(
        <div className='dropdown'>
            <p className='f3 link dim black underline pb0 mr5 mt4 pointer'>Play </p>
            <div className="dropdown-content">
                <p onClick={()=> onPlayClick("Bot vs Bot (Random)")}>Bot vs Bot (Random)</p>
                <p onClick={()=> onPlayClick("Bot vs Human")}>Bot vs Human</p>
                <p onClick={()=> onPlayClick("Human vs Human")}>Human vs Human</p>
            </div>
        </div>
    );
}

export default Play;