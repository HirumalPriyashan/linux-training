# Introduction to Linux Administration

1. Set the VM name as “prod-devops-master” and set timezone as “Asia/Colombo”

   - setting the VM name

     ```sh
     sudo hostnamectl set-hostname prod-devops-master
     ```

     verify

     ```sh
     hostnamectl
     ```

   - set timezone

     ```sh
     sudo timedatectl set-timezone Asia/Colombo
     ```

     verify

     ```sh
     timedatectl
     ```

2. Add Linux users range from user1 to user7

   ```sh
   for user in {1..7}; do sudo useradd "user$user"; done
   ```

3. Create 2 Linux user groups called grpA and grpB, addthe above created users to Linux groups as below
   a. grpA -> user1,user2,user3

   ```sh
   sudo groupadd grpA
   sudo gpasswd -M user1,user2,user3 grpA
   ```

   b. grpB-> user4,user5,user6

   ```sh
   sudo groupadd grpB
   sudo gpasswd -M user4,user5,user6 grpB
   ```

4. Create a new disk partition using a loopback device and format it with XFS filesystem type. Mount it under /mnt and make sure to auto mount the partition during a reboot.

   - create loopback device

     ```sh
     dd if=/dev/zero of=loopbackfile.img bs=100M count=1
     sudo losetup -fP loopbackfile.img
     ```

   - check and find device for loopbackfile

     ```sh
     losetup -a
     ```

   - say device is `/dev/loop6`
   - create new partition

     ```sh
     sudo fdisk /dev/loop6
     ```

   - in the interactive shell

     ```sh
     Command (m for help): n
     Partition type
     p   primary (0 primary, 0 extended, 4 free)
     e   extended (container for logical partitions)
     Select (default p):
     Partition number (1-4, default 1):
     First sector (2048-204799, default 2048):
     Last sector, +sectors or +size{K,M,G,T,P} (2048-204799, default 204799):

     Created a new partition 1 of type 'Linux' and of size 99 MiB.

     Command (m for help): w
     The partition table has been altered.
     Calling ioctl() to re-read partition table.
     Syncing disks.
     ```

   - reflect changes to the kernel

     ```sh
     partprobe -s
     ```

   - verify

     ```sh
     sudo fdisk /dev/loop6
     ```

   - in the interactive shell (need to find corresponding loopback device)

     ```sh
     Command (m for help): p
     Command (m for help): q
     ```

   - say device is `/dev/loop6p1`
   - format with xfs file system

     ```sh
     sudo mkfs.xfs /dev/loop6p1
     ```

   - integrity check

     ```sh
     sudo fsck /dev/loop6p1
     ```

   - mount it under /mnt

     ```sh
     sudo mount /dev/loop6p1 /mnt
     ```

   - verify

     ```sh
     df -h
     ```

   - find uuid for loopback device

     ```sh
     lsblk -o NAMW,FSTYPE,UUID
     ```

   - to automount the partition during a reboot

     ```sh
     sudo nano /etc/fstab
     ```

   - append following and save

     ```txt
     UUID='obtained-uuid-from-previous-step'    /mnt    auto     defaults,loop    0   0
     ```

5. Create 3 folders inside /mnt as below
   a. /mnt/share-grpA
   b. /mnt/share-grpB
   c. /mnt/share-common

   ```sh
   sudo mkdir /mnt/share-grpA /mnt/share-grpB /mnt/share-common
   ```

6. Now configure the folder permissions to achieve belowcompany requirements.
   a. /mnt/share-grpA -> user1 is the owner . All members in grpA as well as the owner should be able to view files inside the folder and modify or create new files.

   - change owner

     ```sh
     sudo chown user1 /mnt/share-grpA
     ```

   - change group

     ```sh
     sudo chgrp grpA /mnt/share-grpA
     ```

   - add permissions

     ```sh
     sudo chmod 770 /mnt/share-grpA
     ```

   b. /mnt/share-grpB -> user4 is the owner . All membersin grpB as well as the owner should be able to view files inside the folder and modify or create new files

   - change owner

     ```sh
     sudo chown user4 /mnt/share-grpB
     ```

   - change group

     ```sh
     sudo chgrp grpB /mnt/share-grpB
     ```

   - add permissions

     ```sh
     sudo chmod 770 /mnt/share-grpB
     ```

   c./mnt/share-common -> user1 is the owner . All members in grpA and grpB should be able to view and create new files inside the folder. But they should not be able to delete another user’s file. Anyone else should not be able to view,create or delete files inside this folder.

   - change owner

     ```sh
     sudo chown user1:user1 /mnt/share-common
     ```

   - add permissions

     ```sh
     sudo chmod 700 /mnt/share-common
     sudo apt install acl
     sudo setfacl -m g:grpA:rwx /mnt/share-common
     sudo setfacl -m g:grpB:rwx /mnt/share-common
     sudo chmod +t /mnt/share-common
     ```

7. There is another requirement from higher management to allow CTO to only view the files inside the shared folder. Also he should not be added to either grpA or grpB linux groups. And still Anyone else other than the CTO / grpA /grpB should not be able to access files inside this folder.

   - create the group `CTO` and add `user7` to it

     ```sh
     sudo groupadd CTO
     sudo gpasswd -M user7 CTO
     ```

   - add permissions

     ```sh
     sudo apt install acl
     sudo setfacl -m g:CTO:r /mnt/share-common
     ```

8. Now in the devops server , we need to install the git command for cloning Github repositories.

   ```sh
   sudo apt install git
   ```

   to clone a repository

   ```sh
   git clone <url-for-required-repository>
   ```

9. The security team has been instructed to encrypt the /mnt partition as it contains sensitive data using the cryptsetup tool. Also to auto mount the /mnt partition on reboot.(hint - /etc/crypttab)

   - open crontab

   ```sh
   sudo apt update
   sudo apt install cryptsetup
   ```

   - unmount `/mnt`

     ```sh
     sudo umount /mnt
     ```

   - enter following and follow the propmts

     ```sh
     sudo cryptsetup -y -v luksFormat /dev/loop6p1
     ```

   - open to access the partition

     ```sh
     sudo cryptsetup luksOpen /dev/loop6p1 mnt
     ```

   - mount the LUKS

     ```sh
     sudo mkfs.xfs /dev/mapper/mnt
     sudo mount /dev/mapper/mnt /mnt
     ```

   to auto mount the /mnt partition on reboot

   - obtain the UUID of the encrypted device

     ```sh
     sudo cryptsetup luksUUID /dev/loop6p1
     ```

   - open `/etc/crypttab`

     ```sh
     sudo nano /etc/crypttab
     ```

   - add following to `/etc/crypttab` file and save it

     ```txt
     loop6p1 /dev/disk/by-uuid/<UUID-of-block-device> none luks
     ```

10. Finally , we need to monitor the shared folder to find and remove files older than 90 days using bash script. This script must be scheduled to run every day.

    - open crontab

      ```sh
      crontab -e
      ```

    - add following to the end of opened file and seave it

      ```txt
      0 0 * * * find /etc/mnt/share-common -type f -mtime +90 -delete
      ```
