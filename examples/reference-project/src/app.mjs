export function createHandler() {
  return (request, response) => {
    response.setHeader('content-type', 'application/json; charset=utf-8');

    if (request.method === 'GET' && request.url === '/health') {
      response.writeHead(200);
      response.end(JSON.stringify({ status: 'ok' }));
      return;
    }

    response.writeHead(404);
    response.end(JSON.stringify({ error: { code: 'NOT_FOUND', message: 'Route not found' } }));
  };
}
