import React from 'react';

const Navigation = () => {
    return(
        <nav style={{display: 'flex', justifyContent: 'center'}}>
            <p className='f3 link dim black underline pa3 pointer'>Play </p>
            <p className='f3 link dim black underline pa3 pointer'> Stats </p>
            <p className='f3 link dim black underline pa3 pointer'> Sign Up </p>
        </nav>
    );
}

export default Navigation;