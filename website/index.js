const path = require ('path');
const express = require('express');

const app = express();

app.use('', express.static(path.join(__dirname, 'public')));

//home page (index.html)
app.get('/', (request,response)=>{
  return response.sendFile('index.html', { root: '.' });
});
//documentation page
app.get('/documentation', (request, response)=>{
  return response.sendFile('documentation.html', { root: '.' })
});
//contact page
app.get('/contact', (request, response)=>{
  return response.sendFile('contact.html', { root: '.' })
});

//about page
app.get('/about', (request, response)=>{
  return response.sendFile('about.html', { root: '.' })
});
//dashboard page
app.get('/auth/discord', (request, response)=>{
  return response.sendFile('dashboard.html', { root: '.' })
});
//invite page
app.get('/invite', (request, response)=>{
  return response.sendFile('invite.html', { root: '.' })
});


const port = "3000";
app.listen(port, () => console.log('App listening at http://localhost:3000'));