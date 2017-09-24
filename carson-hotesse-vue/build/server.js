var express = require('express');
var path = require('path');
var serveStatic = require('serve-static');
var morgan = require('morgan');
var bodyParser = require('body-parser');

// var config = require('../config')

var app = express();

// HTTP Authentication 

app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())
//app.use(morgan('dev'));
//app.use('/api', routes)

app.use("/static", express.static(path.join(__dirname, '/../dist/static')));

//var staticPath = path.posix.join(config.build.assetsPublicPath, config.build.assetsSubDirectory)
//app.use(staticPath, express.static('./static'))
/* GET home page. */
app.get('/', function(req, res, next) {
	res.sendFile(path.join(__dirname + '/../dist/index.html'));
});


var port = process.env.PORT || 3000;
app.listen(port);
console.log('server started '+ port);