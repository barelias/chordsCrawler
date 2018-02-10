const cheerio = require('cheerio');                     // Modulo que implementa o core do JQuery, usado para fazer as segmentacoes necessarias na pagina em HTML
const jsonframe = require('jsonframe-cheerio');
const request = require('request');
const fs = require('fs');
const got = require('got');
var json = { title : ""};
var pagesToVisit = [];
var frame;
var song;
var teste = 'https://www.cifraclub.com.br/letra/A/lista.html';
var relativeLinks = { "Links" : []};
var weber = [];
var songNum = 0;

function navigate(website){
    request(website, function(error, response, body) {
        if(error) {
            //console.log("Error: " + error);
        }
    
        try {
            //console.log("Status code: " + response.statusCode);
            if(response.statusCode == 200) {
                var $ = cheerio.load(body);
                //console.log("Page title: " + $('title').text());
            }
        } catch (err) {
            //console.log("Error: "+ err);
        }
        return collectfirstInternalLinks($);
    });

    return 1;
}

function navigateBands(website, num){
    if(website !== undefined){
        request(website, function(error, response, body) {
            if(error) {
                //console.log("Error: " + error);
            }
        
            try {
                //console.log("Status code: " + response.statusCode);
                if(response.statusCode == 200) {
                    var $ = cheerio.load(body);
                    console.log("Page title: " + $('title').text() + num , songNum++);
                }
            } catch (err) {
                //console.log("Error: "+ err);
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
    ////console.log(relativeLinks.Links);

    //console.log("Found " + relativeLinks.Links.length + " relative links");

    return relativeLinks.Links;

}

function collectsecondtInternalLinks($){

    jsonframe($);
    
    let links = {
        "Links": ['.art_music-link @ href']
    }

    if ($('body') !== undefined){
        relativeLinks = $('body').scrape(links);
        ////console.log(relativeLinks.Links);

        //console.log("Found " + relativeLinks.Links.length + " relative links");
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

    //console.log(song);

    var name = (title + '.json').replace('/', replaceValue = '');
    var fileTitle = (name.replace('/', replaceValue = '')).replace('/', '');

    //console.log(fileTitle);

    if (!fileTitle.includes('letra')){
        fs.writeFile(fileTitle.replace('/',''), JSON.stringify(song, null), function(err){
            //console.log('File successfully written! - Check your project directory for the ' + fileTitle.replace('/', replaceValue = '') + ' file');
        })
    }

}

async function crawl() {
    
    navigate(teste);
    setTimeout(function timeout(){
        //console.log(relativeLinks.Links);
        asyncForEach(relativeLinks.Links);
    }, 10000)

    /*firstSetLinks.forEach(function(value, index, ar) {

        var weber = 'https://www.cifraclub.com.br' + value;
        //console.log(weber);
        var secondeSetLinks = ['0', '1', '2'];
        secondSetLinks = navigate(weber);

    });*/
        

}

async function asyncForEach(array){
    for(var i = Z     ; i < Z     ; i++){
        weber[i] = 'https://www.cifraclub.com.br' + relativeLinks.Links[i];
        //console.log(weber[i]);
        try {
            navigateBands(weber[i], i);
        } catch (err) {
            //console.log(err);
        }
        //console.log(i);
    }
    /*array.forEach(function(value){
        setTimeout(function(){
            var weber = 'https://www.cifraclub.com.br' + value;
            //console.log(weber);
            navigate(weber);
        }, 0);
    })*/
}

//scrapChords(extreme);
crawl();
