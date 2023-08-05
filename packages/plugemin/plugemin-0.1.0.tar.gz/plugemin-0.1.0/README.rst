plugemin
========

plugemin is a simple utility which wraps the amazing jinja2 templating engine.

It will look for templates in a series of locations and take a structured
data format as input. It will render the template with each piece of
data.

*Example*

in C:\\plugemin\\templates\\test.j2::

    cp {{src}} {{dst}}
    rm {{src}}

in C:\\tmp\\files.csv::

    src,dst
    /var/log/*,/tmp/.
    /usr/var/log/*,/tmp/.
    /var/www/*,/tmp/.

Then you can use the following command::

    C:\> plugemin -t backup-delete.j2 -d C:\plugemin\files.csv
    cp /var/log/* /tmp/.
    rm /var/log/*
    cp /usr/var/log/* /tmp/.
    rm /usr/var/log/*
    cp /var/www/* /tmp/.
    rm /var/www/*
