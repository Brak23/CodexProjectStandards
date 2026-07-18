import { createServer } from 'node:http';
import { createHandler } from './app.mjs';

const port = Number.parseInt(process.env.PORT ?? '3000', 10);
const server = createServer(createHandler());

server.listen(port, '127.0.0.1', () => {
  console.log(JSON.stringify({ level: 'info', event: 'server.started', port }));
});

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => {
    server.close((error) => {
      if (error) {
        console.error(JSON.stringify({ level: 'error', event: 'server.shutdown_failed', message: error.message }));
        process.exitCode = 1;
      }
    });
  });
}
