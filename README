Python Selenese translator
--------------------------

Selenium IDE lets you create Selenium tests in specially structured HTML (or
"Selenese"). These can be easily run on your local machine but do not lend
themselves to being run on a server via e.g. Selenium RC.

This dynamically translates suites of Selenese tests into Python
unittest.TestCase classes, which can then be run using Selenium RC within 
the standard Python unit testing framework and using the Python Selenium 
bindings.


= Warning =

This code is still under construction. It might break randomly and does not 
currently support more than a fraction of Selenese keywords. If you'd like to
improve its behaviour then please add more methods to the class in mapper.py
to map Selenese keywords to Python-binding API calls.


= Setup =

1. Download Selenium RC http://seleniumhq.org/download/

2. Unpack the server JAR at selenium-server-X/selenium-server.jar and run it
in the background:

 java -jar selenium-server.jar

3. Check out this repository anywhere on your filesystem.

4. Unpack the Python bindings selenium-python-client-driver-X/selenium.py 
from Selenium RC and place it within this repository


= Execution =

Assuming your Selenese test suite is saved as ~/my-tests/index.html (with all 
the separate test files within ~/my-tests/ too) you can run the following at 
a command prompt:

 python main.py ~/my-tests [selenium-server]

The server defaults to "localhost"

Alternatively you can run Selenese tests alongside your other unittest test
cases using e.g:

 class OneTest(unittest.TestCase):
     # ...

 class TwoTest(unittest.TestCase):
     # ...

 ThreeTest = selenese.convert_selenese(directory_name, root_url)

This creates a ThreeTest class, just like a OneTest and TwoTest, which 
unittest will pick up on and run. Selenium IDE tests require a root_url, as
they all run within the same domain owing to browser security restrictions.
This is not encoded within the tests as it is assumed that the tests are to
be run off the same domain as the website under test.


= Testing =

PySelenese can itself be tested and contains its own internal test suite. Run:

 python test.py [selenium-server]

This should run near-silently as per a normal unittest run. Alternatively, 
tests can be run in debug mode with e.g:

 python test.py localhost debug

You should then see some debug messages, both from the conversion process and
from the tests themselves, but no failures.


= Known issues =

The main issue is that not all of Selenium's test syntax has been transcribed
in mapper.py yet. Please let me know if your tests fail on a particular 
Selenium keyword; alternatively, feel free to fork the github repository and 
add the mapping yourself.

 http://github.com/jpstacey/PySelenese
