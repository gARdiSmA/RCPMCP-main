#!/bin/bash

# Session cookies variable
SESSION_COOKIES='adAuthCookie=3E4B8442C4C2B56A55611D00DB26D793B8B72FC1FC5D433E8C1EB8DB8923CCF9FAF264C8E59D72BAD342196F9E3C24AF277BB92504B17312AF5CF5E3E3983700C6688964BA9FD75864A6797CB6B074459C815AB3BD601F98D8A0517445BF8E509920987EB4CE13A80F04EBEF2A26DF5211E9FADA; ui-tabs-1=0; _ga=GA1.1.209123277.1752075474; _ga_6JKEKWMK4R=GS2.1.s1752333686$o7$g1$t1752334715$j60$l0$h0; ASP.NET_SessionId=duvywnxg0ptglmba41bz2lun; AWSALB=p5b2IUeOMx7IqHcoA4H208ubymsk1iEg+P5YxmsXlVyaRtfvdgY/2N/Gnl8J4NOe5lC0B0FMF7jyZxgK2cYJtKHlMS7A5egCJf1Mcttn9CDGudv1ZFmnIX6wbakR; AWSALBCORS=p5b2IUeOMx7IqHcoA4H208ubymsk1iEg+P5YxmsXlVyaRtfvdgY/2N/Gnl8J4NOe5lC0B0FMF7jyZxgK2cYJtKHlMS7A5egCJf1Mcttn9CDGudv1ZFmnIX6wbakR'

curl 'https://drill.gghc.com/extras/api/rcp/get-payment-requests.aspx?emp_id=154&period_id=202506' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b "$SESSION_COOKIES" \
  -H 'priority: u=1, i' \
  -H 'referer: https://drill.gghc.com/rcp.html' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' > payment_requests.json


curl 'https://drill.gghc.com/extras/api/rcp/update-payment-request.aspx?emp_id=154&id=85360&split=0.1&producerApproved_fl=true&producerRejected_fl=false' \
  -X 'POST' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -b "$SESSION_COOKIES" \
  -H 'origin: https://drill.gghc.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://drill.gghc.com/rcp.html' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' > approval_json.json


curl 'https://drill.gghc.com/extras/api/rcp/get-payments-ytd.aspx?emp_id=154&period_id=202506' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b "$SESSION_COOKIES" \
  -H 'priority: u=1, i' \
  -H 'referer: https://drill.gghc.com/rcp.html' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' > payments_ytd.json
