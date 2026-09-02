import http from 'k6/http';
import {check} from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

const url = 'http://localhost:8081/request-registration';

export default function () {
  const payload = JSON.stringify({
    email: 'test@example.com',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is 204': (r) => r.status === 204,
  });
}