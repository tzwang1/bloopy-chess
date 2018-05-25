import React from 'react';
import './Navigation.css';
import Logo from './Logo/Logo';
import Play from './Play/Play';

const Navigation = () => {
    return(
        <nav className='nav_bar'>
            <Logo />
            <Play />
            <p className='f3 link dim black underline pb0 mb0 mr5 mt4 pointer'> Stats </p>
            <p className='f3 link dim black underline pb0 mb0 mr5 mt4 pointer'> Sign Up </p>
        </nav>
    );
}

export default Navigation;