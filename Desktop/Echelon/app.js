// server.js

// BASE SETUP
// =============================================================================

// call the packages we need
var express    = require('express');        // call express
var app        = express(); 
var http = require('http');               // define our app using express
var bodyParser = require('body-parser');
const Aerospike = require('aerospike');
var bcrypt = require('bcrypt-nodejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;        // set our port


// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();              // get an instance of the express Router

var client = Aerospike.client({
  hosts: [{addr: "104.196.232.255", port: 3000}],
  log: {level: Aerospike.log.INFO},
  policies: {timeout: 15000}
});

client.connect(function(error){
  if(error)
  {
    console.log("Error connecting to cluster");
  }else
  {
    console.log("Connected to aerospike");
  }
});

router.route('/api/weights').get(function(req, res)
{
  
});

router.route('/api/submit-training-data').post(function(req, res)
{
    var sampleID = req.body.sampleID;
    var username = req.body.username;
    var data = req.body.data;

    var key = new Aerospike.Key('data', username, sampleID);
    var rec = 
    {
      user: username,
      sample_id: sampleID,
      dataset: data
    }

    console.log("Trying to push data...");

    client.put(key, rec, function(error)
    {
      if(error)
      {
        console.log("Error pushing data.");
      }else{
        console.log("Data pushed successfully.");
      }
    });

    res.json({"message":"data added"});

});

router.route('/api/train').get(function(req,res)
{

});

router.route('/admin/addCredits').post(function(req, res)
{
  
});

router.route('/admin/removeCredits').post(function(req, res)
{
  
});

/*
router.route('/api/get-training-data').get(function(req,res)
{
  var namespace = 'test';
  var username = req.query.username;
  var scan = client.scan(namespace, username);
  
  scan.concurrent = false;
  scan.nobins = false;
  console.log('Getting data for: '+username);
  var stream = scan.foreach()
  stream.on('data', function(record)
    {
      console.log(record);
    })
  res.json({"message":"data retrieved!"});
});

/*
router.route('/admin/setPassword').post(function(req, res)
{
    var username = req.body.username;
    var password = String(req.body.password);
    bcrypt.hash(password, null, null, function(err, hash)
    {
      if(err)
        res.json({"message" : "There was an error"});
      else
      {
          var key = new Aerospike.Key('users','admin_passwords', username);
          var rec = 
          {
            user: username,
            password: hash
          }

          console.log("setting password...");

          client.put(key, rec, function(error)
          {
            if(error)
            {
              console.log("Password not set.");
            }else{
              console.log("Password set "+password);
            }
          });

          res.json({"message":"password changed"});
      }
  });
});

router.route('/admin/login/:username/:password').get(function(req, res)
{
    var username = req.params.username;
    var password = req.params.password;
    const key = new Aerospike.key('users','admin_passwords', username);
    client.get(key, function(error, record, metadata)
    {
      if(error)
        res.json({"message":"user not found"});
      else
      {
        var hash = record.password;
          
        bcrypt.compare(password, hash, function(err, results)
        {
          if(err)
            res.json({"message":"logon servers not available"});
          else if(results)
             res.json({"message":"welcome!"});
           else
             res.json({"message":"wrong password!"});
        })
        
      }
    });
});
*/

router.route('/admin/setCredits').post(function(req, res)
{

});

router.route('/admin/addUser').post(function(req, res)
{
	
});

router.route('/admin/getCredits').get(function(req, res)
{
	
});

router.route('/admin/test').get(function(req, res)
{
  res.json({"message": "hello world"});
});



// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/', router);
// START THE SERVER
// =============================================================================
http.createServer(app).listen(port);
console.log("Listening on port: "+port);
