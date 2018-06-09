import React from 'react';
import './Navigation.css';
import Logo from './Logo/Logo';
import Play from './Play/Play';

const Navigation = ({ onPlayClick, onStatsClick, onSigninClick }) => {
    return(
        <nav className='nav_bar'>
            <Play onPlayClick={onPlayClick}/>
            <p onClick={onStatsClick} className='f3 link dim black underline pb0 mb0 mr3 ml3 mt4 pointer'> Stats </p>
            <p onClick={onSigninClick} className='f3 link dim black underline pb0 mb0 mr3 ml3 mt4 pointer'> Sign Up </p>
            <Logo />
        </nav>
    );
}

export default Navigation;