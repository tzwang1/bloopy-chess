import React from 'react';
import logo from './Logo.png';
import './Logo.css';

const Logo = () => {
    return(
        <div className='Logo mr4'>
            <img className='pa3' alt='logo' src={logo}/>
        </div>
    );
}

export default Logo;