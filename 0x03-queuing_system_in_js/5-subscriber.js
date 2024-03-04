// Create a redis client that listens for messages published to the channel holberton school channel.
// When a message is received, the script will log it to the console.
// Upon receiving the message KILL_SERVER, the script will unsubscribe from the channel and exit.

import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

client.subscribe('holberton school channel');
client.on('message', (channel, message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    client.unsubscribe(channel);
    client.quit();
  }
});
