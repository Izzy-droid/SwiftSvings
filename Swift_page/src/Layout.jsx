import react from 'react'

function Layout(){
return(
    <>
    
        <div className="navbar">
          
            <div className="elements-container">
                <div className="inner-container">

                
               {/* Added the missing <ul> opening tag */}
                
                  <img src="/Slime_0.png" alt="logo" className="logo" />
                
                  <h1 className="ST">Swift Savings</h1>
                  <a href="index.html">Home</a>
                
                
                  <a href="about.html">About</a>
                
                
                  <a href="FAQ.html">FAQ</a>
                
                
                  <a href="contact.html">Contact</a>
                
               {/* This closing tag now matches the opening <ul> */}
            
                <div className="form-btn-container">
                    <div className="search-arrange">
                    <form>
                        <input type="text" className="Search-box" placeholder="Search.." />
                    </form>  
                    </div>
                   
                    <a href="login.html" className="Log-in">
                    Login
                    </a>
                </div>
            </div>
         </div>
          
        </div>
      
      <div>
        <h2>Please select the stores you're interested in</h2>
        <div className="storeSearch active"></div>
      </div>
    </>
);
}
export default Layout;