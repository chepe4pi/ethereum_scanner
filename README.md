[![Build Status](https://travis-ci.org/chepe4pi/ethereum_scanner.svg?branch=master)](https://travis-ci.org/chepe4pi/ethereum_scanner)
[![Coverage Status](https://coveralls.io/repos/github/chepe4pi/ethereum_scanner/badge.svg?branch=master)](https://coveralls.io/github/chepe4pi/ethereum_scanner?branch=master)

Usage:

- Pull docker image:
 ``` docker pull chepe4pi/ethereum_scanner ```
- Run docker container with port binding: 
``` docker run -d -p8000:8000 chepe4pi/ethereum_scanner ```
- for fill database fast and async you have to use this script:
``` ./manage.py sync_blocks_and_txs 1 1800000``` (blocks rate)
- for start real-time tx and blocks monitoring you have to use this one:
``` ./manage.py start_block_monitor``` (it will fell database in real-time)
 
 
 PS: It's configuration for tests and development. 
 For production environment you have to use stronger solution.