# FastAPI based Plotly plot server

This project is an attempt to create a 'plot server' API using plotly and fastapi. The idea is to send a request to the API and receive data back to render a plotly plot!

The first part of this project is the API itself, using fastapi as the backbone. A route will be created and when called, will return a plot back to the caller.

The second part of this project is a web server to render the plot. This will use flask, which will call the API endpoint for the plot then show it on the page.

Eventually, I would like to find how to embed this API call into a React.js web page.