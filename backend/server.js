const express = require("express");
const amqp = require('amqplib/callback_api');

const app = express();

AMQP_HOST = "amqp://localhost"

function generateUuid() {
  return Math.random().toString() +
         Math.random().toString() +
         Math.random().toString();
}

app.listen(5000, () => {
    console.log("app is running on port 5000");
});

app.get('/twoRandomBots', function(req, res){
    amqp.connect(AMQP_HOST, function(err, conn) {
        conn.createChannel(function(err, ch) {
            ch.assertQueue('', {exclusive: true}, function(err, q) {
            let corr = generateUuid();
            let game_type = "two random bots";

            ch.consume(q.queue, function(msg) {
                if (msg.properties.correlationId == corr) {
                    console.log(' [.] Got\n %s', msg.content.toString());
                    res.send(msg.content.toString());
                }
            }, {noAck: true});

            ch.sendToQueue('rpc_queue',
            new Buffer.from(game_type),
            { correlationId: corr, replyTo: q.queue });
            });
        });
    });
})



