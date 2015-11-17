Global Fixtures
===============

These fitures are primarily for transferring existing known content
back and forth between dev / staging / production.

Many of them may be outdated.

Testing fixtures are generated & kept in the respective apps directories
where they are automatically picked up by the respective tests.

JJW

11/7/15 Done as part of obdject.Snippet to quickpages.QuickSnippets migration:
./manage.py dumpdata --format=yaml obdjects.Snippet >fixtures/quickpages-quicksnippets.yaml
(The fixtures were then modified by had to load back into the new app, quickpages - JJW)
