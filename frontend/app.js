"use strict";
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const request = require('request');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname + '/view'));
app.set('view engine', 'pug');

const corsOptions = {
    origin: 'http://localhost:3000',
    optionsSuccessStatus: 200
};

app.use(cors(corsOptions));

app.get('/result', (req, res) => {
    const coreName = 'solr_first_core';
    let solrUrl = 'http://localhost:8983/solr/' + coreName + '/select?';

    const q = req.query.q;
    console.log(req.query);

    // Search in content field
    solrUrl += "q=content:" + q;

    // Highlighting result
    solrUrl += "&hl=on";
    solrUrl += "&hl.fl=content";
    solrUrl += "&hl.requireFieldMatch=true";
    solrUrl += "&hl.simple.pre=<b>";
    solrUrl += "&hl.simple.post=</b>";
    solrUrl += "&hl.fragsize=500";

    // Pagination
    const results_per_page = 20;
    const p = parseInt(req.query.p) ? parseInt(req.query.p) : 0;
    solrUrl += "&start=" + (p * results_per_page);
    solrUrl += "&rows=" + results_per_page; // results per page
    let nextPageUrl, prevPageUrl;

    if (/[?&]p=\d*/.test(req.url)) {
        nextPageUrl = req.url.replace(/([?&])p=\d*/, '$1p=' + (p + 1));
        if (p > 0) {
            prevPageUrl = req.url.replace(/([?&])p=\d*/, '$1p=' + (p - 1));
        }
    } else {
        nextPageUrl = req.url + '&p=' + (p + 1);k
    }

    request({
        uri: encodeURI(solrUrl),
        method: 'GET',
    }, function (error, response, body) {
        if (error || response.statusCode !== 200) {
            return renderNotFound(res, q);
        }
        let jsonBody = JSON.parse(body);
        jsonBody.response.docs.forEach(function (value, index) {
            let hlContent = jsonBody.highlighting[jsonBody.response.docs[index].id].content;
            if (hlContent !== undefined && hlContent.length > 0) {
                jsonBody.response.docs[index].highlight = hlContent[0];
            } else {
                if (/^\s+$/.test(value.overview)) {
                    delete jsonBody.response.docs[index];
                } else {
                    jsonBody.response.docs[index].highlight = value.overview;
                }
            }
        });
        if (jsonBody.response.numFound > 0) {
            const maxPage = jsonBody.response.numFound / results_per_page;
            if (p + 1 > maxPage) {
                nextPageUrl = false;
            }
            res.render('result', {
                query: q,
                title: 'Query for: ' + q,
                count: jsonBody.response.numFound,
                docs: jsonBody.response.docs,
                nextPageUrl,
                prevPageUrl,
            });
        } else {
            renderNotFound(res, q);
        }
    });
});

function renderNotFound(res, q) {
    res.render('result', {
        query: q,
        title: 'Query for: ' + q,
        count: 0,
        docs: [{
            url: [],
            title: ["No '" + q + "' found in any documents."],
            overview: [],
            content: []
        }],
    });
}

app.get('/', (req, res) => {
    res.render('index', {
        title: 'Wiki search'
    });
});

app.listen(3000, () => {
    console.log("app is running on port 3000")
});
