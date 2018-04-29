KUMPARAN REST API

1. CRUD NEWS
	A. CREATE:
		- POST http://127.0.0.1:5002/news with body(x-form-urlencoded) title, content, status, topic
	B. READ:
		- GET http://127.0.0.1:5002/news/{news_id}
		- GET http://127.0.0.1:5002/news?topic={topic_name}&status={status}
		- GET http://127.0.0.1:5002/news?topic={topic_name}
		- GET http://127.0.0.1:5002/news?status={status}
	C. UPDATE:
		- PUT http://127.0.0.1:5002/news/{news_id} with body(x-form-urlencoded) title, content, status, topic
		- PUT http://127.0.0.1:5002/news/{news_id}/{status}
	D. DELETE:
		- DELETE http://127.0.0.1:5002/news/{news_id}

2. CRUD TOPIC
	A. CREATE:
		- POST http://127.0.0.1:5002/topics with body(x-form-urlencoded) name
	B. READ:
		- GET http://127.0.0.1:5002/topics/{topic_id}
		- GET http://127.0.0.1:5002/topics
	C. UPDATE:
		- PUT http://127.0.0.1:5002/topics/{topic_id} with body(x-form-urlencoded) name
	D. DELETE:
		- DELETE http://127.0.0.1:5002/topics/{topic_id}
