import React from 'react';
import './Play.css';

const Play = ({onPlayClick}) => {
    return(
        <div className='dropdown'>
            <p className='f3 link dim black underline pb0 mr3 ml3 mt4 pointer'>Play </p>
            <div className="dropdown-content">
                <p onClick={()=> onPlayClick("twoRandomBots")}>Bot vs Bot (Random)</p>
                <p onClick={()=> onPlayClick("oneBotOneHuman")}>Bot vs Human</p>
                <p onClick={()=> onPlayClick("twoHumans")}>Human vs Human</p>
            </div>
        </div>
    );
}

export default Play;