const express = require("express");
const app = express();
app.use(express.static(__dirname + '/public'));
var server = require("http").Server(app);
server.listen(4000,()=>{
	console.log("server listen on port 4000")
});
app.get('/', (req, res)=>{
    res.render('index.html')
})