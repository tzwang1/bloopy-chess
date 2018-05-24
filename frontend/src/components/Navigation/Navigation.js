import React from 'react';
import './Navigation.css';
import Logo from './Logo/Logo'

const Navigation = () => {
    return(
        <nav className='nav_bar'>
            <Logo />
            <p className='f3 link dim black underline pa3 pointer'>Play </p>
            <p className='f3 link dim black underline pa3 pointer'> Stats </p>
            <p className='f3 link dim black underline pa3 pointer'> Sign Up </p>
        </nav>
    );
}

export default Navigation;