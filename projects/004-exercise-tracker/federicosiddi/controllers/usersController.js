const mongoose = require('mongoose');
const User = require('../model/User');

// create user and return object with username and _id properties
const createUser = async (req, res) => {
    let user = req.body.username;
    // if req.body has no username attribute we return a status code of 400
    if (!user) return res.status(400).json({ Error: 'Username is required' });

    let duplicate = await User.findOne({ username: user }).exec();
    // if there is already a user registered with req.body.username we return a status code of 409
    if (duplicate)
        return res
            .status(409)
            .json({ Error: 'This user is already registered' });
    try {
        // if username is not duplicate we create a new user
        result = await User.create({ username: user });
        // then we return the newly created user as an object
        return res.status(201).json(result);
    } catch (err) {
        console.error(err);
    }
};

// getAllUsers will return an array of all users
const getAllUsers = async (req, res) => {
    try {
        let result = await User.find();
        return res.status(200).json(result);
    } catch (err) {
        console.log(err);
        return res.json(error);
    }
};

module.exports = { createUser, getAllUsers };
