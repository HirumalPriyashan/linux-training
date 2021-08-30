# Linux Troubleshooting

## Resource Limitation ( Soft and Hard limits )

1. Create a user with name : user1

   ```sh
   sudo useradd user1
   ```

2. Set the user1 soft limit RAM size to 1 GB

   ```sh
   su user1
   ulimit -Sv 1048576
   ```

3. Set the user1 soft limit file size to 2MB and Hard Limit file size to 3MB

   while logged in as user1

   ```sh
   ulimit -Sf 2048
   ulimit -Hf 3072
   ```

4. Set the user1 Linux open file limit Soft = 5000 hard = 6000

   while logged in as user1

   ```sh
   ulimit -Sn 5000
   ulimit -Hn 6000
   ```

   - For the ulimits to persists across reboots, add followings to `/etc/security/limits.conf` and save the file

   ```txt
   user1 soft fsize 2048
   user1 hard fsize 3072
   user1 soft nofile 5000
   user1 hard nofile 6000
   ```

5. Set the servers network card’s receiving ring buffer to Maximum value

   - find the max of receiving ring buffer

   ```sh
   ethtool -g enp0s3
   ```

   - set to the max of receiving ring buffer

   ```sh
   sudo ethtool -G enp0s3 rx <max-RX-value>
   ```

6. Share the screenshot of
   i. Ulimit -Ha

   ![Ulimit -Ha](./q1-1.png)

   ii. Ulimit -Sa

   ![Ulimit -Sa](./q1-1.png)

   iii. /etc/security/limits.conf

   ![/etc/security/limits.conf](./q1-3.png)

## SWAP

Creare Two swap files , and one should be in size of 100MB and second file should 200MB

- create files those will be used as swap files

  ```sh
  sudo fallocate -l 100M /swapfile1
  sudo fallocate -l 200M /swapfile2
  ```

  - if fallocate not installed

    ```sh
    sudo dd if=/dev/zero of=/swapfile1 bs=1024 count=102400
    sudo dd if=/dev/zero of=/swapfile2 bs=1024 count=204800
    ```

- set permissions

  ```sh
  sudo chmod 600 /swapfile1
  sudo chmod 600 /swapfile2
  ```

- setup the files as swap space

  ```sh
  sudo mkswap /swapfile1
  sudo mkswap /swapfile2
  ```

- enable swap

  ```sh
  sudo swapon /swapfile1
  sudo swapon /swapfile2
  ```

1. Assign 200MB swap file a priority 10 and 100MB swap file a priority 20

   ```sh
   sudo swapoff /swapfile1; sudo swapon -p 20 /swapfile1
   sudo swapoff /swapfile2; sudo swapon -p 10 /swapfile2
   ```

2. Configure swap files to mount during a boot

   - append followings to the `/etc/fstab` file

     ```txt
     /swapfile1 swap swap pri=20 0 0
     /swapfile2 swap swap pri=10 0 0
     ```

3. Change system swappiness value to 40

   ```sh
   sudo sysctl vm.swappiness=40
   ```

4. Share the screenshot of
   i. ./etc/fstab

   ![./etc/fstab](./q2-1.png)

   ii. free -m

   ![free -m](./q2-2.png)

   iii. swapon -s

   ![swapon -s](./q2-3.png)

## FTP

Configure and setup the proftpd FTP server .

```sh
sudo apt update
sudo apt install proftpd
```

use `/etc/proftpd/proftpd.conf` to configure
If needed change the server name change the server name value in the file.

```txt
ServerName  "prod-devops-master"
```

To only allow users access to their home directory by adding(or uncommenting),

```txt
# Use this to jail all users in their homes
DefaultRoot ~
```

Whenever changes are made to the configuration files make sure to restart the ftp service.
To restart:

```sh
sudo service proftpd restart
```

1. Create a user called proftpuser , which should be able to upload and download content from the ftp server

   ```sh
   sudo echo "/bin/false" >> /etc/shells
   sudo adduser proftpuser --shell /bin/false --home /home/proftpuser
   ```

   add followings to `/etc/proftpd/proftpd.conf` and save.

   ```txt
   <Directory /home/proftpuser>
        Umask 022
        AllowOverwrite off
        <Limit LOGIN>
            AllowUser proftpuser
            DenyAll
        </Limit>
        <Limit ALL>
            AllowUser proftpuser
            DenyAll
        </Limit>
   </Directory>
   ```

2. Set the proftpd process priority ( Nice value) as -5

   - if the server is already running

     - find the process PID

       ```sh
       ps aux | grep -i 'proftpd'
       ```

     - change nice value

       ```sh
       renice -n -5 <process-PID>
       ```

3. Share screenshot of
   i. Top command showing priority of the proftpd process

   ![top](./q3-1.png)

   ii. Share the configuration file of proftpd service

   [https://github.com/HirumalPriyashan/linux-training.git](https://github.com/HirumalPriyashan/linux-training.git)

## SQUID Proxy

Setup and configure the Squid proxy server in the Linux box

```sh
sudo apt update
sudo apt install squid
```

1. Make sure to allow HTTP traffic via squid proxy.

   - open `/etc/squid/squid.conf`

   ```txt
   sudo nano /etc/squid/squid.conf
   ```

   - navigate to the `http_access deny all` option and change that to the following:

   ```txt
   http_access allow all
   ```

   - restart the service

   ```sh
   sudo systemctl restart squid
   ```

2. Then point your local web browser to Squid proxy and check whether you can access HTTP web sites via the proxy

   ```sh
   curl -x http://127.0.0.1:3128/ -l http://google.com/
   ```

3. Configure Squid proxy to block following Domains
   i. .facebook.com and facebook.com
   ii. .wso2.com and wso2.com
   iii. Ubuntu.com

   - create new file for blocked list

   ```sh
   sudo nano /etc/squid/blocked.acl
   ```

   - add followings to the file

   ```txt
   .facebook.com
   .wso2.com
   ubuntu.com
   ```

   - open the /etc/squid/squid.conf file

   ```sh
   sudo nano /etc/squid/squid.conf
   ```

   - add the following lines before the first `http_access allow` statement:

   ```txt
   acl blocked_websites dstdomain "/etc/squid/blocked.acl"
   http_access deny blocked_websites
   ```

   - restart the service

   ```sh
   sudo systemctl restart squid
   ```

4. Configure Squid proxy daemon so that it will start during the boot in only in 1,3,5 run levels

   ```sh
   update-rc.d squid defaults
   update-rc.d squid disable 2 4 6
   update-rc.d squid enable 1 3 5
   ```

   ```txt
   (runlevel 1 & 6 can be omitted since action will have no effect on those runlevels)
   ```

5. Assign the I/O priority of Constant to the proftpd process ( Go via ionice command )

   - find `proftpd` service's pid

   ```sh
   ps aux | grep "proftpd"
   ```

   - assign the I/O priority

   ```sh
   sudo ionice -c 1 -p {pid-of-proftpd}
   ```

   i. Share the configuration file of Squid ( You can share configuration file via Github public repository URL )

   [https://github.com/HirumalPriyashan/linux-training.git](https://github.com/HirumalPriyashan/linux-training.git)
