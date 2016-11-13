public: yes
tags: [AWS, micro instance, cloud]
summary: |
  We stumbled upon a problem attaching, detaching, and then 
  reattaching a EBS volume to the same drive letter that is reproducible

A hidden limitation on AWS micro instances?
===========================================

We use a lot of AWS micro instances for development at `PythonAnywhere <http://www.pythonanywhere.com/>`_.
They can be viciously slow but in some ways that helps with our dogfooding
because you aren't lulled into a false sense of security by using a powerful
server with only a couple of dev users. 

Yesterday though when troubleshooting our backups process we discovered a weird
and reproducible problem.

Steps to replicate:

    1. Create an EBS volume on AWS 
    2. Attach it to a linux instance
    3. Wait for it to attach
    4. Detach it
    5. Attach it again at the same device point (i.e /dev/sdp)
    6. Voila! You volume does not attach


I have tested this against Debian Squeeze and Ubuntu 11.10. Both had identical
results. The EBS volume stays in the 'attaching' state for as long as we cared
to wait. And it is really NOT attached. It does not show up in /dev.

The important part in the step above is reusing the drive letter, but it does
not matter whether you actually mount the the filesystem on the volume. It 
seems that once you've used an attachment point (i.e /dev/sdp, which shows up
as /dev/xvdp on the OS) it is somehow corrupted and not available again until
after you reboot the instance.

Perhaps it is a byproduct of the IO limitations placed on micro-instances? 

Playing with EBS volumes is one easy way to cause some strange problems with 
AWS instances. Try detaching a mounted volume, it won't work. Then try 
unmounting the filesystem. Congrats, you've created an instance that takes a 
really long time to reboot with a umount process that does not listen to
kill -9. This is easy enough to do if you are not careful. 


