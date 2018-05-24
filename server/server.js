const express = require("express");
const amqp = require('amqplib/callback_api');

const app = express();

var args = process.argv.slice(2);

amqp.connect('amqp://localhost', function(err, conn) {
  conn.createChannel(function(err, ch) {
    ch.assertQueue('', {exclusive: true}, function(err, q) {
      var corr = generateUuid();
      var game_type = "two random bots"

      //console.log(' [x] Requesting test(%d)', num);

      ch.consume(q.queue, function(msg) {
        if (msg.properties.correlationId == corr) {
          console.log(' [.] Got\n %s', msg.content.toString());
          setTimeout(function() { conn.close(); process.exit(0) }, 500);
        }
      }, {noAck: true});

      ch.sendToQueue('rpc_queue',
      new Buffer.from(game_type),
      { correlationId: corr, replyTo: q.queue });
    });
  });
});

function generateUuid() {
  return Math.random().toString() +
         Math.random().toString() +
         Math.random().toString();
}

// app.listen(process.env.PORT || 3000, () => {
//     console.log("app is running on port 3000");
// });



