import os

os.system("docker image rm scale_chart_image")
os.system("docker build -t scale_chart_image .")
os.system("docker run --rm -p 4545:4545 --name scale_chart scale_chart_image")