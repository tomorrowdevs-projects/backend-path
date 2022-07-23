const mongoose = require('mongoose');
const Exercise = require('../model/Exercise');
const User = require('../model/User');

const getExercises = async (req, res) => {
    // retrieve query params if specified and convert to date objects
    const date_from = req.query.from ? new Date(req.query.from) : undefined;
    const date_to = req.query.to ? new Date(req.query.to) : undefined;
    // check if date interval is valid

    if (date_from >= date_to) {
        console.log(date_from);
        console.log(date_to);
        return res
            .status(400)
            .json({ error: 'please specify a valid date interval' });
    }

    // here we check if limit is present and if is greater or equal than 0
    // with 0 as a limit all the logs present will be returned
    const limit =
        parseInt(req.query.limit) >= 0 ? parseInt(req.query.limit) : 0;

    const req_id = req.params._id;

    try {
        // first we check if a user with req id exist
        const user_match = await User.findById({ _id: req_id }).exec();
        if (!user_match) {
            // if user is not found we send 404 status with an error msg
            return res.status(404).json({ error: 'User not found' });
        }
        const user = user_match.username;

        // here we search for all the exercises between the specified date interval
        const exercises_log = await Exercise.find({ username: user })
            .where('date')
            .gte(date_from)
            .lte(date_to)
            .limit(limit);
        const ex_count = exercises_log.length;

        // here we create the final log, mapping the original log and removing unwanted fields
        const final_log = exercises_log.map((exercise) => {
            let log = {};
            log['description'] = exercise.description;
            log['duration'] = exercise.duration;
            log['date'] = exercise.date.toDateString();
            return log;
        });

        // initialize and populate the response object
        let res_obj = {};
        res_obj['username'] = user;
        res_obj['_id'] = req_id;
        res_obj['count'] = ex_count;
        res_obj['log'] = final_log;

        // finally we return the complete response object formatted as required
        return res.status(200).json(res_obj);
    } catch (err) {
        console.error(err);
        return res.status(400).json({ error: 'Invalid user id' });
    }
};

module.exports = getExercises;
