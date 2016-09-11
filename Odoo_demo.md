## Install Odoo

1. Run the following commands to install the main dependencies:

```
$ sudo apt-get install git python2.7 postgresql nano \
python-virtualenv
```

2. Download and install wkhtmltopdf:

   `$ wget http://nightly.odoo.com/extra/wkhtmltox-0.12.1.2_linux-jessie-amd64.deb`

   `$ sudo dpkg -i wkhtmltox-0.12.1.2_linux-jessie-amd64.deb`

**Caution**

This is a package provided by the Odoo maintainer for Debian Jessie.If you are using another distribution, browse to http://download.gna.org/wkhtmltopdf/0.12/0.12.1/ and download thepackage for your operating system.

3. Now, use this to install the build dependencies:

```
$ sudo apt-get install gcc python2.7-dev libxml2-dev \ libxslt1-dev libevent-dev libsasl2-dev libldap2-dev libpq-dev \
libpng12-dev libjpeg-dev
```

4. Con gure PostgreSQL:

```
$ createuser -d -a -P postgres
$ createdb $(whoami)
```

5. Con gure git:

  ` $ git config --global user.name "Your Name"`
  ` $ git config --global user.email youremail@example.com`

6. Clone the Odoo code base:

```
$ mkdir ~/odoo-dev
$ cd ~/odoo-dev
```

```
// $ git clone -b 9.0 --single-branch https://github.com/odoo/odoo.git (too slow)

$ git clone http://zhengl@git.ersoft.cn/scm/odoo/odoo.git 
$ cd odoo
```

7. Create an odoo-9.0 virtual environment and activate it:

   `$ virtualenv ~/odoo-9.0`

   `$ source ~/odoo-9.0/bin/activate`

8. Install the Python dependencies of Odoo in virtualenv:

   ```
   $ pip install -r requirements.txt
   ```

9. Create and start your  first Odoo instances:

```
$ createdb odoo-test
$ python odoo.py -d odoo-test --addons-path=addons \
 --db-filter=odoo-test$
```

10. Point your browser to [http://localhost:8069](http://localhost:8069) and authenticate using the **admin** account and **admin** as password.



## Start Odoo

1. Simple start

```
$ python odoo.py start
```

2. The Odoo **start** command is a shortcut to *start* a server instance using the current directory.The directory name is automatically used as the *database* name (for the **-d** option), and the current directory is automatically added to the addons path (the **--addons-path** option) as long as it contains an Odoo *addon* module. By default the current directory is used, but the **—path** option allows you to set a *specific path* to use instead. For example, this would work from any directory:

```
$ ~/odoo-dev/odoo/odoo.py start -d odoo_demo --addons-path=addons \
--path=~/odoo-dev/my-odoo
```

3. Set the server *listening port*, use the following command **--xmlrpc-port**:

```
$ ../odoo/odoo.py start --xmlrpc-port=8080
```



## Configure Database

### webpage mode

Configuresthe server with some options which interfere with multi-database management.To access the database, the following steps need to be performed:

1.   Go to the login screen of your instance (if you are authenticated, log out).

2.   Click on the Manage Databases link. This will navigate to [http://localhost:8069/web/database/manager](http://localhost:8069/web/database/manager) (you can also point your browserdirectly to that URL.).

3.   Click on the **Create Database**

     - Master password: The master password for this instance,like superuser password, e.g. 123456.
     - Database name: Input the name of the database you wish to create.
     - Language: Select the language you wish to be installed by default in the newdatabase.
     - Password of **admin** user: Type the password you want to set for the adminuser of the new instance.
     - Load demonstration data: **Check** this box to have **demonstration data**. Thisis useful to run tests or set up a demonstration for a customer, but **shouldnot** be checked for a database meant to contain **production data**. 

4.   **Duplicating a database**

     Choose the pg_dump file, that can be restored; Choose the zip file, that include full files.

5.   **Removing a database**

6.   **Restore a database**

### command line mode

```
$ createdb testdb && odoo.py -d testdb

```

The additional bonus of this command line is that you can request installation of addonswhile you are at it using for instance -i sale,purchase,stock (more on this in Chapter 2,Managing Odoo Server Instances).

To duplicate a database, stop the server, and run the following command:

```
$ createdb -T dbname newdbname

$ cd ~/.local/share/Odoo/filestore # adapt if you have changed the data_
dir

$ cp -r dbname newdbname
$ cd -
```

To remove an instance, run the following command:

```
$ dropdb dbname
$ rm -rf ~/.local/share/Odoo/filestore/dbname

```

To create a backup (assuming the PostgreSQL server is running locally), use the followingcommand:

```
$ pg_dump -Fc -f dbname.dump dbname
$ tar cjf dbname.tgz dbname.dump ~/.local/share/Odoo/filestore/dbname
```

To restore the backup, run the following command:

```
$ tar xf dbname.tgz
$ pg_restore -C -d dbname dbname.dump
```



## Configure Odoo

To generate(create) a configuration  file for your Odoo instance, run the following command:

```
$ odoo.py --save --config myodoo.cfg --stop-after-init
```

The name of the file which is created is **myodoo.cfg**.

| Command line                    | Configuration file          |
| ------------------------------- | --------------------------- |
| --db-filter                     | dbfilter                    |
| --no-xmlrpc                     | `xmlrpc = True / False`     |
| --database                      | db_name                     |
| --debug                         | `debug_mode = True / False` |
| `--i18n-import / --i18n-export` | Unavailable                 |

| Option         | Format                      | Usage                                    |
| -------------- | --------------------------- | ---------------------------------------- |
| `without_demo` |                             | Prevents module demo data from being loaded. |
| addons_path    | Commaseparated list ofpaths | A list of directory names in which the server willlook for addons (see Chapter 2, Managing OdooServer instances). |
| `admin_passwd` | Text                        | The master password (see previous recipe). |
| data_dir       | Path to adirectory          | A directory in which the server will store sessioninformation, addons downloaded from theInternet, and documents if you enable the filestore. |
| db_host        | Host name                   | The name of the server running the PostgreSQLserver. Use False to use local Unix Domainsockets, and localhost to use TCP socketslocally. |
| db_user        | Database userlogin          |                                          |
| db_password    | Database userpassword       | This is generally empty if db_host is False anddb_user has the same name as the user runningthe server. Read the man page of pg_hba.conffor more information on this. |

| Option                        | Format                          | Usage                                    |
| ----------------------------- | ------------------------------- | ---------------------------------------- |
| database                      | Database name                   | Used to set the database name on which somecommands operate by default). This does not limitthe databases on which the server will act. See thefollowing dbfilter option for this. |
| dbfilter                      | A regularexpression             | The expression should match the name of thedatabases considered by the server. If you runthe website, it should match a single database,so it will look like ^databasename$. Moreinformation on this is in Chapter 16, ServerDeployment. |
| `xmlrpc_interface`            | IP addressof a networkinterface | Defaults to 0.0.0.0, meaning the server listenson all interfaces |
| `xmlrpc_portlongpolling_port` | Port number                     | The ports on which the Odoo server will listen.You will need to specify both to run multiple Odooservers on the same host. longpolling_portis only used if workers is not 0. |
| logfile                       | Path to a file                  | The file in which Odoo will write its logs. |
| log_level                     | Log verbositylevel              | Specify the level of logging. Accepted values (inincreasing verbosity order): critical, error,warn, info, debug, debug_rpc, debug_rpc_answer, debug_sql. |
| workers                       | Integer                         | The number of worker processes. See Chapter 16,Server Deployment, for more information. |
| `no_database_list`            | True / False                    | Set to True to disable listing of databases.See Chapter 16, Server Deployment, for moreinformation. |

The parsing of the con guration  le by Odoo is done using the Python **ConfigParser** module. 



##  Developer Mode

login->username->about->Activate the developer mode


​			
​		
​	
