
// =============================================================================

var express    = require('express');
const Aerospike = require('aerospike');
var app        = express(); 
var http = require('http');
var bodyParser = require('body-parser');
var bcrypt = require('bcrypt-nodejs');
var crypto = require('crypto');
var path = require('path');
var fs = require('fs');
var constants = require("constants");
var op = Aerospike.operator;
var iconv = require('iconv-lite');


app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;
var SERVER_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4bstItI4kdHNqONsukB2l4fT2OdpurLNwsjvYEC3boN7Q8PfPGNB1fnyAPBa63yZYjcjK7QmIsLehrb+0vURmWFNiPGUIvsfL/rJlQ3Vga2hlyy0sH33JluYrKnZQ04UuTmzk0eUvMyPVl9kQMWkeX7YwrC52FlL6wxYVgzxNC/rUJYDVfpd+fp9Lq+12fFxDtcB1+5dy6mWD9GCasxhbX1dbMkCftpeDnvvIQ1aYySmRKSD3ZkOccXOo2NaAyHqByR2KICcymvP3uvr622WQfNjPFhkoZLo4GQ/Aa+Lk8/KKHHhHhBI9k9LSJlMRpktO1oLUY+Zt77Aob7smmnAuwIDAQAB\n-----END PUBLIC KEY-----";
var CLIENT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs+eZDButVb8nC91QA2NuK9/JoJyz5r013SNoUhxV3gPp8jA9gY5KoMUuMOS8z2aTkTXVXTPeCQczBLHgwCnvHh9uD3FyG7gtOQZQGAnY5EKjVyytWirv1T4mk7jGBRL0e6f7NlZSMive2m9qAfzIxdm4PTYqob/I59Qe2yqEE1SrC9yWGMqLOOKahsBmb3cEncJ6R/RQD0ETx6gXGYbhxqHh7bpwULmc0Yjoh1Wf8PI7e/KFVzBziNj/u64Fjitcm4wPl6OobrWFFjDEaTP2NN3Bq68L2PXTBg7kLHa7tK2x3Gz0wOCPjpzN34N27zRIBPK4zo299zv5jSnA8chUSQIDAQAB\n-----END PUBLIC KEY-----";
var abpath = path.resolve("private.pem");
var privatekey = {"key":fs.readFileSync(abpath, "utf8"), "passphrase":process.env.ENCRYPTION_PASSWORD};
  
//Echelon marketing costs

const CREATE_PROJECT = 50;
const TRAIN = 25;
const PULL_WEIGHTS = 10;
const ADD_DATA = 1;

// =============================================================================
var router = express.Router();

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

function checkCredits(cost, uid)
{
  var key = Aerospike.key('uims', 'userinfo', uid);
  client.get(key, function(error, record, metadata)
    {
      if(error)
        return false;
      else
      {
        if(record.credits>=cost)
          return true;
        else
          return false;
      }
    });
}

function validateAPIKey(projectID, key)
{
  var key = Aerospike.key('pims','projectinfo', projectID);
  client.get(key, function(error, record, metadata)
    {
      if(error)
        return false;
      else
      {
        if(bcrypt.compareSync(key, record.api_key))
          return true;
        else
          return false;
      }
    });
}

var authenticateAdmin = function(req, res, next)
{
  var password = process.env.HTTPS_AUTH.toString();
  var auth = req.body.auth.toString();  
  var access = password.localeCompare(auth);
  console.log("["+access+"] "+req.connection.remoteAddress);
  if(access==0)
  {
    next();
  }
  else
  {
    res.json({"error":"access denied"});
  }
}

router.use('/admin', authenticateAdmin);


router.route('/api/weights').get(function(req, res)
{
  
});

router.route('/api/submit-training-data').post(function(req, res)
{
    var projectid = req.body.projectid;
    var apikey = req.body.key;

    if(validateAPIKey(projectid, key))
    {
      var sampleID = req.body.sampleID;
      var datapoint = req.body.datapoint;

      var key = new Aerospike.Key('dims', projectid, sampleID);
      var rec = 
      {
        id: sampleID,
        data: datapoint
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

      }else{
        res.json({"message":"access denied"})
      }
  });

router.route('/api/train').get(function(req,res)
{

});

router.route('/admin/userops/addCredits').post(function(req, res)
{
  var uid = req.body.uid;
  var numCredits = parseInt(req.body.numcredits);
  var key = new Aerospike.Key('uims', 'userinfo', uid);

  var ops = [
      op.incr('credits',numCredits),
      op.read('credits')
  ];

  client.operate(key, ops, function(err, rec)
  {
    if(err)
      res.json({"message":"could not add credits"});
    else
      res.json({"message" : "user now has "+rec.credits+" credits"});
  });
});

router.route('/admin/userops/getUserData').post(function(req, res)
{
  var uid = req.body.uid;
  var key = new Aerospike.Key('uims', 'userinfo', uid);
  
  var ops = [
      op.read('credits'),
      op.read('user_name'),
      op.read('email_address')
  ];

  client.operate(key, ops, function(err, rec)
  {
    if(err)
      res.json({"error":"user not found", "name":"NA","email":"NA", "credits":"NA"});
    else
      res.json({"error":"NA", "name":rec.user_name,"email":rec.email_address, "credits":rec.credits});
  });
});

router.route('/admin/userops/getCredits').post(function(req, res)
{
  var uid = req.body.uid;
  var key = new Aerospike.Key('uims', 'userinfo', uid);
  
  var ops = [
      op.read('credits')
  ];

  client.operate(key, ops, function(err, rec)
  {
    if(err)
      res.json({"message":"could not read user credits"});
    else
      res.json({"message" : "user has "+rec.credits+" credits"});
  });
});

router.route('/admin/userops/createUser').post(function(req, res)
{
  var uid = req.body.uid;
  var name = req.body.name;
  var email = req.body.email;
  var usercredits = 0;

	var key = new Aerospike.Key('uims', 'userinfo', uid);
  var rec = 
  {
    user_id: uid,
    user_name: name,
    email_address: email,
    credits: usercredits 
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
    {
      console.info(record);
      res.json({"message":"user already exists"});
    }
  });
});

router.route('/admin/userops/createNewProject').post(function(req, res)
{
  var uid = req.body.uid;
  var projectid = req.body.projectid;
  var apikey = req.body.apikey;
  var numLayers = req.body.numlayers;
  var neuronsPerLayer = req.body.neurons;

  var key = new Aerospike.Key('pims', 'projectinfo', projectid);
  var rec = 
  {
    user_id: uid,
    project_id: projectid,
    api_key: apikey,
    num_layers: numLayers,
    neurons_per_layer: neuronsPerLayer
  }

  client.get(key, function(error, record, metadata)
  {
    if(error)
    {
      client.put(key, rec, function(err)
      {
        if(err)
        {
          res.json({"message":"error creating project"});
        }else{
          if(checkCredits(CREATE_PROJECT, uid))
            res.json({"message":"project created"});
          else
            res.json({"message":"not enough credits"});
        }
      });
    }
    else
    {
      console.info(record);
      res.json({"message":"Project name taken"});
    }
  });
});

router.route('/admin/test').post(function(req, res)
{
  var hash = bcrypt.hashSync(req.body.key);
  res.json({"passkey":hash});
});

// =============================================================================

app.use('/', router);

http.createServer(app).listen(port);
console.log("Listening on port: "+port);
