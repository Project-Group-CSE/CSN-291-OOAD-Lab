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
  res.render("features");
});

app.get("/features/userdetails", (req, res) => {
  res.render("userdetails");
});

app.get("/features/dashboard", (req, res) => {
  res.render("userdashboard");
});

app.get("/features/CheckPassword", (req, res) => {
  res.render("check_Password");
});


app.get("/features/Breach_Checker", (req, res) => {
  res.render("breach_checker");
});

app.get("/features/password_generator", (req, res) => {
  res.render("password_generator");
});
app.get("/features/profiles", (req, res) => {
  res.render("userprofiles");
});

app.listen(3000, () => {
  console.log("Server started");
});
