noauthsftp
==========

NoAuthSFTP is an anonymous SFTP server that requires no password (or username) 
to connect to. Users will only be able to invoke sftp and navigate around the 
directory specified on the command line

NoAuthSFTP is not for internet facing use and is only intended as a 'quick and 
dirty' to get files off a machine on a secure network

Features
--------
 * 'Quick and dirty' starts up with minimal configuration
 * pseudo chroots to a directory (emulated in software, does not use chroot())
 * Supports multiple key types for server identication (eliptic curve, RSA)
 * Uses asyncio/asyncssh to allow multiple clients to connect at the same time 
   without blocking each other

Use Cases
---------
 * Move files between machines
 * Replace anon ftp 
 * Serve up files while allowing clients to authenticate the server

Installation
------------
It is recommended to install NoAuthSFTP to a virtual environment as follows:

    $ python3.5 -m venv venv
    $ . venv/bin/activate
    # pip install noauthsftp

If you intend to use eliptic curve keys, additional dependeincies will need to 
be pulled in. These can be installed with the following comamnd:

    $ pip install 'asyncssh[bcrypt,libnacl]'

This will pull in all the required dependencies after which the server can be 
run by executing the following command

    $ noauthsftp

Usage
-----
NoAuthSFTP has a fairly comprehensive help command available by executing the 
following:

    $ noauthsftp --help

In order to get noauthsftp running it requires a ssh host key, this is 
identical to a standard public/private key pair but used by the server instead 
(do not reuse it for standard ssh communications). To generate this keypair use 
the following command

    $ ssh-keygen

you will then be prompted for a filename, select a filename such as 
'ssh_server_key' and make note of this, The filename will be used with the '-k' 
option to allow the ssh server to authenticate itself to the client.
