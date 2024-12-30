const WebSocket = require('ws');
const server = require('../src/server');

describe('WebSocket', () => {
  let ws;
  
  beforeEach((done) => {
    ws = new WebSocket('ws://localhost:3000');
    ws.on('open', done);
  });

  afterEach(() => {
    ws.close();
  });

  test('Should connect successfully', (done) => {
    ws.on('message', (data) => {
      expect(JSON.parse(data)).toHaveProperty('type', 'connection');
      done();
    });
  });
});