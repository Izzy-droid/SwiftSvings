import { useState, useEffect } from 'react';
import './App.css';
import Layout from './Layout';
import { Outlet } from 'react-router-dom';

function Infotable() {
    const [data, setData] = useState([]);
    useEffect(() => {
      fetch('http://localhost:8801/users/BN')
      .then((res) => res.json())
      .then(data => setData(data))
      .catch(err => console.log(err));
    }, [])


  return (
    <>
    <Outlet/>
    <div>
        <table>
            <thead>
               

            </thead>
            <tbody>
                {data.map((data ) => (
                    <tr>
                        <td>{data.id}</td>
                        <td>{data.title}</td>
                        <td>{data.author}</td>
                        <td>{data.price}</td>
                        <td>{data.book_img}</td>
                    </tr>
                ))}
            </tbody>

        </table>
    </div>
   </>   
  );
}

export default Infotable;