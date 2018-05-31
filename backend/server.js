const express = require("express");
const amqp = require('amqplib/callback_api');
const cors = require('cors');
const session = require('express-session');

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

app.get('/twoRandomBots', function(req, res){
    console.log("Received request for /twoRandomBots");
    amqp.connect(AMQP_HOST, function(err, conn) {
        conn.createChannel(function(err, ch) {
            ch.assertQueue('', {exclusive: true}, function(err, q) {
            let corr = req.sessionID;
            console.log("SessionID =", corr);
            let game_type = "two random bots";

            ch.consume(q.queue, function(msg) {
                if (msg.properties.correlationId == corr) {
                    console.log(JSON.parse(msg.content));
                    res.send(msg.content);
                }
            }, {noAck: true});

            ch.sendToQueue('rpc_queue',
            new Buffer.from(game_type),
            { correlationId: corr, replyTo: q.queue });
            });
        });
    });
})



