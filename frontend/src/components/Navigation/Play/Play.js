import React from 'react';
import './Play.css';

const Play = () => {
    return(
        <div className='dropdown'>
            <p className='f3 link dim black underline pb0 mr5 mt4 pointer'>Play </p>
            <div className="dropdown-content">
                <a href="/twoBotsRandom">Bot vs Bot (Random)</a>
                <a href="/oneHumanOneBot">Bot vs Human</a>
                <a href="/twoHumans">Human vs Human</a>
            </div>
        </div>
    );
}

export default Play;