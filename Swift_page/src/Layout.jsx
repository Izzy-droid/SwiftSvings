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
                
                
                  <a href="about.html" classame='links'>About</a>
                
                
                  <a href="FAQ.html" className='links'>FAQ</a>
                
                
                  <a href="contact.html" className='links'>Contact</a>
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