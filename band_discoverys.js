const cheerio = require('cheerio');                     // Modulo que implementa o core do JQuery, usado para fazer as segmentacoes necessarias na pagina em HTML
const jsonframe = require('jsonframe-cheerio');
const request = require('request');
const fs = require('fs');
const got = require('got');
var json = { title : ""};
var pagesToVisit = [];
var frame;
var song;
var relativeLinks = { "Links" : []};
var secondRelativeLinks = { "Links" : []};
var weber = [];
var songNum = 0;

function navigate(website, element, b){
    request(website, function(error, response, body) {
        if(error) {
            //console.log("Error: " + error);
        }
    
        try {
            if(response.statusCode == 200) {
                var $ = cheerio.load(body);
            }
        } catch (err) {
        }
        return collectfirstInternalLinks($, element, b);
    });

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

function collectfirstInternalLinks($, element, b){

    jsonframe($);
    
    let links = {
        "Links": ['a @ href']
    }

    relativeLinks = $('ul').scrape(links)
    b.set(element, relativeLinks.Links.length)
    console.log(relativeLinks.Links.length, element, b) //console.log("Found " + relativeLinks.Links.length + " relative links");

    return relativeLinks.Links;

}

function collectsecondtInternalLinks($){

    jsonframe($);
    
    let links = {
        "Links": ['.art_music-link @ href']
    }

    if ($('body') !== undefined){
        secondRelativeLinks = $('body').scrape(links);
        for(var i = 0; i < secondRelativeLinks.Links.length; i++){
            scrapChords('https://www.cifraclub.com.br' + secondRelativeLinks.Links[i], secondRelativeLinks.Links[i]);
        }

        return secondRelativeLinks.Links;
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

function genCharArray(charA, charZ) {
    var a = [], i = charA.charCodeAt(0), j = charZ.charCodeAt(0);
    for (; i <= j; ++i) {
        a.push(String.fromCharCode(i));
    }
    return a;
}

a = genCharArray('B', 'Z')
<<<<<<< HEAD
console.log(a)
var myMap = new Map()
a.forEach((element) => {
    navigate('https://www.cifraclub.com.br/letra/'+element+'/lista.html', element, myMap)
    for (var i = 0; i < myMap.get(element); i++) {
        weber[i] = 'https://www.cifraclub.com.br' + relativeLinks.Links[i];
        try {
            navigateBands(weber[i], i);
        } catch (err) {
        }
    }
})
=======
var myMap = new Map()
c = new Promise(function(resolve, reject){
    resolve(a.forEach((element) => {
        d = new Promisse((resolve, reject) => {
            resolve(navigate('https://www.cifraclub.com.br/letra/'+element+'/lista.html', element, myMap))
        })
        d.then(() => {
            for (var i = 0; i < myMap.get(element); i++) {
                weber[i] = 'https://www.cifraclub.com.br' + relativeLinks.Links[i];
                try {
                    navigateBands(weber[i], i);
                } catch (err) {
                }
            }
        })
    }))
})

c.then(() => {
    console.log(myMap)
});
>>>>>>> e46d035c59e88b38723080e602859a34de21c32b
