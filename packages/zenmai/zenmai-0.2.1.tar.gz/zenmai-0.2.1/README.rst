zenmai
========================================

.. image:: https://travis-ci.org/podhmo/zenmai.svg?branch=master
    :target: https://travis-ci.org/podhmo/zenmai


toylang on yaml or json

command line example
----------------------------------------

main.yaml

.. code-block:: yaml

  code:
    $import: ./filters.py
    as: f
  definitions:
    $let:
      nums: {$load: ./nums.yaml#/definitions/nums0/enum}
    odds:
      type: integer
      enum:
        $f.odds: {$get: nums}
    even:
      type: integer
      enum:
        $f.evens: {$get: nums}

nums.yaml

.. code-block:: yaml

  definitions:
    nums0:
      type: integer
      enum:
        [1, 2, 3, 4, 5, 6]
    nums1:
      type: integer
      enum:
        [1, 2, 3, 5, 7, 11]

filters.py

.. code-block:: python

  def odds(nums):
      return [n for n in nums if n % 2 == 1]
  
  
  def evens(nums):
      return [n for n in nums if n % 2 == 0]

run.

.. code-block:: bash

  $ zenmai examples/readme2/main.yaml

output

.. code-block:: yaml

  zenmai main.yaml
  definitions:
    odds:
      type: integer
      enum:
      - 1
      - 3
      - 5
    even:
      type: integer
      enum:
      - 2
      - 4
      - 6
  

config loader
----------------------------------------

using zenmai as config loader.

.. code-block:: python

  from zenma.loader import load

  with open("config.yaml") as rf:
      d = load(rf)

