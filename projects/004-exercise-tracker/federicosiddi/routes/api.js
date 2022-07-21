express = require('express');
router = express.Router();
const { createUser, getAllUsers } = require('../controllers/usersController');

router
    .route('/users')
    // You can POST to `/api/users` with form data username to create a new user.
    // The returned response from POST `/api/users` with form data username will be an object with username and _id properties.
    .post((req, res) => {
        createUser(req, res);
    })
    // You can make a GET request to `/api/users` to get a list of all users.
    // The GET request to `/api/users` returns an array.
    // Each element in the array returned from GET `/api/users` is an object literal containing a user's username and _id.
    .get((req, res) => {
        getAllUsers(req, res);
    });

router
    .route('/users/:_id/exercises')
    // You can POST to `/api/users/:_id/exercises` with form data description, duration, and optionally date. If no date is supplied, the current date will be used.
    //The response returned from POST `/api/users/:_id/exercises` will be the user object with the exercise fields added.
    .post((req, res) => {});

// You can make a GET request to `/api/users/:_id/logs` to retrieve a full exercise log of any user.
// A request to a user's log GET `/api/users/:_id/logs` returns a user object with a count property representing the number of exercises that belong to that user.
// A GET request to `/api/users/:id/logs` will return the user object with a log array of all the exercises added.
// Each item in the log array that is returned from GET `/api/users/:id/logs` is an object that should have a description, duration, and date properties.
router.get('users/:_id/logs', (req, res) => {});

module.exports = router;
