//Reproduce a calculator just using APIs.

//Create a list of endpoints to reproduce the operations of Sum, Subtraction, Multiply and Division.

//Each API should:

//Accept a list of parameters within the body section
//Be called only with POST method
//Return the result of the operation, and provide an error if the operation is not possible

const express = require('express')
const app = express()
const { operation } = require("./operation")
const result = []


app.post("/:id", (req, res) => {
    const {number1, number2} = req.query

    const { id } = req.params
    
    const calc = operation.find(
        (calc) => calc.id === id
    )
    
    if (calc.id === "+") {
        let final = Number(number1) + Number(number2);
        result.push(final)
        res.json({success: true, result: final});
    }
    else if (calc.id === "-") {
        let final = Number(number1) - Number(number2);
        result.push(final)
        res.json({success: true, result: final});
    }
    else if (calc.id === "*") {
        let final = Number(number1) * Number(number2);
        result.push(final)
        res.json({success: true, result: final});
    }
    else if (calc.id === "divi") {
        if (Number(number2) === 0) {
            let final = "Error"
            result.push(final)
            res.json({success: true, result: final});
        } else {
        let final = Number(number1) / Number(number2);
        result.push(final)
        res.json({success: true, result: final});
        };
    }
    
})


app.listen(3000)