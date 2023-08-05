phovea_data_redis [![Phovea][phovea-image]][phovea-url] [![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Dependency Status][daviddm-image]][daviddm-url]
=====================

Data provider plugin for loading data stored in a [Redis in-memory database](http://redis.io/).

Installation
------------

```
git clone https://github.com/phovea/phovea_data_redis.git
cd phovea_data_redis
npm install
```

Testing
-------

```
npm test
```

Building
--------

```
npm run build
```

Usage
------------

The plugin is currently used to load ID mapping files.

### Flush Mapping Database

```bash
redis-cli

select 3
flushall
```

Administrating Redis from your host machine
------------

Follow this steps if you want to administrate the Redis instance that is installed inside the virtual machine (using Vagrant)

1. Download any Redis administration tool (e.g., [Redis Desktop Manager](https://redisdesktop.com/))
2. Start docker-compose in debug mode: `docker-compose-debug up -d`
3. Access via localhost

Backing up a Redis DB: -> https://www.npmjs.com/package/redis-dump

Restoring in a named volume:

1. launch container
 ```
docker run -it -v workspacename_db_redis_data:/data -v F:\w\workspace_name\_backup\:/backup --name test redis:3.2-alpine sh ; docker rm test
 ```
2. within shell
 ```
redis-server --appendonly yes &
cd /backup
cat redis_db_dump_id.txt | redis-cli -n 3
cat redis_db_dump_mapping.txt | redis-cli -n 4 
exit
 ```
3. use backup tool to backup
 ```
 ./docker-backup backup db_redis_data
 ```

***

<a href="https://caleydo.org"><img src="http://caleydo.org/assets/images/logos/caleydo.svg" align="left" width="200px" hspace="10" vspace="6"></a>
This repository is part of **[Phovea](http://phovea.caleydo.org/)**, a platform for developing web-based visualization applications. For tutorials, API docs, and more information about the build and deployment process, see the [documentation page](http://phovea.caleydo.org).


[phovea-image]: https://img.shields.io/badge/Phovea-Server%20Plugin-10ACDF.svg
[phovea-url]: https://phovea.caleydo.org
[npm-image]: https://badge.fury.io/js/phovea_data_redis.svg
[npm-url]: https://npmjs.org/package/phovea_data_redis
[travis-image]: https://travis-ci.org/phovea/phovea_data_redis.svg?branch=master
[travis-url]: https://travis-ci.org/phovea/phovea_data_redis
[daviddm-image]: https://david-dm.org/phovea/phovea_data_redis/status.svg
[daviddm-url]: https://david-dm.org/phovea/phovea_data_redis


