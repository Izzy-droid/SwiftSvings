import { useState, useEffect } from 'react';
import './App.css';
import Layout from './Layout';
import {Link, Routes, Route} from 'react-router-dom';
//import Sidebar from "./Sidebar";

//TODO:
// do ebay? 
//run server forever
//pagination: (https://www.freecodecamp.org/news/build-a-custom-pagination-component-in-react/)
//dockerize



//FOR LATER:
//also fix the add icon idk why they're so reactive with one another
//set up mangaspider on a later date
//schedule scraper and 
//set up azmspider
//set up a dropdown for manga/figure filters
//future filters by website

function App() {
  const [BNdata, setBNData] = useState([]);
  const [GSdata, setGSData] = useState([]);
  const [Amidata, setAmiData] = useState([]);
  const [input, setInput] = useState('');
  const [filteredData, setFilteredData] = useState([]);
  const [ogData, setogData] = useState([]);
  
    useEffect(() => {
      Promise.all([
        fetch('http://localhost:8801/users/BN').then((res) => res.json()),
        fetch('http://localhost:8801/users/GS').then((res) => res.json()),
        fetch('http://localhost:8801/users/Ami').then((res) => res.json())
      ])
      .then(([BNdata, GSdata, Amidata]) => {
        console.log('BNdata:', BNdata); 
        console.log('GSdata:', GSdata);
        console.log('Amidata:', Amidata);
          
      GSdata.forEach((item) => {
        item.price = parseFloat(item.price.replace(/[^\d.]/g, '')).toFixed(2) || 0;
        item.title = item.title.replace(/\t/g, "").trim(); 
      });
      BNdata.forEach((item) => {
        item.price = parseFloat(item.price.replace(/[^\d.]/g, '')).toFixed(2) || 0; 
      });
     
      Amidata.forEach((item) => {
        item.price = parseFloat(item.price.replace(/[^\d.]/g,  '')).toFixed(2) || 0; 
      });
        setBNData(BNdata);
        setGSData(GSdata);
        setAmiData(Amidata);
        const all_data = [...BNdata, ... GSdata, ...Amidata]
        console.log('Combined Data (all_data):', all_data); // Check combined data
      setogData(all_data);
      setFilteredData(all_data); // Initialize filteredData
      console.log('Filtered Data after initialization:', all_data);
      
      })
      
      .catch(err => console.log(err));
     
      
    
    }, [])

   
    

    function filterZ_A(){
      const Z_A_data = [...ogData].sort((a, b) => b.title.localeCompare(a.title));
      setFilteredData(Z_A_data);
     
      

    }
    function filterA_Z(){
    
      const A_Z_data = [...ogData].sort((a, b) => a.title.toLowerCase().localeCompare(b.title.toLowerCase())) ;
      setFilteredData(A_Z_data);
    } 

    function filterPrice_L_H(){
     
      
      const done_data = [...ogData].sort((a, b) => parseFloat(a.price) -parseFloat(b.price)) ;
      setFilteredData(done_data);
      
     
    }  
    function filterPrice_H_L(){
      const done_data = [...ogData].sort((a, b) => parseFloat(b.price) -parseFloat(a.price)) ;
      setFilteredData(done_data);
      

    } 

    function isFigure(){
      if (isFigure){
        const filtered_figure = ogData.filter((item) => !BNdata.includes(item));
        setFilteredData(filtered_figure)
      }
      else{
        setFilteredData(ogData);
      }
    }
    function isBook(){

      if (isBook){
        const filtered_book = ogData.filter((item) => BNdata.includes(item));
        setFilteredData(filtered_book);
        
      }
      else{
        setFilteredData(ogData);
      }
    }
    
  useEffect(() =>{
    if (!input.trim()){
      setFilteredData(ogData)
    }
    else{
      const filtered_search = [...ogData].filter(item => 
      item.title.toLowerCase().startsWith(input.toLowerCase())); 
      setFilteredData(filtered_search); 
      
    }
  },
[input, ogData, setFilteredData],)
    
  

  
  return (
  <>
    <Routes>
      <Route path="/" element={<Layout />} />

        {/* <Route path ="/About" element={<Abput/>}/> */}
        {/* <Route path = "/FAQ" element = { <FAQ/>}/> */}
         {/* <Route path = "/contact" element = { <contact/>}/> */}
      
        
     
    </Routes>
  <div className='main-container'>

    
    <div className='filter-container'>
      <div className='inner-filter'>
       
        <div id="items-container">
            <div >
              
                <form>
                  <input type="text" className="Search-box" placeholder="Search.."  onChange={(e) => setInput(e.target.value)} value={input}/>
                  <p>Sort by..</p>
                  <div className='filter-container'>
                    <div className='inner-form'>

                    
                    <input type="radio" id="A_Zname" name="name" value="name" onClick={filterA_Z} className='radio-sort'/>
                    <label htmlFor="name" className='check'> name (A-Z)</label>
                    <input type="radio" id="Z_Aname" name="name" value="name"  onClick={filterZ_A} className='radio-sort'/>
                    <label htmlFor="name" > name (Z-A)</label>
                    
                    
                    <br/>
                    
                     
                        <input type="radio" id="priceL_H" name="name" value="name" onClick={filterPrice_L_H} className='radio-sort'/>
                        <label htmlFor="name" > price (lowest to highest)</label>
                      
                     
                      <input type="radio" id="priceH_L" name="name" value="name" onClick={filterPrice_H_L} className='radio-sort'/>
                      <label htmlFor="name" > price (highest to lowest)</label> 
                    
                   
                   
                     <br/>
                     <p>Filter by..</p>
                      <input type="radio" id="priceL_H" name="name" value="name" onClick={isBook} className='radio-sort'/>
                      <label htmlFor="name"> Manga </label>
                      <input type="radio" id="priceH_L" name="name" value="isFigure" onClick={isFigure} className='radio-sort'/>
                      <label htmlFor="isFigure" > Figures</label> 
                      
                      
                    
                   
                      

                    </div>
                    
                  

                  </div>
                  

                 
                </form>

                
              </div>
          </div>
      </div>
      
    </div>

    <div className='table-container'>
      <div className="inner-tablebox">
        <table>
            <thead>
               

            </thead>
            <tbody >
                {filteredData.map((item, index ) => (
                    <tr key={index}>
                       
                       <td><img src={item.book_img || item.figure_img}/></td>
                        <td><div className='title-container'><a href={item.book_url || item.figure_url}>{item.title}</a></div></td>
                        <td><div className='author-container'>{item.author || item.brand}</div></td>
                        <td><div className='price-container'>${item.price}</div></td>
                        <td><div className='desc-container truncate-overflow'>{item.descript ||  "No description given."}</div></td>
                        <td><div className='type-container'>{item.book_type}</div></td>
                        {/* <td><img src='./add.png' className='add-icon'/></td> */}
                        
                    </tr>
                ))}
               
                          
                        
                 
            </tbody>

        </table>
      </div>
    </div>
  </div>
  </>   
  );
}

export default App;