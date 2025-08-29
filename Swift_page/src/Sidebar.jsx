import { useState, useEffect } from 'react';
import './App.css';
import Layout from './Layout';

function Sidebar() {
    useEffect(() => {
      fetch('http://localhost:8801/users/BN')
      .then((res) => res.json())
      .then(data => console.log(data))
      .catch(err => console.log(err));
    }, [])

    
  return (
    <>
    
   </>   
  );
}

export default Sidebar;