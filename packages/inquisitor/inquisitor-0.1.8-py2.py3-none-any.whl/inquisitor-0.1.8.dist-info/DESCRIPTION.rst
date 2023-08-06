Inquisitor
==========

| This Python module provides a python wrapper around the API of Inquirim.com.
| For a successful response, API users must provide an authentication. To obtain an authentication token, users can register at inquirim.com.

Installation
------------

Just type:

.. code:: bash

    pip install inquisitor

You can also find `Inquisitor on Github
<https://github.com/inquirim/inquisitor/>`_



Documentation
-------------

The documentation on installation, use and API description is found at econdb.com `documentation page. <https://www.econdb.com/docs/libraries/#python/>`_

Usage example
-------------

.. code:: python

	import inquisitor
	qb = inquisitor.Inquisitor("YOUR_API_KEY")

	### List sources 
	qb.sources()

	### List datasets
	qb.datasets(source='EU')

	### Obtain series data
	qb.series(dataset='EI_BSCO_M')

	### Return the response of any API url in Pandas if it contains time series data and JSON format otherwise
	qb.from_url('https://www.econdb.com/api/series/?ticker=GDPQUS')


