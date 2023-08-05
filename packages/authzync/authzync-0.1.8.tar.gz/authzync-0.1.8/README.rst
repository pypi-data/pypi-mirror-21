.. code-block:: bash
  
   ______     __  __     ______   __  __     ______     __  __     __   __     ______    
  /\  __ \   /\ \/\ \   /\__  _\ /\ \_\ \   /\___  \   /\ \_\ \   /\ "-.\ \   /\  ___\   
  \ \  __ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/  /__  \ \____ \  \ \ \-.  \  \ \ \____  
   \ \_\ \_\  \ \_____\    \ \_\  \ \_\ \_\   /\_____\  \/\_____\  \ \_\\"\_\  \ \_____\ 
    \/_/\/_/   \/_____/     \/_/   \/_/\/_/   \/_____/   \/_____/   \/_/ \/_/   \/_____/ 
                                                                                      
  

- Supports LDAP & local users.
- Follows nested groups.
- Compatible with Python 2 and 3.


Installation
------------

**git**

.. code-block:: bash
  
  $ pypi install ldap3
  $ git clone https://github.com/rbw0/authzync.git  
  
**pypi**

.. code-block:: bash

  $ pypi install authzync


Usage example
-------------

Perform a sync of the LDAP directory specified in ``authzync.json``, get non-LDAP permissions from ``local_db.json`` and write results to ``svn_authz.txt``

.. code-block:: bash

  $ python authzync.py --config authzync.json --local_db local_db.json --authz svn_authz.txt


Configuration
-------------

**Authzync config (--config)**
Configures LDAP, mappings, parse rules, logging etc


 | Example
 | https://github.com/rbw0/authzync/blob/master/examples/authzync.json



**Local users (--local_db)** 
Can be used to set repository permissions for users not present in the LDAP directory, i.e. local users.


 | Example
 | https://github.com/rbw0/authzync/blob/master/examples/local_db.json



How it works
------------
1. Authzync starts by looking for groups matching the ``patterns.access_pattern`` in ``ldap.base_dn``

  Note that there's only one required part in the group name: ``repo_access`` (**RO** or **RW**). This tells authzync which permission to apply to members of this group.
   
2. Next, the value of the attribute set in ``mappings.section_name`` is parsed according to ``patterns.section_pattern``
3. Finally, a list of members is fetched and the authz file generated.


Example
-------

**Authzync config**

========================  ===========================
Name                      Value
========================  ===========================
ldap.base_dn              ou=SVN,dc=example,dc=com
mappings.section_name     description
patterns.access_pattern   ^svn_.*_(?P<repo_access>RO|RW)$
patterns.section_pattern  ^(?P<repo_name>.*):(?P<repo_path>\/.*)
========================  ===========================

**...and...**

**LDAP directory**

=====================  ===========================  ===========================
Group name             ``description`` value        Members
=====================  ===========================  ===========================
svn_repo1-trunk_ro     repo1:/trunk                 user1, user2
svn_repo2-branches_ro  repo2:/branches              user1, user3
svn_repo1_rw           repo1:/                      user3
=====================  ===========================  ===========================


**Should result in**::

  [repo1:/trunk]
  user1 = r
  user2 = r
  
  [repo2:/branches]
  user1 = r
  user3 = r
  
  [repo1:/]
  user3 = rw


Author
------
Created by Robert Wikman <rbw@vault13.org> in 2017


