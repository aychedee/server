public: yes
tags: [AWS, tips]
summary: |
  Converting an instance store backed AMI to an EBS backed AMI is quite simple
  but has a couple of little tricks that can leave you scratching your head for
  6 hours... or maybe that's just me. 

Convert an instance store backed AMI to an EBS backed AMI
=========================================================

At PythonAnywhere we recently decided to move all our development environments
onto Amazon's AWS. Thie first step of that was to convert the base AMI, that we 
use for all our servers, into an EBS backed one. The reason for this is that 
micro instances can only be created from EBS backed AMIs. We use a lot of 
servers for each developer, but don't use each server very much, so this seemed
like a natural cost saving to make.  

Quick summary:

    1. Use your instance store AMI to spin up a server on AWS
    2. Create a brand new EBS volume, 8 gigs oughta be enough
    3. Attach the new volume to the new instance
    4. SSH into the new machine 
    5. Make a filesystem on the appropriate device  
    6. Mount the new filesytem
    7. Rsync the contents of '/' to the mounted EBS volume
    8. Make necessary changes to /etc/fstab then unmount
    9. In the AWS console create a snapshot of the EBS volume
    10. Use the new snapshot to create an EBS backed image


The part that gave us the most trouble was getting that image to boot which 
came down to selecting the correct AKI. Each AKI is setup to boot a specific
CPU architecture from a specific device or partition. hd00 means that PVgrub is
going to look for a kernel to boot from on the first partition of the first 
device. If you follow the steps above you won't have a first partition and will
have to use the AKI hd0. This took us a while to figure out...

I'll only bother going into a bit more depth on the parts that aren't
completely obvious. The commands mentioned below should be run as root while
logged into the instance you are trying to create an EBS AMI from. 

3. When you attach an EBS volume to a linux machine the the /dev/DEVICE is 
   usually different. /dev/sdf becomes /dev/xvdf for example. You'll have to 
   double check where the device is actually attached. 

5. Do this before mounting using the filesytem of your choice. 

.. code-block:: bash

   mkfs.ext4 /dev/xvdf

Will do the trick.

7. We tried various methods of copying the root device. It turns out that rsync
   was the best. dd took much longer for no real benefit. /dev/xvdf was 
   mounted on /mnt/ebs before running this command of course.

.. code-block:: bash

   rsync -ax / /mnt/ebs
   mkfs.ext4 /dev/xvdf

8. As I mentioned above you might need to modify your fstab in order for the 
   new AMI to boot. Removing any references to anything other than /dev/xvda
   should be safe and you can always change it later.


Being lazy / efficient we automated this whole procedure using the Python
libraries boto and fabric to create the function below. 

.. code-block:: python

    from boto.ec2.blockdevicemapping import BlockDeviceMapping, EBSBlockDevice

    def create_ebs_image_from_running_instance(conn, instance, image_name):
        ebs_image_name = 'EBS - %s' % (image_name,)
        volume, snapshot, image = None, None, None
        try:
            volume = conn.create_volume(10, 'us-east-1a')
            volume.add_tag('Name', 'Base for %s' % (ebs_image_name,))
            attach_ebs_volume(conn, instance.id, volume.id, '/dev/sdf')
            with fabric_settings(instance.dns_name, root_password):
                run('mkfs.ext4 /dev/xvdf')
                run('mkdir -p /mnt/ebs')
                run('mount /dev/xvdp /mnt/ebs')
                run('rsync -ax / /mnt/ebs')

                # Remove any unwanted entries from /etc/fstab
                run('grep -v xvdb /mnt/ebs/etc/fstab > /tmp/fstab')
                run('mv /tmp/fstab /mnt/ebs/etc/fstab')
                # umount to flush fs changes
                run('umount /mnt/ebs')

                snapshot = conn.create_snapshot(volume.id, description=ebs_image_name)
                if not snapshot:
                    raise Exception('EBS image creation failed at the snapshot phase.')
                while snapshot.status != 'completed':
                    time.sleep(10)
                    snapshot.update()
                    print '.',
                    sys.stdout.flush()

                # Define the mapping for the images ephemeral drive
                mapping = BlockDeviceMapping()
                ebs_device = EBSBlockDeviceType()
                ebs_device.snapshot_id = snapshot.id
                ebs_device.delete_on_termination = True
                mapping['/dev/sda1'] = ebs_device

                image = conn.register_image(
                name=ebs_image_name,
                architecture='x86_64',
                kernel_id='aki-825ea7eb',
                root_device_name='/dev/sda1',
                block_device_map=mapping,
                )

                return ebs_image_name, image

