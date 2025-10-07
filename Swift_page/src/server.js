import mysql from 'mysql2';
import dotenv from 'dotenv';
import cors from 'cors';
import express from 'express';
import process from 'node:process';

dotenv.config({path: '../../../SwiftSvings/Scraping/my_scrape/.env'});

const app = express()
app.use(cors())

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: process.env.DBpass,
    database: 'mangafigure_scraping',
});
app.get('/', (req, res)=> {
  return res.json("from backend")
})
app.get('/users/BN', (req, res) => {
  const sql = "SELECT * FROM BNmanga_products";
  connection.query (sql, (err, data)=>{
    if(err) return res.json(err);
    return res.json(data);
  })
})
app.get('/users/GS', (req, res) => {
  const sql = "SELECT * FROM GoodSM_figure_products";
  connection.query (sql, (err, data)=>{
    if(err) return res.json(err);
    return res.json(data);
  })
})
app.get('/users/Ami', (req, res) => {
  const sql = "SELECT * FROM Ami_figure_products";
  connection.query (sql, (err, data)=>{
    if(err) return res.json(err);
    return res.json(data);
  })
})




app.listen(8801, () => {
  console.log('listening');
})



