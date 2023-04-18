
## Sample Python App

This is a basic Python application, used in a number of AWS tutorials, that focus on various ways to deploy it. It is a simple application that allows the user to sign up for a new startup.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

This app is written in Python, and can be deployed on an `Ubuntu 20.04` instance with the following commands:
~~~
apt-get update
apt-get install -y --no-install-recommends build-essential python3 python3-pip python3-dev nginx uwsgi-core
pip3 install pipenv
cp nginx-app.conf /etc/nginx/conf.d/

# App is now ready to run using the script:
./start.sh
~~~
