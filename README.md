# Scale Chart

I got tired of googling guitar scales so I made this to create them for me. It's still a work in progress, plenty of enhancements to come.

Steps to run (assuming you have Docker already installed)

1) Clone this repo
2) Set the following variables 
  ``export FLASK_APP=scale_chart
    export FLASK_ENV=development``
3) Build the image by running ``docker build -t scale_chart .`` in this directory
4) Start the container by running ``docker run -p 4545:4545 scale_chart``
5) Open a browser and go to http://localhost:4545/
