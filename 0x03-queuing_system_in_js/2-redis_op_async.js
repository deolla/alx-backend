// Add two functions: setNewSchool and displaySchoolValue.
// setNewSchool should accept two arguments: schoolName (string) and value (string).
// displaySchoolValue should accept one argument: schoolName (string).

import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

const setNewSchool = (schoolName, value) => {
  setAsync(schoolName, value)
    .then((reply) => {
      console.log(`Reply: ${reply}`);
    })
    .catch((err) => {
      console.error(`Error setting value for ${schoolName}: ${err.message}`);
    });
};

async function displaySchoolValue(schoolName) {
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);
  } catch (error) {
    console.error(`Error getting value for ${schoolName}: ${error.message}`);
  }
}

(async () => {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
})();
