const mongoose = require('mongoose');
const Exercise = require('../model/Exercise');
const User = require('../model/User');

// function to save an exercise in the exercise collection of mongodb
// returns the exercise object saved in the db
const createExercise = async (user_data, description, duration, date) => {
    try {
        let exercise = await Exercise.create({
            username: user_data.username,
            description: description,
            duration: duration,
            date: date ? new Date(date) : undefined,
        });
        return exercise;
    } catch (err) {
        console.error(err);
    }
};

// function that handle post request of an exercise
const postExercise = async (req, res) => {
    const { description, duration, date } = req.body;
    const user_id = req.body[':_id'] || req.params._id;

    // if a field in the request is missing
    if (!description || !duration) {
        return res
            .status(400)
            .json({ error: 'Please complete all the form data' });
    }

    // if the _id param is missing
    if (!user_id) {
        return res
            .status(400)
            .json({ error: 'Missing user id in request params' });
    }
    // if all params are present we search the user
    try {
        let db_user = await User.findOne({ _id: user_id }).exec();
        if (!db_user) {
            // if user is not found in the db
            return res.status(404).json({
                error: 'User not found, please provide a valid user id',
            });
        }
        const data = await createExercise(db_user, description, duration, date);

        // this is the response object required
        const res_obj = {
            username: data.username,
            description: data.description,
            duration: data.duration,
            date: data.date.toDateString(),
            _id: db_user._id,
        };
        return res.status(200).json(res_obj);
    } catch (err) {
        console.log(err);
    }
    console.log(description, duration, date, user_id);
};

module.exports = postExercise;
