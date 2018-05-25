import React from 'react';
import './Play.css';

const Play = () => {
    return(
        <div className='dropdown'>
            <p className='f3 link dim black underline pb0 mr5 mt4 pointer'>Play </p>
            <div className="dropdown-content">
                <p>Bot vs Bot (Random)</p>
                <p>Bot vs Human</p>
                <p>Human vs Human</p>
            </div>
        </div>
    );
}

export default Play;