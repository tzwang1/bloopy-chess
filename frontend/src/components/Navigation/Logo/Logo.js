import React from 'react';
import logo from './Logo.png';
import './Logo.css';

const Logo = () => {
    return(
        <div className='Logo mr5 pt2'>
            <img alt='logo' src={logo}/>
        </div>
    );
}

export default Logo;