const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Create listProducts array
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);

// Middleware to parse JSON request body
app.use(express.json());

// Route to get the list of products
app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => {
    return {
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock
    };
  }));
});

// Function to reserve stock in Redis
const reserveStockById = (itemId, stock) => {
  redisClient.set(`item.${itemId}`, stock);
};

// Async function to get the current reserved stock from Redis
const getCurrentReservedStockById = async (itemId) => {
  const reservedStock = await getAsync(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock) : 0;
};

// Route to get product details
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = listProducts.find(p => p.id === itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);
    res.json({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity: currentQuantity
    });
  }
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = listProducts.find(p => p.id === itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);

    if (currentQuantity >= product.stock) {
      res.json({ status: 'Not enough stock available', itemId: product.id });
    } else {
      reserveStockById(itemId, currentQuantity + 1);
      res.json({ status: 'Reservation confirmed', itemId: product.id });
    }
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});