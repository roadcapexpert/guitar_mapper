from setuptools import find_packages, setup

# export FLASK_APP=scale_chart
# export FLASK_ENV=developmentecho $FLASK
setup(
    name="scale_chart",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',

    ],
)
