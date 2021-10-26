from invokes import invoke_http

# invoke book microservice to get all books
results = invoke_http("http://localhost:5000/COURSE")