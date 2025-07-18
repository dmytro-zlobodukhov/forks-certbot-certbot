import os
import sys

from setuptools import find_packages
from setuptools import setup

version = '5.0.0.dev0'

install_requires = [
    # for now, do not upgrade to cloudflare>=2.20 to avoid deprecation warnings and the breaking
    # changes in version 3.0. see https://github.com/certbot/certbot/issues/9938
    'cloudflare>=2.19, <2.20',
]

if os.environ.get('SNAP_BUILD'):
    install_requires.append('packaging')
else:
    install_requires.extend([
        # We specify the minimum acme and certbot version as the current plugin
        # version for simplicity. See
        # https://github.com/certbot/certbot/issues/8761 for more info.
        f'acme>={version}',
        f'certbot>={version}',
    ])

docs_extras = [
    'Sphinx>=1.0',  # autodoc_member_order = 'bysource', autodoc_default_flags
    'sphinx_rtd_theme',
]

test_extras = [
    'pytest',
]

setup(
    name='certbot-dns-cloudflare',
    version=version,
    description="Cloudflare DNS Authenticator plugin for Certbot",
    url='https://github.com/certbot/certbot',
    author="Certbot Project",
    author_email='certbot-dev@eff.org',
    license='Apache License 2.0',
    python_requires='>=3.9.2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'docs': docs_extras,
        'test': test_extras,
    },
    entry_points={
        'certbot.plugins': [
            'dns-cloudflare = certbot_dns_cloudflare._internal.dns_cloudflare:Authenticator',
        ],
    },
)
