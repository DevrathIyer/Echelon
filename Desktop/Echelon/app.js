// server.js

// BASE SETUP
// =============================================================================

// call the packages we need
var express    = require('express');        // call express
var app        = express();                 // define our app using express
var bodyParser = require('body-parser');
var firebase = require('firebase');
var spawn = require('child_process').spawn;

// configure app to use bodyParser()
// this will let us get the data from a POS
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;        // set our port

//Firebase config
//==============================================================================

var config = {
    apiKey: "AIzaSyDdk3MF-lbJE-syCHGrprOqRWac2zoJ9hI",
    authDomain: "echelondb.firebaseapp.com",
    databaseURL: "https://echelondb.firebaseio.com",
    storageBucket: "",
 };

firebase.initializeApp(config);

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();              // get an instance of the express Router

//return weights from training
router.route('/weights').get(function(req, res) {
    res.json({ message: 'weights go here'});   
});

router.route('/submit-training-data').post(function(req, res){
  var userID = req.body.userID;
  var datasetID = req.body.datasetID;
  var data = req.body.data;
  var postsRef = firebase.database().ref().child("data/"+userID+"/"+datasetID);
  postsRef.push().set({
    value: data
  });
  res.json({message: "the data was " + data +" and pushed to data/users/"+userID+"/"+datasetID});
});

router.route('/train').get(function(req,res)
{
	var train  = spawn('java', ['-jar', 'helloworld.jar']);
});

// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/api', router);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);