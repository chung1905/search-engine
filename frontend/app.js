const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const request = require('request');
const path = require('path');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname + '/view'));
app.set('view engine', 'pug');

const corsOptions = {
    origin: 'http://localhost:3000',
    optionsSuccessStatus: 200
};

app.use(cors(corsOptions));

app.get('/result',(req,res)=>{
    const coreName = 'solr_first_core';
    const solrUrl = 'http://localhost:8983/solr/' + coreName + '/select?q=';

    const q = req.query.q;

    let searchObject = {
        "query": "content:" + q,
        "limit": 10,
    }

    request({
        uri: solrUrl,
        method: 'POST',
        json: searchObject,
    },function(error, response, body) {
        if (error || response.statusCode !== 200) {
            return;
        }
        console.log(body.response);
        res.render('result', {
            title: 'Query for: ' + q,
            count: body.response.numFound,
            docs: body.response.docs,
        });
    });
});

app.get('/',(req,res)=>{
    res.render('index', {
        title: 'Wiki search'
    });
});

app.listen(3000,()=>{
    console.log("app is running on port 3000")
});