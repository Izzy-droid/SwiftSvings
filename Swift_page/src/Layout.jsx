import React from 'react';
import { Outlet, Link } from 'react-router-dom';
function Layout(){
return(
    <>
    
        <div className="navbar">
          
            <div className="elements-container">
                <div className="inner-container">

                
               {/* Added the missing <ul> opening tag */}
                
                  <img src="./images/Slime_0.png" alt="logo" className="logo" />
                
                  <h1 className="ST">Swift Savings</h1>
                <div className="links-homepg">

                
                  <Link to='/' className='links'>Home</Link>
                
                
                  <Link to="./about.jsx" classame='links'>About</Link>
                
                
                  <Link to="./FAQ.jsx" className='links'>FAQ</Link>
                
                
                  <Link to="./contact.jsx" className='links'>Contact</Link>
                </div>
               {/* This closing tag now matches the opening <ul> */}
            
                
                   
              
            </div>
         </div>
          
        </div>
      
      
     
      <Outlet/>
    </>
);
}
export default Layout;