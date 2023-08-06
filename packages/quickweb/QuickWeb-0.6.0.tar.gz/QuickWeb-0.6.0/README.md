<p align="center">
<b><a href="#Installing">Installing</a></b>
|
<b><a href="#getting-started">Getting Started</a></b>
|
<b><a href="#features">Features</a></b>
|
<b><a href="#contributing">Contributing</a></b>
</p>

**QuickWeb** is a Rapid Web Development framework targeted for cloud platforms.

## Installing
You should be able to use quickweb on both Windows Linux or Mac, for the sake of simplicity the following instructions assume you will be using a Linux system for development, you will need to adapt for Windows/Mac as required. You must have python and pip installed on your system.


Install quickweb using pip:
```sh
sudo pip install quickweb
```
If the installation is succesful the `quickweb` command will be available, it will allow you to manage quickweb applications from the command line.

## Getting Started
### Creating your first application
Create your first quickweb app using a bootstrap starter template:
```sh
quickweb init my-quickweb-app bootstrap-starter
```
You will get a _my-quickweb-app_ directory containing the a runnable quickweb app with a starter template using Bootstrap's library.

### Changing the application content
Check the application directory using your preferred HTML/CSS/JavaScript editor/IDE, edit the the contents from the `template` and `webroot` directories as desired.

### Starting the application
Once you need to test your application, you can simply start it with:
```sh
quickweb run my-quickweb-app
```
A CherryPy based web server is started using a random port on your local system. You can check your application by browsing to the URL displayed on the app startup information. If you later change some of the HTML/CSS/JS, you will need to refresh the page on your browser.

### Deploying to a cloud platform
When your application is ready for public access you can deploy it to a cloud platform, it has been tested with the following providers:
- Heroku Cloud Application Platform (deploy with: git push heroku master)
- IBM Bluemix (deploy with: cf push appname)
- Other CloudFoundry based provider (deploy with: cf push appname)

It should be able to run from other <a href="https://www.cloudfoundry.org/">CloudFoundry</A> based providers.

NOTES:
 * Check the cloud provider documentation for the web app detailed setup instructions
   - Use the instructions for python web applications setup/deployment
 * The level of support for python based apps will depend on your provider, check it's documentation for details

## Features
QuickWeb is still on an early stage of development, the following are core features:

- Static content serving from restricted/predefined locations (using url mapping)
- HTML files templating support, using <a href="http://docs.makotemplates.org/en/latest/syntax.html">Mako</a>.
    - Extended with HTTP specific functions:
        - Execution context (url; method)
        - Session (get)
        - Cookies (get)
        - TODO: Authentication
        - TODO: Authorization
- Web application server code using the pythonic, object-oriented web framework <a href="http://cherrypy.org/">CherryPy</a>

## Contributing
If you want to contribute developing quickweb, you will need to run it from the source. From the source directory use:
```sh
quickweb/quickweb [arguments...]
```


Developed By
------------

* [MyWasOS Team](//github.com/MyWayOS)

Git repository located at
[github.com/MyWayOS/QuickWeb](//github.com/MyWayOS/QuickWeb)

Project Demo Site:
[quickweb.mywayos.org](//quickweb.mywayos.org)

