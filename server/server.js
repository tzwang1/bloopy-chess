const express = require("express");
const amqp = require('amqplib/callback_api');

const app = express();

app.listen(process.env.PORT || 3000, () => {
    console.log("app is running on port 3000");
});

