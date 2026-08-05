const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

const dataFile = path.join(__dirname, "data.json");

app.use(express.json());

// 🔥 MOST IMPORTANT (STATIC FILES FIX)
app.use(express.static(__dirname));

app.get("/", (req, res) => {
  res.sendFile(require("path").join(__dirname, "index.html"));
});

// 👉 homepage
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// 👉 GET trips
app.get("/trips", (req, res) => {
  let data = [];

  if (fs.existsSync(dataFile)) {
    data = JSON.parse(fs.readFileSync(dataFile));
  }

  res.json(data);
});

// 👉 POST trips
app.post("/trips", (req, res) => {
  let data = [];

  if (fs.existsSync(dataFile)) {
    data = JSON.parse(fs.readFileSync(dataFile));
  }

  data.push(req.body);

  fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));

  res.json({ message: "Trip saved!" });
});

// 👉 start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

app.get("/test", (req, res) => {
  res.send("Server working");
});
