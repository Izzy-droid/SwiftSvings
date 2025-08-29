import { useState, useEffect } from 'react';
import './App.css';
import Layout from './Layout';
import {Link, Routes, Route} from 'react-router-dom';
import Infotable from './Infotable';
//import Sidebar from "./Sidebar";
function App() {
  const [data, setData] = useState([]);
    useEffect(() => {
      fetch('http://localhost:8801/users/BN')
      .then((res) => res.json())
      .then(data => setData(data))
      .catch(err => console.log(err));

      fetch('http://localhost:8801/users/GS')
      .then((res) => res.json())
      .then((data) => console.log(data))
      .catch((err) => console.error(err));

      fetch('http://localhost:8801/users/Ami')
      .then((res) => res.json())
      .then((data) => console.log(data))
      .catch((err) => console.error(err));
    }, [])
  return (
    <>
    <Routes>
      <Route path="/" element={<Layout />} />

        <Route path ="/Infotable" element={<Infotable/>}/>
        {/* <Route path = "/Sidebar" element = { <Sidebar/>}/> */}

      
        
     
    </Routes>
    <div class='filter-container'>

    </div>
    <div className='table-container'>
      <div className="test-run">
        <table>
            <thead>
               

            </thead>
            <tbody >
                {data.map((data ) => (
                    <tr key={data.id}>
                       
                       <td><img src={data.book_img || null}/></td>
                        <td ><a href={data.book_url}>{data.title}</a></td>
                        <td>{data.author}</td>
                        <td>{data.price}</td>
                          
                        
                    </tr>
                ))}
            </tbody>

        </table>
      </div>
    </div>
   </>   
  );
}

export default App;