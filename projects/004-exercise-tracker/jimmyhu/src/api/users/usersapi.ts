const exps: any = require('express')

const router = exps.Router()


// global variables for store the information
let users: user[] = []
let exercises: exercise[] = []
let alredyUsedIds:  number[] = []


// user interface, the Id will be a random number for now
type user = {
    'username' : string,
    '_id': number
}

// exercise extend the user interface due the structure require the same information anyway
type exercise = user  & {
    "description": string,
    "duration": number,
    "date": Date|string,
}

// function for check if the date is in the interval
function checkdate (Indate:string|Date, start: string, end: string): boolean{
    if (new Date(Indate) > new Date(start) && new Date(Indate) < new Date(end)){
        return true
    } else if (start == undefined || end == undefined){
        return true
    }
    return false
}


// base post request, the id is a random number auto-generated, for avoid double id there are a check on a list
router.post('/', (req: any, res:any): void => {
    let username: string = req.body.name
    let randID: number = Math.floor(Math.random() * 1000)
    while (alredyUsedIds.includes(randID)){
        let randID: number = Math.floor(Math.random() * 1000)
    }
    let newUser: user = {
        'username' : username,
        '_id': randID
    }
    alredyUsedIds.push(randID)
    users.push(newUser)
    res.json(newUser)
})

router.get('/', (req: any, res:any): void => {
    res.json(users)
})

router.post('/:_id/exercises', (req: any, res:any): void => {
    // check if the id exist in the stored list
    if(!alredyUsedIds.includes(parseInt(req.params._id))){
        res.send(`Invalid ID: The id ${req.params._id} do not exist`)
        return
    }
    if(new Date(req.body.date).toUTCString() == null || new Date(req.body.date).toUTCString() == 'Invalid Date'){
        res.send('Invalid Date')
        return
    }
    // check if the required information is different from undefinied
    if(req.body.description == undefined || req.body.duration == undefined){
        res.send("Missing Information")
        return
    }
    // find the id that match in the list of registered user
    let username:string = ''
    let userId: number = parseInt(req.params._id)
    for (let user of users){
        if (user._id == userId){
            username = user.username
            break
        }
    }
    
    let newExercise: exercise = {
        "username": username,
        "_id": userId,
        "description": req.body.description,
        "duration": req.body.duration,
        // if the date is undefined than it will register the current date in UTCS format
        "date": req.body.date == undefined ? new Date(Date.now()).toUTCString() : req.body.date,
    }
    for (let ex of exercises){
        if (ex.username == newExercise.username && ex._id == newExercise._id && ex.description == newExercise.description && ex.duration == newExercise.duration){
            res.send('This Exercise already Exist')
            return
        }
    }
    exercises.push(newExercise)
    res.json(newExercise)
})

router.get('/:_id/logs/:limit?', (req: any, res:any): void => {

    if(!alredyUsedIds.includes(parseInt(req.params._id))){
        res.send(`Invalid ID: The id ${req.params._id} do not exist`)
        return
    }
    let username: string = ''
    for (let user of users){
        if (user._id == parseInt(req.params._id)){
            username = user.username
            break
        }
    }
    let exerciseArray = []
    for (let exer of exercises){
        if (exer._id == parseInt(req.params._id) && exerciseArray.length !== parseInt(req.params.limit) && checkdate(exer.date, req.body.from, req.body.to)){
            let match = {
                "description":exer.description,
                "duration":exer.duration,
                "date":exer.date,
            }
            exerciseArray.push(match)
        }
    }
    let result = {
        "username": username,
        "count": exerciseArray.length,
        "_id": req.params._id,
        "log": exerciseArray.length > 0 ? exerciseArray : "This user doesn't have registered Exercise"
    }
    res.json(result)
})

module.exports = router