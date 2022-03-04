# Scale Chart

I got tired of googling guitar scales so I made this to create them for me. It's still a work in progress, plenty of enhancements to come.

Steps to run (assuming you have Docker already installed)

1) Clone this repo
2) Build the image by running ``docker build -t scale_chart .``
3) Start the contained by running ``docker run -p 4545:4545 scale_chart``
4) Open a browser and go to http://localhost:4545/
