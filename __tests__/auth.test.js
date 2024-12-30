const request = require('supertest');
const app = require('../src/app');
const { createUser, validateToken } = require('../src/services/auth');

describe('Authentication', () => {
  test('Should create user successfully', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'Password123!'
    };
    const user = await createUser(userData);
    expect(user.email).toBe(userData.email);
  });

  test('Should authenticate user', async () => {
    const response = await request(app)
      .post('/auth/login')
      .send({
        email: 'test@example.com',
        password: 'Password123!'
      });
    expect(response.status).toBe(200);
    expect(response.body.token).toBeDefined();
  });
});