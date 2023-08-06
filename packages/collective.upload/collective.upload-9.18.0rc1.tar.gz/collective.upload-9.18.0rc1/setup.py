# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '9.18.0rc1'
description = 'File upload widget for Plone with multiple file selection.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='collective.upload',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='plone jquery upload',
      author='OpenMultimedia',
      author_email='contacto@openmultimedia.biz',
      url='https://github.com/collective/collective.upload',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Acquisition',
          'plone.api >=1.4.11',
          'plone.app.content',
          'plone.app.contentmenu',
          'plone.app.jquery >=1.8.3',
          'plone.app.jquerytools >=1.5.7',
          'plone.app.layout',
          'plone.app.registry',
          'plone.namedfile [blobs]',
          'plone.registry',
          'Products.ATContentTypes',
          'Products.CMFCore',
          'Products.CMFPlone >=4.3,<5.0',
          'Products.GenericSetup',
          'requests',
          'setuptools',
          'zope.component',
          'zope.container',
          'zope.event',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'AccessControl',
              'plone.app.robotframework',
              'plone.app.testing [robot]',
              'plone.browserlayer',
              'plone.testing',
              'robotsuite',
              'transaction',
              'zope.browsermenu',
              'zope.viewlet',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
