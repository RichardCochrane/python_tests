### Selenium IDE

== Introduction ==
Selenium IDE (http://www.seleniumhq.org/projects/ide/) is useful for functional testing of your app. It allows you to record
specific actions and then replay them at will. So if you recorded a signup process, you could replay the macro any number of times
to create that many new users.

== Setting it up ==
Install Selenium IDE (it only runs in Firefox). Due to some issues introduced many years ago, it's still rated as an experimental
add-on in Firefox and you have to add it directly from this page:
https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/

== Creating Selenium Tests ==
To get started creating Selenium tests, simply open the IDE in Firefox and do the following:
- Ensure that the record button is lit (ie. it is recording your actions)
- Go the page that you want to start at (this is important since the test must always start in the same place)
- Start interacting with the page, filling in forms and submitting them - don't worry about making mistakes for now
- Once the basic test has been run to completion, save the test and then go through it and refine it. Add extra checks (verifying titles or page content), remove unnecessary duplication of edits and, if necessary, set the test up to be repeatable. So it it's going to create a user, running the create_user test successfully will result in that user now being in the database. However, running the test again will attempt to create another user with the same details, causing the test to fail. One solution around this is to use the Selenium IDE stored variables plugin and assign a date/time variable that is appended to any fields that should be unique. One value required to assign a date/time to a variable could be:

    javascript{var startTime=new Date().toString().split(&quot; &quot;)[4].split(&quot;:&quot;).join(&quot;&quot;); startTime;}

== Running Selenium Tests ==
Since these don't run in an automated fashion, the Selenium IDE must be opened and the test file (or test suite - a collection of test files) must be opened, the webserver started and then the tests run.

== Benefits ==
* These are very easy to get started with since they get created simply by recording you actually doing something.
* Running tests through Selenium IDE is very visual and with plugins added, they become even easier to run and diagnose issues.
* You can add breakpoints to tests to help diagnose progress or in making changes.

== Limitations ==
* It requires a running webserver to operate against
* It does not run in a headless fashion and so cannot be run on buildservers
* It doesn't rollback database changes from one test to the next and so workarounds must be employed to cater for this.
* It performs as fast as the webserver can process the requests and so it tends to be fairly slow to run the whole test suite.

== Conclusion ==
These are fairly quick to setup and run but only being able to run them on a developer's machine is a serious limitation.
