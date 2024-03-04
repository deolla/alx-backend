const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Create Kue queue
const queue = kue.createQueue();

// Initialize the number of available seats
const initialNumberOfSeats = 50;
setAsync('available_seats', initialNumberOfSeats);

// Initialize reservationEnabled to true
let reservationEnabled = true;

// Middleware to parse JSON request body
app.use(express.json());

// Route to get the current number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getAsync('available_seats');
  res.json({ numberOfAvailableSeats });
});

// Function to reserve a seat
const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

// Function to get the current number of available seats
const getCurrentAvailableSeats = async () => {
  const numberOfAvailableSeats = await getAsync('available_seats');
  return parseInt(numberOfAvailableSeats);
};

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
  } else {
    const job = queue.create('reserve_seat').save((err) => {
      if (err) {
        res.json({ status: 'Reservation failed' });
      } else {
        console.log(
            'Seat reservation job',
            job.id,
            'completed'
        );
        res.json({ status: 'Reservation in process' });
      }
    });
  }
});

// Process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentNumberOfSeats = await getCurrentAvailableSeats();
    const newNumberOfSeats = currentNumberOfSeats - 1;

    if (newNumberOfSeats >= 0) {
      await reserveSeat(newNumberOfSeats);

      if (newNumberOfSeats === 0) {
        reservationEnabled = false;
      }

      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});