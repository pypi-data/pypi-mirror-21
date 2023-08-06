robobrowserquery
~~~~~~~~~~~~~~~~

PyQuery on RoboBrowser

RoboBrowser: https://github.com/jmcarp/robobrowser

PyQuery: https://pythonhosted.org/pyquery/


install
=======

pip install robobrowserquery



How to use
==========

::

    from robobrowserquery import RoboBrowserQuery

    browser = RoboBrowserQuery()

    browser.open('https://www.mangazenkan.com/')

    f = browser.get_form()
    f['name'].value = 'Tokyo'
    browser.submit_form(f)

    print(browser.query('title').text())
    for a in browser.query('a').items():
        print(a.attr('href'))
