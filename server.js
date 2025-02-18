const express = require("express");
const { Sequelize, DataTypes, Op } = require("sequelize");
const path = require("path");

const app = express();
const PORT = 3000;

// Initialize SQLite database
const sequelize = new Sequelize({
  dialect: "sqlite",
  storage: "./search.db",
});

// Define Item model
const Item = sequelize.define("Item", {
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
});

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Route: Serve homepage
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Route: Search API
app.get("/search", async (req, res) => {
  const query = req.query.q;
  if (!query) return res.json({ results: [] });

  const items = await Item.findAll({
    where: {
      name: {
        [Op.like]: `%${query}%`
      }
    },
  });

  
  res.json({ results: items.map((item) => item.name) });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
