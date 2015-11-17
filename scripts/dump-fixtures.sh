#./manage.py dumpdata obdjects.Snippet --format=yaml >fixtures/obdjects-snippets.yaml
./manage.py dumpdata quickpages.QuickPage --format=yaml --all >fixtures/quickpages-quickpages.yaml
./manage.py dumpdata quickpages.QuickSnippet --format=yaml --all >fixtures/quickpages-quicksnippet.yaml

./manage.py dumpdata customers.CustomerImage --format=yaml --all >fixtures/customers-customerimages.yaml
./manage.py dumpdata customers.Testimonial --format=yaml --all >fixtures/customers-testimonials.yaml
./manage.py dumpdata customers.UserenaProfile --format=yaml --all >fixtures/customers-profiles.yaml
./manage.py dumpdata customers.Address --format=yaml --all >fixtures/customers-addresses.yaml

./manage.py dumpdata bloglets.Category --format=yaml --all >fixtures/bloglets-categories.yaml
./manage.py dumpdata bloglets.Post --format=yaml --all >fixtures/bloglets-posts.yaml

./manage.py dumpdata catax.CaTax --format=yaml --all >fixtures/catax.cataxes.yaml

./manage.py dumpdata home.FeaturedImage --format=yaml --all >fixtures/home-featuredimages.yaml

./manage.py dumpdata products.Categories --format=yaml --all >fixtures/products-categories.yaml
./manage.py dumpdata products.Product --format=yaml --all >fixtures/products-products.yaml
./manage.py dumpdata products.Option --format=yaml --all >fixtures/products-options.yaml
./manage.py dumpdata products.Choice --format=yaml --all >fixtures/products-choices.yaml
./manage.py dumpdata products.Prodopt --format=yaml --all >fixtures/products-prodopts.yaml
./manage.py dumpdata products.Prodoptchoice --format=yaml --all >fixtures/products-prodoptchoices.yaml
./manage.py dumpdata products.ChoiceCategory --format=yaml --all >fixtures/products-choice-categories.yaml
./manage.py dumpdata products.Images --format=yaml --all >fixtures/products-images.yaml
