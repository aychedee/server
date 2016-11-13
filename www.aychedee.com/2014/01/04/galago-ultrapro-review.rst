public: yes
tags: [review, system76, linux]
summary: |
  I recently bought myself a Galago UltraPro 14" laptop. It's the first
  dedicated piece of Linux hardware I have purchased. Here's a short review

Galago UltraPro 14" Linux laptop review
=======================================

For as long as I've been buying myself laptops I have been buying them with
windows installed, formatting the hard drive, and installing Linux. After 14
years of doing that I decided it was time to buy a dedicated piece of hardware.

The `Galago UltraPro looked like the ideal machine <https://www.system76.com/laptops/model/galu1>`_
to replace my aging Dell.

.. image:: http://www.aychedee.com/static/galago-ultrapro-open.jpg
   :alt: Galago UltraPro running Gnome Shell


**Pricing**: A reasonable price for the quality of machine that you are getting.
Works out to be quite expensive once you pay for UK shipping and cover the
domestic sales tax (VAT of 20%).

**Feel**: It’s simultaneously light and solid. There is no flex to the chassis
and the keyboard is satisfying solid to type on. From reading some other
reviews I see this is the third incarnation of the keyboard bed and it seems to
have fixed all problems that may have existed previously. I also appreciate
that the function keys default to being function keys. The alternate
media keys behaviour requires pressing <Fn>.

**Display**: This is a very nice display, crips and bright. Compares well to
anything else I’ve seen and has a resolution of 1980 x 1080. It has one issue
that you notice when watching movies. At certain points around the edges the
backlight bleeds through. So the screen is noticeably brighter in places. Oh,
and the screen has a matte finish. Sure a glossy tv screen appeals to consumers
but I just don't think gloss finish should be used for something you're
primarily reading / writing on. Would you buy a glossy Kindle? Would any sane
company make one?

**Performance**: This is a very fast machine. The CPU is an Intel Core i7-4750HQ
CPU @ 2.00GHz. So that’s 8 cores. Combined with an SSD and 16GB of fast ram
this is a proper ultrabook. Even with 8 processes maxing out the available
cores the UI never feels unresponsive. Though I don’t think System76 can really
take the credit for that. Ever since `the Completely Fair Scheduler <http://en.wikipedia.org/wiki/Completely_Fair_Scheduler>`_
was introduced in the 2.6.23 kernel we’ve seen that behaviour.

**Sound / Heat**: In order to get the fans whirring I had to max out all 8 cores. I
did it by following these instructions on `how to mine primecoins <http://www.aychedee.com/2013/11/28/mining-primecoins/>`_
With the primecoin miner running at a satisfying 760% of cpu the fans do
eventually come on. But then only if it is sitting on a flat surface. Sitting
on my lap I was unable to get the fans to start and the CPU temperature never
exceeded 52°C. It never felt hot on my lap. Even with the fans on it wasn’t
particularly loud. So overall a very qiuet and cool little machine. May seem
like something inconsequential but working with a noisy and or hot computer on
your lap for extended periods is horrid.

**Battery life**: Not fantastic for this form factor. About 3 hour under normal
use. There are probably improvements to this that can be made to this by using
`powertop <https://01.org/powertop/>`_ and doing some tuning.

**Trackpad**: It took a little while getting used to it and it has some problems.
Specifically it doesn’t seem to be able to emulate a middle click. And middle
click to paste, or open a link in a new tab, or a close a tab is something that
I use a lot. The behaviour is very similar to a Mac laptop. In that you can two
finger click for a right click and double tap to select. There is also a small
portion of the trackpad in the bottom right corner that you can just click for
a right click.

But yeah. If anyone has middle click emulation working on this thing then I
would love to hear about iti...

*UPDATE 18/03/2014:* `Thomas Schaz <https://twitter.com/ThomasSchaz>`_ got in
touch and helped me through this issue: By default three finger tap is set up
to be the middle mouse click. However this just doesn't work for me on Ubuntu.
So the solution I went for was to swap the two finger tap (which I don't need)
from being a right click to a middle click.

The relevant config for xorg looks like this:

.. code-block:: bash

    Option "TapButton2" "2"
    Option "TapButton3" "3"

And I added those to a new file in /usr/share/X11/xorg.conf.d/

**Ports**: Nothing legacy! No RGB ports cluttering things up. Just three USB
v3.0, HDMI, mini displayport and SD reader. If you wanted to connect this to
two monitors you'd need some kind of HDMI to displayport adaptor. But really
for my uses this is the perfect selection of ports.

**Graphics**: The Intel Iris Pro chipset works. I tested it with a couple of
old games on steam. Team Fortress 2 and Left 4 Dead 2 both worked perfectly.
I'm sure it couldn't handle the very latest titles but that is not unexpected.

Out of the box experience? fantastic. Ubuntu install was perfect. All
components work well. The experience in this regards was better than my wife's
Mac pro.

This is my first time buying a dedicated piece of Linux hardware (not counting
cell phones) and it’s been a very happy experience.

After using Linux exclusively for 14 years I felt it was about time that I
bought dedicated hardware. It is almost impossible to buy a laptop without
windows pre installed from a major manufacturer (with the notable exception of
`Dell’s “sputnik” laptops <http://www.dell.com/learn/us/en/555/campaigns/xps-linux-laptop>`_
) so as someone who morally disagrees with that situation it was time to stop
buying a windows license and throwing it away each time I upgraded.

Overall this is a very powerful, small, light, quiet laptop that I’ve been
enjoying developing on with some small problems. Problems which I’m willing to
forgive to support a broader cause.

.. image:: http://www.aychedee.com/static/galago-ultrapro-closed.jpg
   :alt: Galago UltraPro closed

