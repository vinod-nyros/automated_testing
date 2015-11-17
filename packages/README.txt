10/27/13 Sun JJW

let's slowly migrate this "packages" dir to be for forked-packages, and on the path -

Anything installable via normal pip (even non-forked github installs) should go in requirements.txt

# ...

# actually, let's try even using the requirements.txt for forked ones, too - I did it with bread-and-pepper


# OLD:
#git clone https://github.com/bitmazk/django-cms-html5-1140px-boilerplate.git
#git clone https://github.com/mike360/django-html5-boilerplate.git
#git clone https://github.com/HowlingEverett/django-html5boilerplate.git
#git clone https://github.com/matthewwithanm/django-html5boilerplate.git django-html5boilerplate2

git clone git://github.com/h5bp/html5-boilerplate.git
git clone https://github.com/zurb/foundation.git

        # JJW Apr 2012 for django-eRacks
        pip install $v django-ide
        pip install $v django-dbtemplates
        pip install $v hg+https://bitbucket.org/offline/django-annoying
        #pip install $v hamlpy
        pip install $v pisa
        pip install $v django-aloha
        pip install $v django_codemirror

