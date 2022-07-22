express = require('express');
router = express.Router();
const { createUser, getAllUsers } = require('../controllers/usersController');
const postExercise = require('../controllers/postExerciseController');
const getExercises = require('../controllers/getUserExercisesController');

router
    .route('/users')
    .post((req, res) => {
        createUser(req, res);
    })
    .get((req, res) => {
        getAllUsers(req, res);
    });

router.post('/users/:_id/exercises', (req, res) => {
    postExercise(req, res);
});

router.get('/users/:_id/logs', (req, res) => {
    getExercises(req, res);
});

module.exports = router;
