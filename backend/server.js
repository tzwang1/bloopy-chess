require('isomorphic-fetch');
// import express from 'express';
// import amqp from 'amqplib/callback_api';
const express = require("express");
const amqp = require('amqplib/callback_api');
const cors = require('cors');
const session = require('express-session');
const bodyParser = require('body-parser');
const Utilities = require('../frontend/src/Utilities');


const app = express();
app.use(cors({
    origin: "http://localhost:3000",
    credentials: true
}));
app.use(session({
    secret: 'bloopy-chess',
    resave: false,
    saveUninitialized: true

}));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

AMQP_HOST = "amqp://localhost"

function generateUuid() {
  return Math.random().toString() +
         Math.random().toString() +
         Math.random().toString();
}

app.listen(5000, () => {
    console.log("app is running on port 5000");
})

app.get('/', function(req, res) {
    console.log("Home page");
    console.log(req.sessionID);
    res.send("Home page");
});

app.get('/playTwoRandomBots', function(req, res){
    amqp.connect(AMQP_HOST, function(err, conn) {
        conn.createChannel(function(err, ch) {
            ch.assertQueue('', {exclusive: true}, function(err, q) {
            let corr = req.sessionID;
            let game_type = "twoRandomBots";

            ch.consume(q.queue, function(msg) {
                if (msg.properties.correlationId == corr) {
                    res.send(msg.content);
                }
            }, {noAck: true});
            console.log(req.query.new_game);
            game_data = {"game_type": game_type, "new_game": req.query.new_game}
            
            ch.sendToQueue('rpc_queue',
            new Buffer.from(JSON.stringify(game_data)),
            { correlationId: corr, replyTo: q.queue });
            });
        });
    });
})

app.post('/oneBotOneHuman', function(req, res) {
    // console.log("Received request for /oneBotOneHuman");
    amqp.connect(AMQP_HOST, function(err, conn) {
        conn.createChannel(function(err, ch) {
            ch.assertQueue('', {exclusive: true}, function(err, q) {
            let corr = req.sessionID;
            let human_player = req.body.human_player;

            ch.consume(q.queue, function(msg) {
                if (msg.properties.correlationId == corr) {
                    // console.log(JSON.parse(msg.content));
                    res.send(msg.content);
                }
            }, {noAck: true});
            // console.log("Request body: ", req.body);
            // console.log(req.body.move);
            // game_data = {"game_type": game_type, "move": req.body.move }
            ch.sendToQueue('rpc_queue',
            new Buffer.from(JSON.stringify(req.body)),
            { correlationId: corr, replyTo: q.queue });
            });
        });
    });
})





