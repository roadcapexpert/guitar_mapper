# Scale Chart


Steps to run (assuming you have Docker already installed)

1) Clone this repo
2) Build the image by running ``docker build -t scale_chart_image .`` in this directory
3) Start the container by running ``docker run --rm -p 4545:4545 --name scale_chart scale_chart_image``
4) Open a browser and go to http://localhost:4545/
5) To restart the container run docker_restart.py
