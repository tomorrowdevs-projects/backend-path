class Validator {

    validate(bodyRequest, rules) {
        const errors = [];

        Object.keys(rules).forEach( key => {
            const rulesForThatKey = rules[key].split('|');

            rulesForThatKey.forEach( rule => {
                if(rule === 'requested') {
                    const requestedValidationResult = this.isRequested(bodyRequest, key);
                    if(requestedValidationResult) errors.push(requestedValidationResult);
                }
                if(rule === 'number') {
                    const numberValidationResult = this.isNumber(bodyRequest, key);
                    if(numberValidationResult) errors.push(numberValidationResult);
                }
            });
        });

        return errors.length > 0 ? errors : false;
    }

    isRequested(req, key) {
        if(!req.hasOwnProperty(key)) {
            return `Missing '${key}' key in body request`;
        }
        return false;
    }

    isNumber(req, key) {
        if(req.hasOwnProperty(key) && isNaN(parseFloat(req[key]))) {
            return `'${key}' is not a number`;
        }
        return false;
    }
}

module.exports = new Validator();