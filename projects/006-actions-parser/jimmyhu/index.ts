const express: Function = require('express')
const fs = require('fs')
const axios = require('axios')


// interfaces and type declarations
export interface story {
    "actions": action[]
}

export interface IRegx {
    "raw": string
    "filtered": string
}

export interface Inames<Tvalue> {
    [id: string]: Tvalue
}



export interface action {
    "type": string,
    "name": string,
    "options": {
        "url"?: string,
        "message"?: string
    }
}

// global variables 
let fileName:string = 'sunset.json'
let story = jsonParser(fileName) as story


// Regex declaration for find varible to substitute
const moustache = new RegExp('\\{{(.*?)\\}}')

// function that take a file name and return a parsed json
export function jsonParser(fileName: string) : object{
    let raw:string = fs.readFileSync(`./stories/${fileName}`, { encoding: "utf8" })
    return JSON.parse(raw)
}

export function moustacheChecker(urlString: string): IRegx[]{
    let final: IRegx[] = []
    while (true){
        let newmatch: string[]|null = urlString.match(moustache)
        if(newmatch !== null){
            urlString = urlString.replace(newmatch[0], '')
            let pair: IRegx ={
                "raw": newmatch[0],
                "filtered" : newmatch[1]
            }
            final.push(pair)
        } else{
            break
        }
    }
    return final
}


export async function httpGet(url:string) {
    let result = await axios.get(url).then( function (response:Inames<object>){
        return response.data
    })
    return result
}


// function that replace the {{}} notation
export function moustacheReplace(url:string, moustaches:IRegx[], names:Inames<Inames<string|number>>): string{
    for (let moust of moustaches){
        let splitted : string[] = moust.filtered.split('.')
        // this function work only with 2 indentetion
        if (splitted[0] in names && splitted.length == 2){
            url = url.replace(moust.raw, String(names[splitted[0]][splitted[1]]))
        } else if(splitted[0] in names && splitted.length == 3){
            url = url.replace(moust.raw, String(names[splitted[0]][splitted[1][splitted[2]]]))
        }
    }
    return url
}


// function that take a link and return the result
export async function httpAction(url: string, names: Inames<Inames<string|number>>){
    let moustaches: IRegx[] = moustacheChecker(url)
    if(moustaches.length > 0){
        url = moustacheReplace(url,moustaches, names )
    }
    let result = await httpGet(url)
    console.log(result)
    return result
}

// TODO: Fix the flow of the function when a url is passed, you have to check if the url have {{}} or not
// TODO: write the test of a function that take the url and sostitute all the {{}} with corrisponding value from "names"

// main function
export function storyTeller(story: story): void{
    let names: Inames<Inames<string|number>> = {
        "location": {
            "latitude": 0.02222,
            "longitude": 0.22555555
        }
    }
    for (let action of story.actions){
        if (action.type == "HTTPRequestAction" && action.options.url !== undefined){
            httpAction(action.options.url, names)
            // console.log(name)
        }
    }
    
}


storyTeller(story)

const app = express()

// app.get('/', (req: object, res: object) => {
//     console.log(typeof req)
// })

// app.listen(3000, () => {
//     console.log('Server Ready')
// })