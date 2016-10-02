// server.js

// BASE SETUP
// =============================================================================

// call the packages we need
var express    = require('express');        // call express
var app        = express();                 // define our app using express
var bodyParser = require('body-parser');
var firebase = require('firebase');
var spawn = require('child_process').spawn;
var events = require('events');
// configure app to use bodyParser()
// this will let us get the data from a POS
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//Echelon Costs
var trainCost = 50;
var submitSampleCost = 1;
var eventEmitter = new events.EventEmitter();

var port = process.env.PORT || 8080;        // set our port

//Firebase config
//==============================================================================

var config = 
{
    apiKey: "AIzaSyDdk3MF-lbJE-syCHGrprOqRWac2zoJ9hI",
    authDomain: "echelondb.firebaseapp.com",
    databaseURL: "https://echelondb.firebaseio.com",
    storageBucket: "",
 };

firebase.initializeApp(config);

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();              // get an instance of the express Router

//MISC Functions

function checkCredits(userID, creditCheck)
{
	var apicounter = firebase.database().ref('usrData/' + userID+"/credits");
	apicounter.on('value', function(snapshot) {
  			var hasCredits = parseInt(snapshot.val()) >= creditCheck;
        if(hasCredits)
          eventEmitter.emit('has credits');
        else
          eventEmitter.emit('missing credits');
	});
}

//return weights from training
router.route('/api/weights').get(function(req, res)
{
    res.json({ message: 'weights go here'});   
});

router.route('/api/submit-training-data').post(function(req, res)
{
  var userID = req.body.userID;
  var datasetID = req.body.datasetID;
  var data = req.body.data;
  var postsRef = firebase.database().ref().child("data/"+userID+"/"+datasetID);
  postsRef.push().set(
  {
    value: data
  });
  res.json({message: "the data was " + data +" and pushed to data/users/"+userID+"/"+datasetID});
});

router.route('/api/train').get(function(req,res)
{
  var userID = req.param('userID');
  var datasetID = req.param('datasetID');
  //checkCredits(userID, trainCost);
  var apicounter = firebase.database().ref('usrData/' + userID+"/credits");
  apicounter.once('value', function(snapshot) {
        var hasCredits = parseInt(snapshot.val()) >= trainCost;
        if(hasCredits)
        {
           console.log("training!");
           var postsRef = firebase.database().ref().child("usrData/"+userID+"/");
           var apicounter = firebase.database().ref('usrData/' + userID+"/credits");
           var credits = trainCost;
           apicounter.once('value', function(snapshot) {
              credits = parseInt(snapshot.val())-credits;
              if(credits<0)
              {
                credits = 0;
              }
              postsRef.set({
                credits: credits
              });
            console.log(credits);
          });
              res.json({message: "trained!"});
        }
        else
          res.json({message: "missing credits"});
  });
    //var train  = spawn('java', ['-jar', 'helloworld.jar']);
});

router.route('/admin/addCredits').post(function(req, res)
{
	var userID = req.body.userID;
	var credits = parseInt(req.body.credits);
	var postsRef = firebase.database().ref().child("usrData/"+userID+"/");

	var apicounter = firebase.database().ref('usrData/' + userID+"/credits");
	apicounter.on('value', function(snapshot) {
  			credits = credits+parseInt(snapshot.val());
	});
  	postsRef.set({
    	credits: credits
  	});
  res.json({message: "added!"});
});

router.route('/admin/removeCredits').post(function(req, res)
{
	var userID = req.body.userID;
	var credits = parseInt(req.body.credits);
	var postsRef = firebase.database().ref().child("usrData/"+userID+"/");

	var apicounter = firebase.database().ref('usrData/' + userID+"/credits");
	apicounter.on('value', function(snapshot) {
  			credits = parseInt(snapshot.val())-credits;
  			if(credits<0)
  			{
  				credits = 0;
  			}
	});
  	postsRef.set({
    	credits: credits
  	});
  res.json({message: "removed!"});
});

router.route('/admin/setCredits').post(function(req, res)
{
	var userID = req.body.userID;
	var credits = parseInt(req.body.credits);
	var postsRef = firebase.database().ref().child("usrData/"+userID+"/");

  	postsRef.set({
    	credits: credits
  	});
  res.json({message: "set "+credits+" as user credits for " +userID});
});

router.route('/admin/addUser').post(function(req, res)
{
	var userID = req.body.userID;
	var postsRef = firebase.database().ref().child("usrData/"+userID+"/");

  	postsRef.set({
    	credits: 0
  	});
  res.json({message: "added "+userID});
});

router.route('/admin/getCredits').get(function(req, res)
{
	var userID = req.param('userID');
	var credits = 0;
	var apicounter = firebase.database().ref('usrData/' + userID+"/credits");
	apicounter.on('value', function(snapshot) {
  			credits = parseInt(snapshot.val());
	});
  res.json({message: userID+" has "+credits+" api calls remaining"});
});

// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/', router);
// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);