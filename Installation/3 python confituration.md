#### 1. download python source
```shell
Login as root
wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz
```

#### 2. install python on OS
```shell
Login as root
cd /download/
yum install openssl-devel -y
yum install sqlite-devel -y 
tar -xvf Python-3.5.1.tgz
cd /download/Python-3.5.1
mkdir /opt/python35
chmod 0755 /opt/python35
./configure --prefix=/opt/python35/  --with-ensurepip=install
make
make install

```

#### 3. config user vitural python environment
```shell
Login as logoshow
/opt/python35/bin/pyvenv-3.5 --copies ~/py35
echo ". ~/py35/bin/activate" >> ~/.bash_profile
```