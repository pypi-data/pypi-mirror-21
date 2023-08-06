=====
Emily
=====

Emily is a fully functional chatbot platform built in Python. Emily can be customized and controlled using brain files written in a simple JSON structure, and can also be configured to run your own custom Python code.

Emily does not have incredible abilities out of the box, but is instead meant to give developers of various skill levels an easy-to-configure chatbot that can interact with custom Python code effortlessly.

============

- Python 2.7 or later
- fuzzywuzzy  - Fuzzy string matching
    - Uses python-Levenshtein 
- Flask  - Web Server Microframework in Python

Installation
============

Using PIP

.. code-block:: bash

    $ pip install emily

Usage
=====

Command Line Example:
---------------------

After installing Emily, a new bash command is available for chatting with Emily.

.. code-block:: bash

    $ emily

    User      >  Hello

    Emily     >  Hello!

    User      >  Tell me a joke

    Emily     >  Why did the scarecrow win an award?

    User      >  I don\'t know

    Emily     >  Because he was outstanding in his field...

    User      >  bye

    Emily     >  Bye!

Stateless Emily:
-----------------

Emily saves sessions to disk or to DynamoDB depending on your Configuration Parameters.
Because of this, Emily can run as a stateless application, meaning she does not need to stay running and retain everything in memory.

**Note:** Running Emily as a stateless application does have an negative impact on response times.

.. code-block:: bash

    $ python

    >>> import emily
    >>> response,session_id = emily.stateless(message="Hello")
    >>> print(response,session_id)
    (u'Hey there!',42279)
    >>> response,session_id = emily.stateless(session_id=session_id,message="Tell me a joke")
    >>> print(response,session_id)
    (u'Knock knock',42279)
    >>> response,session_id = emily.stateless(session_id=session_id,message="Who's there?")
    >>> print(response,session_id)
    (u'A pencil',42279)
    >>> response,session_id = emily.stateless(session_id=session_id,message="A pencil who?")
    >>> print(response,session_id)
    (u"Never mind, it's pointless",42279)
    >>> response,session_id = emily.stateless(session_id=session_id,message="quit")
    >>> print(response,session_id)
    (u'Bye!',42279)

In between function calls in the example above, Emily is not running as a background process. At each execution, she loads the brain files (including jokes.yaml) and also references her saved session information which allows her to keep track of where the user is in any given conversation.

Notice that the first call to the emily.stateless() function only contains a message and no session_id. Emily will automatically assign the user a session ID and return it with her response. That session ID remains valid until the user sends a message of "quit", "q", "exit", or "bye".

Emily as a Web Server:
----------------------

Emily uses Flask  to run as a web server and accept HTTP requests.

First start Emily as a web server.

.. code-block:: bash

    $ emily_server
    Web Server Started...

Then, from another terminal window, use HTTP requests to interact with Emily.

.. code-block:: bash

    $ curl http://localhost:5000/get_session
    40113
    $ curl -H "Content-Type: application/json" -X POST -d '{"session_id":"40113","message":"Hello"}' http://localhost:5000/chat
    {"response":"Hello!","session_id":40113}

**URLs:**

- **GET /get_session** - Stores a new set of session variables based on the default session variables and returns a session ID
- **POST /chat** - Send a message to Emily. Request should include a 'session_id' parameter and a 'message' paramter.

Using Custom Code with Emily
----------------------------

The sample brain files included with Emily provide a good introduction to Emily's functionality, but by adding custom Python modules, Emily can learn to have some pretty intelligent conversations and carry out complicated tasks. Here is a sample project that uses Emily's functionality, but provides custom brain files and Python modules.

**Project Structure**

::

  my_module/
    brain/
      my_brain.json
    modules/
      __init__.py
      my_submodule.py
    my_module.py

**Inside my_brain.json**

.. code-block:: json

  {
    "intent": "my_brain",
    "conversations": {
      "default": {
        "when_i_say_this": {
          "node_type": "response",
          "pattern": "when i say this",
          "responses": [
            "You say this"
          ]
        },
        "but_when_i_say_this": {
          "node_type": "simple_logic",
          "pattern": "but when i say this",
          "command": "my_submodule.my_function()",
          "next_node": "print_result"
        },
        "print_result": {
          "node_type": "response",
          "responses": [
            "Run function and print result here: {command_result}"
          ]
        },
        "quit": {
          "node_type": "response",
          "pattern": "quit",
          "utterances": [
            "exit",
            "q",
            "bye"
          ],
          "responses": [
            "Bye!"
          ]
        }
      }
    }
  }

**Inside my_submodule.py**

.. code-block:: python

    import sys,os

    def my_function():
        return "The Result"

**Inside my_module.py**

.. code-block:: python

    from six.moves import input # Python 2 and 3 compatible
    import emily
    import sys
    import os

    def chatbot(chat=None):
        # Array of brain files from my brain directory
        brains = ["brain/my_brain.json"]

        # Append my modules directory to the Python path so that Emily can import my custom code
        sys.path.append(os.path.dirname(os.path.realpath(__file__)),"modules"))

        if chat is None:
            # Get Emily as Flask Application
            application = emily.start_emily(more_brains=brains,more_vars={'foo':'bar'},disable_emily_defaults=True)
            application.run(debug=True,port=5000)
        else:
            # Get Emily Session using Emily() Python Class
            session = emily.Emily(more_brains=brains,more_vars={'foo':'bar'},,disable_emily_defaults=True)
            session_id = session.get_session()
            session.start()

            # Enter while loop for command line chatting
            while True:
                user_input = input("User >  ")
                response,session_id = session.send(message=user_input,session_id=session_id)
                print("\nEmily >  {}\n".format(response))

                # Exit while loop if user enters word for quit
                if user_input.upper() in ['Q','QUIT','EXIT','BYE']:
                    break

    if __name__ == '__main__':
        chatbot(*sys.argv[1:]) if len(sys.argv) > 1 else chatbot()

**Example Run**

.. code-block:: bash

  $ python my_module.py chat
  User >  When I say this

  Emily >  You say this

  User >  but when I say this

  Emily >  Run function and print result here: The Result

  User >  exit

  Emily >  Bye!

Configuration Options
---------------------

All of Emily's configuration paramters can be altered when using the Emily() class or when running Emily as a web server using the start_emily() function.

Configuration parameters include:

- more_brains - Python List of full paths to additional brain files for Emily to consume. **Default:** None
- more_vars - Python Dictionary of additional session variables to add to Emily's default session variables. **Default:** None
- disable_emily_defaults - Boolean controlling whether Emily loads her default brain files or not. **Default:** False

In addition to the paramters above, any paramter contained in the emily/emily_conf/emily_config.yaml can also be passed in to the Emily() class or the start_emily() function. Information on those parameters can be found here: Configuration Parameters

**Example**

.. code-block:: python

    # Example with Emily() Class
    session = emily.Emily(more_brains=['other/brain.json'],disable_emily_defaults=True,logging_level='INFO',emily_port=8001,log_file='/full/path/to/my_log_dir/emily.log')
    session_id = session.get_session()
    session.start()

    # Example with start_emily() function (Flask app)
    application = emily.start_emily(more_vars={'foo':'bar'},logging_level='ERROR',emily_port=8001,source='DYNAMODB',region='us-west-2',session_vars_path='emily-dynamo-table')
    application.run(debug=True)

Releases
--------

1.0.4 (2017-04-11)
++++++++++++++++++

**Bugfixes**

- Emily's default log file is 'emily/log/emily.log', but the empty log directory was not included in the wheel. Added log directory path to MANIFEST.in
- Escaped single quote in README.rst that caused the syntax highlights in the command line example to look off.

1.0.3 (2017-04-07)
++++++++++++++++++

**Improvements**

- Added function to setup.py for removing links in README.rst when creating the long description. PyPI does not display the description properly when there are links.

**Bugfixes**

- Forgot to make "user_input" change to Emily's stateless function in release 1.0.2

1.0.2 (2017-04-07)
++++++++++++++++++

**Improvements**

- Preformat and intent filters (configured through config file) were expecting "user_input" instead of "{user_input}", which was inconsistent with user_input logic in nodes. Now the user's input is always referenced using "{user_input}" no matter where it is referenced.
- Emily has always set user input to lowercase and removed all puncuation before matching it to patterns. Previously, when "{user_input}" was referenced in commands and responses, this formatted version of the input was used. Changed code so that now "{user_input}" is replaced with the raw input of the user, complete with capitalization and punctuation.

1.0.1 (2017-03-27)
++++++++++++++++++

**Bugfixes**

- Previous version of setup.py tried to import emily and reference version, but did so before installing dependencies, so setup.py always failed while installing from PyPI. Changed location of version to setup.py.


1.0.0 (2017-03-27)
++++++++++++++++++

- Initial attempt at releasing Emily to PyPI
- All features specified in README files should be available

