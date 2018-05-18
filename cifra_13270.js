const cheerio = require('cheerio');                     // Modulo que implementa o core do JQuery, usado para fazer as segmentacoes necessarias na pagina em HTML
const jsonframe = require('jsonframe-cheerio');
const request = require('request');
const fs = require('fs');
const got = require('got');
var json = { title : ""};
var pagesToVisit = [];
var frame;
var song;
var teste = 'https://www.cifraclub.com.br/letra/B/lista.html';
var relativeLinks = { "Links" : []};
var weber = [];
var songNum = 0;

function navigate(website){
    request(website, function(error, response, body) {
        if(error) {
        }
        try {
            if(response.statusCode == 200) {
                var $ = cheerio.load(body);
            }
        } catch (err) {
        }
        return collectfirstInternalLinks($);
    });
    return 1;
}

function navigateBands(website, num){
    if(website !== undefined){
        request(website, function(error, response, body) {
            if(error) {
            }
        
            try {
                if(response.statusCode == 200) {
                    var $ = cheerio.load(body);
                    console.log("Page title: " + $('title').text() + num , songNum++);
                }
            } catch (err) {
            }
            return collectsecondtInternalLinks($);
        });
    }

    return 1;
}

function collectfirstInternalLinks($){

    jsonframe($);
    
    let links = {
        "Links": ['a @ href']
    }

    relativeLinks = $('ul').scrape(links);
    return relativeLinks.Links;

}

function collectsecondtInternalLinks($){

    jsonframe($);
    
    let links = {
        "Links": ['.art_music-link @ href']
    }

    if ($('body') !== undefined){
        relativeLinks = $('body').scrape(links);
        for(var i = 0; i < relativeLinks.Links.length; i++){
            scrapChords('https://www.cifraclub.com.br' + relativeLinks.Links[i], relativeLinks.Links[i]);
        }

        return relativeLinks.Links;
    }

}

async function scrapChords(website, title) {
    const url = website;
    const html = await got(url);
    const $ = cheerio.load(html.body);
    var chords = new Array();

    jsonframe($); // initializing the plugin
    
    frame = {
        "Songname": "h1.t1",
        "Genre": "[itemprop=title]",
        "Chords": ["pre b"]
    }

    song = $('body').scrape(frame);

    var name = (title + '.json').replace('/', replaceValue = '');
    var fileTitle = (name.replace('/', replaceValue = '')).replace('/', '');

    if (!fileTitle.includes('letra')){
        fs.writeFile(fileTitle.replace('/',''), JSON.stringify(song, null), function(err){
        })
    }

}

async function crawl() {
    
    navigate(teste);
    setTimeout(function timeout(){
        asyncForEach(relativeLinks.Links);
    }, 10000)

}

async function asyncForEach(array){
    for(var i = 13270    ; i < 13280     ; i++){
        weber[i] = 'https://www.cifraclub.com.br' + relativeLinks.Links[i];
        try {
            navigateBands(weber[i], i);
        } catch (err) {
        }
    }
}

crawl();