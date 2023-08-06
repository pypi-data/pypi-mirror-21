=====
Usage
=====

To use Django isNull list_filter in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'isnull_filter.apps.IsnullFilterConfig',
        ...
    )

Add Django isNull list_filter's URL patterns:

.. code-block:: python

    from isnull_filter import urls as isnull_filter_urls


    urlpatterns = [
        ...
        url(r'^', include(isnull_filter_urls)),
        ...
    ]
