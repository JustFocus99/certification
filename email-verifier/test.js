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

/**
 * 
 * k6 run test.js

         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 


     execution: local
        script: test.js
        output: -

     scenarios: (100.00%) 1 scenario, 10 max VUs, 1m0s max duration (incl. graceful stop):
              * default: 10 looping VUs for 30s (gracefulStop: 30s)



  █ TOTAL RESULTS 

    checks_total.......: 6543    217.741184/s
    checks_succeeded...: 100.00% 6543 out of 6543
    checks_failed......: 0.00%   0 out of 6543

    ✓ status is 204

    HTTP
    http_req_duration..............: avg=45.68ms min=14.52ms med=37.6ms  max=313.36ms p(90)=74.43ms p(95)=98.63ms
      { expected_response:true }...: avg=45.68ms min=14.52ms med=37.6ms  max=313.36ms p(90)=74.43ms p(95)=98.63ms
    http_req_failed................: 0.00%  0 out of 6543
    http_reqs......................: 6543   217.741184/s

    EXECUTION
    iteration_duration.............: avg=45.88ms min=14.7ms  med=37.79ms max=313.66ms p(90)=74.63ms p(95)=99.1ms 
    iterations.....................: 6543   217.741184/s
    vus............................: 10     min=10        max=10
    vus_max........................: 10     min=10        max=10

    NETWORK
    data_received..................: 177 kB 5.9 kB/s
    data_sent......................: 1.1 MB 37 kB/s




running (0m30.0s), 00/10 VUs, 6543 complete and 0 interrupted iterations
default ✓ [======================================] 10 VUs  30s
 */