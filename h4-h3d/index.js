const express = require("express");
const bodyparser = require("body-parser");
let ejs = require("ejs");
const app = express();
app.use(bodyparser.urlencoded({ extended: true }));
app.set("view engine", "ejs");
app.use(express.static("static"));

app.get("/", (req, res) => {
  res.render("homepage");
});

app.get("/contact", (req, res) => {
  res.render("contact card");
});

app.get("/login", (req, res) => {
  res.render("login");
});

app.get("/about", (req, res) => {
  res.render("aboutus");
});

app.get("/register", (req, res) => {
  res.render("register");
});

app.get("/features", (req, res) => {
  res.render("dashboard");
});

app.listen(3000, () => {
  console.log("Server started");
});
