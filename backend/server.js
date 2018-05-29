const express = require("express");
const amqp = require('amqplib/callback_api');
const cors = require('cors');
const uuidv4 = require('uuid/v4');

const app = express();
app.use(cors());

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
    if(!req.cookies){
        console.log(uuidv4());
    } else {
        console.log(req.cookies._xsrf);
    }
    res.send("Home page");
});

app.get('/twoRandomBots', function(req, res){
    console.log("Received request for /twoRandomBots");
    amqp.connect(AMQP_HOST, function(err, conn) {
        conn.createChannel(function(err, ch) {
            ch.assertQueue('', {exclusive: true}, function(err, q) {
            let corr = generateUuid();
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



