**craft ai** API python client
==============================

|PyPI| |Build Status| |License| |python|

`**craft ai** *AI-as-a-service* <http://craft.ai>`__ enables developers
to create Apps and Things that adapt to each user. To go beyond useless
dashboards and spammy notifications, **craft ai** learns how users
behave to automate recurring tasks, make personalized recommendations,
or detect anomalies.

Get Started!
------------

0 - Signup
~~~~~~~~~~

If you're reading this you are probably already registered with **craft
ai**, if not, head to
```https://beta.craft.ai/signup`` <https://beta.craft.ai/signup>`__.

    🚧 **craft ai** is currently in private beta, as such we validate
    accounts, this step should be quick.

1 - Create a project
~~~~~~~~~~~~~~~~~~~~

Once your account is setup, let's create your first **project**! Go in
the 'Projects' tab in the **craft ai** control center at
```https://beta.craft.ai/projects`` <https://beta.craft.ai/settings>`__,
and press **Create a project**.

Once it's done, you can click on your newly created project to retrieve
its tokens. There are two types of tokens: **read** and **write**.
You'll need the **write** token to create, update and delete your agent.

2 - Setup
~~~~~~~~~

Install
^^^^^^^

`PIP <https://pypi.python.org/pypi/pip/>`__ / `PyPI <https://pypi.python.org/pypi>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's first install the package from pip.

.. code:: sh

    pip install --upgrade craft-ai

Then import it in your code

.. code:: python

    from craftai import client as craftai

Initialize
^^^^^^^^^^

.. code:: python

    config = {
        "token": "{token}"
    }
    client = craftai.CraftAIClient(config)

3 - Create an agent
~~~~~~~~~~~~~~~~~~~

**craft ai** is based on the concept of **agents**. In most use cases,
one agent is created per user or per device.

An agent is an independent module that stores the history of the
**context** of its user or device's context, and learns which
**decision** to take based on the evolution of this context in the form
of a **decision tree**.

In this example, we will create an agent that learns the **decision
model** of a light bulb based on the time of the day and the number of
people in the room. In practice, it means the agent's context have 4
properties:

-  ``peopleCount`` which is a ``continuous`` property,
-  ``timeOfDay`` which is a ``time_of_day`` property,
-  ``timezone``, a property of type ``timezone`` needed to generate
   proper values for ``timeOfDay`` (cf. the `context properties type
   section <#context-properties-types>`__ for further information),
-  and finally ``lightbulbState`` which is an ``enum`` property that is
   also the output.

.. code:: python

    agent_id = "my_first_agent"
    configuration = {
        "context": {
            "peopleCount": {
                "type": "continuous"
            },
            "timeOfDay": {
                "type": "time_of_day"
            },
            "timezone": {
                "type": "timezone"
            },
            "lightbulbState": {
                "type": "enum"
            }
        },
        "output": ["lightbulbState"]
    }

    agent = client.create_agent(configuration, agent_id)
    print("Agent", agent["id"], "has successfully been created")

Pretty straightforward to test! Open
```https://beta.craft.ai/inspector`` <https://beta.craft.ai/inspector>`__,
select you project and your agent is now listed.

Now, if you run that a second time, you'll get an error: the agent
``'my_first_agent'`` is already existing. Let's see how we can delete it
before recreating it.

.. code:: python

    agent_id = "my_first_agent"
    client.delete_agent(agent_id)
    print("Agent", agent_id, "no longer exists")

    configuration = ...
    agent = client.create_agent(configuration, agent_id)
    print("Agent", agent["id"], "has successfully been created")

*For further information, check the `'create agent' reference
documentation <#create>`__.*

4 - Add context operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

We have now created our first agent but it is not able to do much, yet.
To learn a decision model it needs to be provided with data, in **craft
ai** these are called context operations.

In the following we add 8 operations:

#. The initial one sets the initial state of the agent, on July 25 2016
   at 5:30, in Paris, nobody is there and the light is off;
#. At 7:02, someone enters the room the light is turned on;
#. At 7:15, someone else enters the room;
#. At 7:31, the light is turned off;
#. At 8:12, everyone leaves the room;
#. At 19:23, 2 persons enter the room;
#. At 22:35, the light is turned on;
#. At 23:06, everyone leaves the room and the light is turned off.

.. code:: python

    agent_id = "my_first_agent"
    client.delete_agent(agent_id)
    print("Agent", agent_id, "no longer exists")

    configuration = ...
    agent = client.create_agent(configuration, agent_id)
    print("Agent", agent["id"], "has successfully been created")

    context_list = [
        {
            "timestamp": 1469410200,
            "context": {
                "timezone": "+02:00",
                "peopleCount": 0,
                "lightbulbState": "OFF"
            }
        },
        {
            "timestamp": 1469415720,
            "context": {
                "peopleCount": 1,
                "lightbulbState": "ON"
            }
        },
        {
            "timestamp": 1469416500,
            "context": {
                "peopleCount": 2
            }
        },
        {
            "timestamp": 1469417460,
            "context": {
                "lightbulbState": "OFF"
            }
        },
        {
            "timestamp": 1469419920,
            "context": {
                "peopleCount": 0
            }
        },
        {
            "timestamp": 1469460180,
            "context": {
                "peopleCount": 2
            }
        },
        {
            "timestamp": 1469471700,
            "context": {
                "lightbulbState": "ON"
            }
        },
        {
            "timestamp": 1469473560,
            "context": {
                "peopleCount": 0
            }
        }
    ]
    client.add_operations(agent_id, context_list)
    print("Successfully added initial operations to agent", agent_id, "!")

In real-world applications, you'll probably do the same kind of things
when the agent is created and then, regularly throughout the lifetime of
the agent with newer data.

*For further information, check the `'add context operations' reference
documentation <#add-operations>`__.*

5 - Compute the decision tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The agent has acquired a context history, we can now compute a decision
tree from it! A decision tree models the output, allowing us to estimate
what the output would be in a given context.

The decision tree is computed at a given timestamp, which means it will
consider the context history from the creation of this agent up to this
moment. Let's first try to compute the decision tree at midnight on July
26, 2016.

.. code:: python

    agent_id = "my_first_agent"

    client.delete_agent(agent_id)
    print("Agent", agent_id, "no longer exists")

    configuration = ...
    agent = client.create_agent(configuration, agent_id)
    print("Agent", agent["id"], "has successfully been created")

    context_list = ...
    client.add_operations(agent_id, context_list)
    print("Successfully added initial operations to agent", agent_id, "!")

    decision_tree = client.get_decision_tree(agent_id, 1469476800)
    print("The full decision tree at timestamp", dt_timestamp, "is the following:")
    print(decision_tree)
    """ Outputed tree is the following
      {
        "_version": "1.0.0",
        "configuration": {
          "context": {
            "peopleCount": {
              "type": "continuous"
            },
            "timeOfDay": {
              "type": "time_of_day",
              "is_generated": true
            },
            "timezone": {
              "type": "timezone"
            },
            "lightbulbState": {
              "type": "enum"
            }
          },
          "output": [
            "lightbulbState"
          ],
          "time_quantum": 600,
          "learning_period": 108000
        },
        "trees": {
          "lightbulbState": {
            "children": [
              {
                "children": [
                  {
                    "children": [
                      {
                        "confidence": 0.9545537233352661,
                        "decision_rule": {
                          "operator": "continuous.lessthan",
                          "operand": 1,
                          "property": "peopleCount"
                        },
                        "predicted_value": "OFF"
                      },
                      {
                        "confidence": 0.8630361557006836,
                        "decision_rule": {
                          "operator": ">=",
                          "operand": 1,
                          "property": "peopleCount"
                        },
                        "predicted_value": "ON"
                      }
                    ],
                    "decision_rule": {
                      "operator": "<",
                      "operand": 5.666666507720947,
                      "property": "timeOfDay"
                    }
                  },
                  {
                    "confidence": 0.9947378635406494,
                    "decision_rule": {
                      "operator": ">=",
                      "operand": 5.666666507720947,
                      "property": "timeOfDay"
                    },
                    "predicted_value": "OFF"
                  }
                ],
                "decision_rule": {
                  "operator": "<",
                  "operand": 20.66666603088379,
                  "property": "timeOfDay"
                }
              },
              {
                "confidence": 0.8630361557006836,
                "decision_rule": {
                  "operator": ">=",
                  "operand": 20.66666603088379,
                  "property": "timeOfDay"
                },
                "predicted_value": "ON"
              }
            ],
          }
        }
      ]
      """

Try to retrieve the tree at different timestamps to see how it gradually
learns from the new operations. To visualize the trees, use the
`inspector <https://beta.craft.ai/inspector>`__!

*For further information, check the `'compute decision tree' reference
documentation <#compute>`__.*

6 - Take a decision
~~~~~~~~~~~~~~~~~~~

Once the decision tree is computed it can be used to take a decision. In
our case it is basically answering this type of question: "What is the
anticipated **state of the lightbulb** at 7:15 if there are 2 persons in
the room ?".

.. code:: python

    agent_id = "my_first_agent"

    client.delete_agent(agent_id)
    print("Agent", agent_id, "no longer exists")

    configuration = ...
    agent = client.create_agent(configuration, agent_id)
    print("Agent", agent["id"], "has successfully been created")

    context_list = ...
    client.add_operations(agent_id, context_list)
    print("Successfully added initial operations to agent", agent_id, "!")

    decision_tree = client.get_decision_tree(agent_id, 1469476800)
    print("The decision tree at timestamp", dt_timestamp, "is the following:")
    print(decision_tree)

    context = {
        "timezone": "+02:00",
        "timeOfDay": 7.25,
        "peopleCount": 2
    }
    resp = client.decide(decision_tree, context)
    print("The anticipated lightbulb state is:", resp["output"]["lightbulbState"]["predicted_value"])

*For further information, check the `'take decision' reference
documentation <#take-decision>`__.*

Python starter kit
~~~~~~~~~~~~~~~~~~

If you prefer to get started from an existing code base, the official
Python starter kit can get you there! Retrieve the sources locally and
follow the "readme" to get a fully working **Wellness Coach** example
using *real-world* data.

    `📦 *Get the **craft ai** Python Starter
    Kit* <https://github.com/craft-ai/craft-ai-starterkit-python>`__

API
---

Project
~~~~~~~

**craft ai** agents belong to **projects**. In the current version, each
identified users defines a owner and can create projects for themselves,
in the future we will introduce shared projects.

Configuration
~~~~~~~~~~~~~

Each agent has a configuration defining:

-  the context schema, i.e. the list of property keys and their type (as
   defined in the following section),
-  the output properties, i.e. the list of property keys on which the
   agent takes decisions,

    ⚠️ In the current version, only one output property can be provided.

-  the ``time_quantum`` is the minimum amount of time, in seconds, that
   is meaningful for an agent; context updates occurring faster than
   this quantum won't be taken into account. As a rule of thumb, you
   should always choose the largest value that seems right and reduce
   it, if necessary, after some tests.
-  the ``learning_period`` is the maximum amount of time, in seconds,
   that matters for an agent; the agent's decision model can ignore
   context that is older than this duration. You should generally choose
   the smallest value that fits this description.

    ⚠️ if no time\_quantum is specified, the default value is 600.

    ⚠️ if no learning\_period is specified, the default value is 15000
    time quantums.

Context properties types
^^^^^^^^^^^^^^^^^^^^^^^^

Base types: ``enum`` and ``continuous``
'''''''''''''''''''''''''''''''''''''''

``enum`` and ``continuous`` are the two base **craft ai** types:

-  ``enum`` properties can take any string value;
-  ``continuous`` properties can take any real number value.

    ⚠️ the absolute value of a ``continuous`` property must be less than
    1020.

Time types: ``timezone``, ``time_of_day``, ``day_of_week``, ``day_of_month`` and ``month_of_year``
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

**craft ai** defines the following types related to time:

-  ``time_of_day`` properties can take any real number belonging to
   **[0.0; 24.0[**
   representing the number of hours in the day since midnight (e.g. 13.5
   means
   13:30),
-  ``day_of_week`` properties can take any integer belonging to **[0,
   6]**, each
   value represents a day of the week starting from Monday (0 is Monday,
   6 is
   Sunday).
-  ``day_of_month`` properties can take any integer belonging to **[1,
   31]**, each value represents a day of the month.
-  ``month_of_year`` properties can take any integer belonging to **[1,
   12]**, each value represents a month of the year.
-  ``timezone`` properties can take string values representing the
   timezone as an
   offset from UTC, the expected format is **±[hh]:[mm]** where ``hh``
   represent the
   hour and ``mm`` the minutes from UTC (eg. ``+01:30``)), between
   ``-12:00`` and
   ``+14:00``.

    | ℹ️ By default, the values of the ``time_of_day`` and
      ``day_of_week``
    | properties are generated from the ```timestamp`` <#timestamp>`__
      of an agent's
    | state and the agent's current ``timezone``. Therefore, whenever
      you use generated
    | ``time_of_day`` and/or ``day_of_week`` in your configuration, you
      **must** provide a
    | ``timezone`` value in the context. There can only be one
      ``timezone`` property.

    | If you wish to provide their values manually, add
      ``is_generated: false`` to the
    | time types properties in your configuration. In this case, since
      you provide the values, the
    | ``timezone`` property is not required, and you must update the
      context whenever
    | one of these time values changes in a way that is significant for
      your system.

Examples
''''''''

| Let's take a look at the following configuration. It is designed to
  model the **color**
| of a lightbulb (the ``lightbulbColor`` property, defined as an output)
  depending
| on the **outside light intensity** (the ``lightIntensity`` property),
  the **time
  of the day** (the ``time`` property) and the **day of the week** (the
  ``day``
| property).

| ``day`` and ``time`` values will be generated automatically, hence the
  need for
| ``timezone``, the current Time Zone, to compute their value from given
| ```timestamps`` <#timestamp>`__.

| The ``time_quantum`` is set to 100 seconds, which means that if the
  lightbulb
| color is changed from red to blue then from blue to purple in less
  that 1
| minutes and 40 seconds, only the change from red to purple will be
  taken into
| account.

| The ``learning_period`` is set to 108 000 seconds (one month) , which
  means that
| the state of the lightbulb from more than a month ago can be ignored
  when learning
| the decision model.

.. code:: json

    {
      "context": {
          "lightIntensity":  {
            "type": "continuous"
          },
          "time": {
            "type": "time_of_day"
          },
          "day": {
            "type": "day_of_week"
          },
          "timezone": {
            "type": "timezone"
          },
          "lightbulbColor": {
              "type": "enum"
          }
      },
      "output": ["lightbulbColor"],
      "time_quantum": 100,
      "learning_period": 108000
    }

| In this second example, the ``time`` property is not generated, no
  property of
| type ``timezone`` is therefore needed. However values of ``time`` must
  be manually
| provided continuously.

.. code:: json

    {
      "context": {
        "time": {
          "type": "time_of_day",
          "is_generated": false
        },
        "lightIntensity":  {
            "type": "continuous"
        },
        "lightbulbColor": {
            "type": "enum"
        }
      },
      "output": ["lightbulbColor"],
      "time_quantum": 100,
      "learning_period": 108000
    }

Timestamp
~~~~~~~~~

**craft ai** API heavily relies on ``timestamps``. A ``timestamp`` is an
instant represented as a `Unix
time <https://en.wikipedia.org/wiki/Unix_time>`__, that is to say the
amount of seconds elapsed since Thursday, 1 January 1970 at midnight
UTC. In most programming languages this representation is easy to
retrieve, you can refer to `**this
page** <https://github.com/techgaun/unix-time/blob/master/README.md>`__
to find out how.

``craftai.time``
^^^^^^^^^^^^^^^^

The ``craftai.time.Time`` class facilitates the handling of time types
in **craft ai**. It is able to extract the different **craft ai**
formats from various *datetime* representations, thanks to
`datetime <https://docs.python.org/3.5/library/datetime.html>`__.

.. code:: python

    from craftai.time import Time

    # From a unix timestamp and an explicit UTC offset
    t1 = Time(1465496929, "+10:00")

    # t1 == {
    #   utc: "2016-06-09T18:28:49.000Z",
    #   timestamp: 1465496929,
    #   day_of_week: 4,
    #   time_of_day: 4.480277777777778,
    #   timezone: "+10:00"
    # }

    # From a unix timestamp and using the local UTC offset.
    t2 = Time(1465496929)

    # Value are valid if in Paris !
    # t2 == {
    #   utc: "2016-06-09T18:28:49.000Z",
    #   timestamp: 1465496929,
    #   day_of_week: 3,
    #   time_of_day: 20.480277777777776,
    #   timezone: "+02:00"
    # }

    # From a ISO 8601 string. Note that here it should not have any ":" in the timezone part
    t3 = Time("1977-04-22T01:00:00-0500")

    # t3 == {
    #   utc: "1977-04-22T06:00:00.000Z",
    #   timestamp: 230536800,
    #   day_of_week: 4,
    #   time_of_day: 1,
    #   timezone: "-05:00"
    # }

    # Retrieve the current time with the local UTC offset
    now = Time()

    # Retrieve the current time with the given UTC offset
    nowP5 = Time(timezone="+05:00")

Agent
~~~~~

Create
^^^^^^

Create a new agent, and create its `configuration <#configuration>`__.

.. code:: python

    client.create_agent(
        { # The configuration
            "context": {
              "peopleCount": {
                "type": "continuous"
              },
              "timeOfDay": {
                "type": "time_of_day"
              },
              "timezone": {
                "type": "timezone"
              },
              "lightbulbState": {
                "type": "enum"
              }
            },
            "output": [ "lightbulbState" ],
            "time_quantum": 100,
            "learning_period": 108000
        },
        "impervious_kraken", # id for the agent, if undefined a random id is generated

Delete
^^^^^^

.. code:: python

    client.delete_agent(
        "impervious_kraken" # The agent id
    )

Retrieve
^^^^^^^^

.. code:: python

    client.get_agent(
        "impervious_kraken" # The agent id
    )

List
^^^^

.. code:: python

    client.list_agents()
    # Return a list of agents' name
    # Example: [ "impervious_kraken", "joyful_octopus", ... ]

Create and retrieve shared url
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Create and get a shareable url to view an agent tree.
| Only one url can be created at a time.

.. code:: python

    client.get_shared_agent_inspector_url(
        "impervious_kraken", # The agent id.
        1464600256 # optional, the timestamp for which you want to inspect the tree.
    )

Delete shared url
^^^^^^^^^^^^^^^^^

| Delete a shareable url.
| The previous url cannot access the agent tree anymore.

.. code:: python

    client.delete_shared_agent_inspector_url(
        'impervious_kraken' # The agent id.
    )

Context
~~~~~~~

Add operations
^^^^^^^^^^^^^^

.. code:: python

    client.add_operations(
        "impervious_kraken", # The agent id
        [ # The list of context operations
            {
                "timestamp": 1469410200,
                "context": {
                    "timezone": "+02:00",
                    "peopleCount": 0,
                    "lightbulbState": "OFF"
                }
            },
            {
                "timestamp": 1469415720,
                "context": {
                    "peopleCount": 1,
                    "lightbulbState": "ON"
                }
            },
            {
                "timestamp": 1469416500,
                "context": {
                    "peopleCount": 2
                }
            },
            {
                "timestamp": 1469417460,
                "context": {
                    "lightbulbState": "OFF"
                }
            },
            {
                "timestamp": 1469419920,
                "context": {
                    "peopleCount": 0
                }
            },
            {
                "timestamp": 1469460180,
                "context": {
                    "peopleCount": 2
                }
            },
            {
                "timestamp": 1469471700,
                "context": {
                    "lightbulbState": "ON"
                }
            },
            {
                "timestamp": 1469473560,
                "context": {
                    "peopleCount": 0
                }
            }
        ]
    )

List operations
^^^^^^^^^^^^^^^

.. code:: python

    client.get_operations_list(
        "impervious_kraken" # The agent id
    )

Retrieve state
^^^^^^^^^^^^^^

.. code:: python

    client.get_context_state(
        "impervious_kraken", # The agent id
        1469473600 # The timestamp at which the context state is retrieved
    )

Decision tree
~~~~~~~~~~~~~

Decision trees are computed at specific timestamps, directly by **craft
ai** which learns from the context operations
`added <#add-operations>`__ throughout time.

When you `compute <#compute>`__ a decision tree, **craft ai** returns an
object containing:

-  the **API version**
-  the agent's configuration as specified during the agent's
   `creation <#create-agent>`__
-  the tree itself as a JSON object:

-  Internal nodes are represented by a ``"decision_rule"`` object and a
   ``"children"`` array. The first one, contains the ``"property``, and
   the ``"property"``'s value, to decide which child matches a context.
-  Leaves have a ``"predicted_value"``, ``"confidence"`` and
   ``"decision_rule"`` object for this value, instead of a
   ``"children"`` array. ``"predicted_value``" is an estimation of the
   output in the contexts matching the node. ``"confidence"`` is a
   number between 0 and 1 that indicates how confident **craft ai** is
   that the output is a reliable prediction. When the output is a
   numerical type, leaves also have a ``"standard_deviation"`` that
   indicates a margin of error around the ``"predicted_value"``.
-  The root only contains a ``"children"`` array.

Compute
^^^^^^^

.. code:: python

    client.get_decision_tree(
        "impervious_kraken", # The agent id
        1469473600 # The timestamp at which the decision tree is retrieved
    )

Take Decision
^^^^^^^^^^^^^

To get a chance to store and reuse the decision tree, use
``get_decision_tree`` and use ``decide``, a simple function evaluating a
decision tree offline.

.. code:: python

    tree = { ... } # Decision tree as retrieved through the craft ai REST API

    # Compute the decision on a fully described context
    decision = client.decide(
        tree,
        { # The context on which the decision is taken
            "timezone": "+02:00",
            "timeOfDay": 7.5,
            "peopleCount": 3
        }
    )

    # Or Compute the decision on a context created from the given one and filling the
    # `day_of_week`, `time_of_day` and `timezone` properties from the given `Time`

    decision = client.decide(
      tree,
      {
        "timezone": "+02:00",
        "peopleCount": 3
      },
      craftai.time.Time("2010-01-01T07:30:30")
    )

A computed ``decision`` on an ``enum`` output type would look like:

.. code:: python

    {
      "context": { # In which context the decision was taken
        "timezone": "+02:00",
        "timeOfDay": 7.5,
        "peopleCount": 3
      },
      "output": { # The decision itself
        "lightbulbState": {
          "predicted_value": "ON"
          "confidence": 0.9937745256361138, # The confidence in the decision
          "decision_rules": [ # The ordered list of decision_rules that were validated to reach this decision
            {
              "property": "timeOfDay",
              "operator": ">=",
              "operand": 6
            },
            {
              "property": "peopleCount",
              "operator": ">=",
              "operand": 2
            }
          ]
        },
      }
    }

A ``decision`` for a numerical output type would look like:

.. code:: python

      "output": {
        "lightbulbIntensity": {
          "predicted_value": 10.5,
          "standard_deviation": 1.25, // For numerical types, this field is returned in decisions.
          "decision_rules": [ ... ],
          "confidence": ...
        }
      }

A ``decision`` in a case where the tree cannot make a prediction:

.. code:: python

      "output": {
        "lightbulbState": {
          "predicted_value": None,
          "confidence": 0 // Zero confidence if the decision is null
          "decision_rules": [ ... ]
        }
      }

Error Handling
~~~~~~~~~~~~~~

When using this client, you should be careful wrapping calls to the API
with ``try/except`` blocks, in accordance with the
`EAFP <https://docs.python.org/3/glossary.html#term-eafp>`__ principle.

The **craft ai** python client has its specific exception types, all of
them inheriting from the ``CraftAIError`` type.

| All methods which have to send an http request (all of them except
  ``decide``) may raise either of these exceptions:
  ``CraftAINotFoundError``, ``CraftAIBadRequestError``,
  ``CraftAICredentialsError`` or ``CraftAIUnknownError``.
| The ``decide`` method should only raise ``CrafAIDecisionError`` type
  of exceptions.

.. |PyPI| image:: https://img.shields.io/pypi/v/craft-ai.svg?style=flat-square
   :target: https://pypi.python.org/pypi?:action=display&name=craft-ai
.. |Build Status| image:: https://img.shields.io/travis/craft-ai/craft-ai-client-python/master.svg?style=flat-square
   :target: https://travis-ci.org/craft-ai/craft-ai-client-python
.. |License| image:: https://img.shields.io/badge/license-BSD--3--Clause-42358A.svg?style=flat-square
   :target: LICENSE
.. |python| image:: https://img.shields.io/pypi/pyversions/craft-ai.svg?style=flat-square
   :target: https://pypi.python.org/pypi?:action=display&name=craft-ai


