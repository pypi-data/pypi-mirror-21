# bugOne Python package #

Simple package to interact with a bugNet. You can use both serial port 
sniffer or a mux serial port. 


The package provides a packet dumper 

```
bugone-dumper:
 usage : bugone-dumper [-c host] [-s serial port] [-d hex|log|print]
 Diplay packet bugNet received in an human readable format
```

Example:

```
jkx@home0 ~/> bugone-dumper -c myserver -d log
Thu Mar 23 09:16:40 2017 => Message [65079] from 33 to 255
- (33.1) -> (255.41) = 344
- (33.2) -> (255.41) = 196
Thu Mar 23 09:16:48 2017 => Message [21330] from 22 to 255
- (22.1) -> (255.41) = 352
- (22.2) -> (255.41) = 190
- (22.3) -> (255.41) = 491
```

## Install ## 
To install simply use pip 
```shell
pip install bugone 
```



## Links ##
* [PyPI Entry](https://pypi.python.org/pypi/bugone/)
* [bugOne git](https://github.com/jkx/DIY-Wireless-Bug)
* [DIY Wireless Bug](http://dwb.ilhost.fr/)
* [mux_serial](https://github.com/marcelomd/mux_serial)
