import mysql from 'mysql2';
import dotenv from 'dotenv';
import cors from 'cors';
import express from 'express';
import process from 'node:process';
// import {connection} from '.../SwiftSvings/Scraping/my_scrape/.env';
// Create a connection

dotenv.config({ path: '../Scraping/my_scrape/.env' });
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





// dotenv.config({path: '../Scraping/my_scrape/.env'})
// console.log(dotenv.config({path: '/Users/izzy/coding/chrome/SwiftSvings/Scraping/my_scrape/.env'}))
// const connection = mysql.createConnection({
//   host: 'localhost',
//   user: 'root',
//   password: process.env.DBpass,
//   database: 'mangafigure_scraping',
// });

// // Connect to the database
// connection.connect((err) => {
//   if (err) {
//     console.error('Error connecting to MySQL:', err);
//     return;
//   }
//   console.log('Connected to MySQL!');
// });

// // Perform a query
// connection.query('SELECT * FROM BNspidermanga_products', (err, results) => {
//   if (err) {
//     console.error('Error executing query:', err);
//     return;
//   }
//   console.log('Query results:', results);
// });

// // Close the connection
// connection.end();