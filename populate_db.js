const { Sequelize, DataTypes } = require('sequelize');

// Initialize SQLite database
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './search.db',
});

// Define the model
const Item = sequelize.define('Item', {
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
});

// Function to populate database
async function insertSampleData() {
  await sequelize.sync({ force: true }); // Reset database
  await Item.bulkCreate([
    { name: "Apple" },
    { name: "Banana" },
    { name: "Cherry" },
    { name: "Date" },
    { name: "Elderberry" },
    { name: "Fig" },
    { name: "Grape" },
    { name: "Honeydew" }
  ]);
  console.log("Database populated successfully!");
}

// Run the function
insertSampleData().then(() => {
  sequelize.close();
}).catch(err => console.error(err));
