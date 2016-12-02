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
var crypto = require('crypto');
var path = require('path');
var fs = require('fs');
var constants = require("constants");
const op = Aerospike.operator;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;        // set our port
var SERVER_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4bstItI4kdHNqONsukB2l4fT2OdpurLNwsjvYEC3boN7Q8PfPGNB1fnyAPBa63yZYjcjK7QmIsLehrb+0vURmWFNiPGUIvsfL/rJlQ3Vga2hlyy0sH33JluYrKnZQ04UuTmzk0eUvMyPVl9kQMWkeX7YwrC52FlL6wxYVgzxNC/rUJYDVfpd+fp9Lq+12fFxDtcB1+5dy6mWD9GCasxhbX1dbMkCftpeDnvvIQ1aYySmRKSD3ZkOccXOo2NaAyHqByR2KICcymvP3uvr622WQfNjPFhkoZLo4GQ/Aa+Lk8/KKHHhHhBI9k9LSJlMRpktO1oLUY+Zt77Aob7smmnAuwIDAQAB\n-----END PUBLIC KEY-----";
var CLIENT_PUBLIC_KEY="SOME KEY";

var abpath = path.resolve("private.pem");
var privatekey = {"key":fs.readFileSync(abpath, "utf8"), "passphrase":process.env.ENCRYPTION_PASSWORD};
  
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

function decrypt(text)
{
  //decrypt server
  var server_buffer = new Buffer(text, "base64");
  var server_decrypted = crypto.privateDecrypt(privatekey, server_buffer);
  
  //decrypt client
  var client_buffer = new Buffer(decrypted.toString("utf8"), "base64");
  var client_decrypted = crypto.publicDecrypt(CLIENT_PUBLIC_KEY, client_buffer);

  return client_decrypted.toString("utf8");
}

/*
router.use('/admin/userops',function(req, res, next)
{
  console.log('Admin attempt from '+req.connection.remoteAddress);
  next();
});
*/

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

router.route('/admin/userops/addCredits').post(function(req, res)
{
  var uid = req.body.uid;
  var numCredits = req.body.numcredits;
  var key = new Aerospike.Key('uims', 'userinfo', uid);

  var ops = [
    op.increment('credits', numCredits);
    op.read('credits')
  ];

  client.operate(key, ops, function(error, record)
  {
    if(error)
      res.json({"message":"could not add credits"});
    else
      res.json({"message":"user has "+record+" credits."})
  });
});

router.route('/admin/userops/getCredits').get(function(req, res)
{
  
});

router.route('/admin/userops/createUser').post(function(req, res)
{
  var uid = req.body.uid;
  var name = req.body.name;
  var email = req.body.email;

	var key = new Aerospike.Key('uims', 'userinfo', uid);
  var rec = 
  {
    user_id: uid,
    user_name: name,
    email_address: email,
    credits: 0 
  }

  client.get(key, function(error, record, metadata)
  {
    if(error)
    {
      client.put(key, rec, function(err)
      {
        if(err)
        {
          res.json({"message":"error creating user"});
        }else
        {
          res.json({"message":"user created"});
        }
      });
    }
    else
      res.json({"message":"user already exists"});
  });
});

router.route('/admin/test').get(function(req, res)
{
  
});



// REGISTER OUR ROUTES -------------------------------
app.use('/', router);

// START THE SERVER
// =============================================================================
http.createServer(app).listen(port);
console.log("Listening on port: "+port);
