public: yes
tags: [advertising, golang, realtime]
summary: |
  In the on-line advertising industry bidders are a very important part of the 
  infrastructure of companies that need to buy ads at scale and for wholesale prices. 
  I recently developed one using Golang and learnt a lot along the way.

Developing a Real Time Bidder in Go(lang)
=========================================

Over the last year I have been working in the `online advertising industry <http://www.theguardian.com/media/2015/jul/19/ad-tech-online-experience-facebook-apple-news>`_. The company I was working for quickly realised that we would need to be able to directly purchase advertising inventory from the online exchanges (such as `PubMatic <http://www.pubmatic.com/>`_ and `Rubicon <http://rubiconproject.com/>`_) at wholesale prices. We needed to do this to make most of our ideas work. The only way to do this is to directly participate in the real time auctions that these exchanges hold.

If you don't know how these things work let me to explain. When you visit a website that uses an ad exchange (which is most of them) your details are sent to an exchange. The exchange then formats that information and maybe adds some more details to it. Then it fires that description out to other companies that are registered as bidders. These companies have 100ms (1/10 of a second) to reply with an ad that they want to display and the price that they are willing to pay. The whole process takes less than a second. And at peak times there might be 300K per second of these events to process and bid on.

.. raw:: html

   <img alt="Sample daily RTB traffic" src="https://www.aychedee.com/static/daily-rtb-traffic.png" style="max-width: 100%;">

Above you can see a week of daily traffic from one of these exchanges. It has a very regular cycle. With a peak around 6PM every day. That right there is the internet's pulse.

Bidders are the systems that respond to the exchanges. And bidders are hard core engineering challenges. They combine *low latency* with very *high throughput*. Not only that but they are spending real money. The exchange doesn't care if you made a mistake and accidentally bought $100K worth of online ads one afternoon. They just send you a bill.

After deciding that we needed a bidder, the first step was seeing if there was any existing open source work that we could build on top of. As you can imagine there isn't much. Not that many bidders exist, and there isn't a lot of incentive for a company to open source their bidder once they've built one.

There is an open source project called `RTB Kit <http://rtbkit.org/site/>`_ which I did spend a couple of weeks evaluating. But it included some very interesting design choices which would have prevented us from doing some of the more creative things we wanted to achieve. It was heavily stateful, and each component had to be scaled independently. I had an intuition that a bidder could be radically simpler if it was more functional. If it treated each bid request as a individual unit. And that whole components of the RTB Kit bidder would become unecessary.

To check assumptions I created a prototype in Python. The radically simpler design worked well, and even in Python could handle around 5K requests / second. Which would be enough for the smaller bid streams. The main problem with the Python prototype is that the latency was very inconsistent. A large amount of requests would not have completed in the 100ms window given by the exchange.

The Python prototype made heavy use of ZMQ to distribute the workload between different processors. It seemed that Go's channels, automatic multiprocessing support, and easily deployed executable would make the entire project significantly simpler. While the latency requirements are not so extreme that the pauses for garbage collection would become an actual problem.

These intuitions proved to be true.

Preventing catastrophic overloads
---------------------------------

The first time we exposed the bidder to actual live loads from an exchange it lasted about 2 minutes before a series of cascading failures caused every request to time out. Queues filled up and every request could only be handled as quickly as the slowest component. The big realisation from this was that we didn't really want queues at all. If a bid request had been in a queue for 80ms then it was already too late. We may as well just throw it away. With an exchange you always have the option of responding with a 204 NO CONTENT instead of a bid.

Go provides an elegant way to create a precise bottleneck. Channels can be selected on. If there is nothing waiting in the channel, like a worker thread, then it will flow through to a default case.

.. code-block::  go

    select {
        case worker := <-bouncer:
            // Do the actual work, when the work is finished send response and
            // put the worker back on the bouncer channel
        default:
            // We had no workers attached to the bouncer channel
            // So send a 204 to the exchange
    }

In this case bouncer is a zero length channel. There is no queuing. An incoming task can either be handled with the scarce resources available or it cannot. No work is done before that decision is made. Which means massive surges in requests do not degrade the overall performance of the system. Which is exactly what you need to prevent overloading. The system responds to as many requests as it can while ignoring any that it can't handle in a timely fashion. With this control in place a four core machine could handle a throughput of ~70K requests / sec with each request having only a few ms latency.

Shedding load in this way was the key insight that let us create a stable system that could handle that daily internet pulse with acceptable latency.

Managing budgets
----------------

Each advertising campaign has a budget. It's obviously important that we don't over spend that budget. But less intuitively it's also important that we spend all of that budget, and that we spend the budget smoothly.

Most bidder implementations I've seen in the wild allocate budget on a time basis. So every hour, or 15 minutes, or whatever, the bidder is given a chunk of budget to spend. They then spend this chunk as quickly as they can. Which means that most of the budget is spent at discrete time boundaries. This practice is so common that the price of an online ad is much higher at 10.01AM than it is at 10.05AM. This is exactly how RTB Kit allocates budget, and its design choice to use an independent banker makes it difficult to operate it any differently.

The simplest linear pacing is a big improvement and it was easy to implement. Every time a bid request comes in each we calculate how much each campaign has spent and how much it should have spent, to the second, at this point in time. If it hasn't spent enough then it can place a bid. Simple. It means campaigns spend in a straight line rather than blowing their budget in the first minute of their budget period. The budget details are recorded in a machine local redis instance. Without any network latency redis is fast enough for this purpose.

There is always a period between placing a bid and finding out if you've won it. This means that you need to keep track of budget that is 'inflight' and tidy up that record as time passes when you can assume you didn't win. There are no win or loss notices from the exchange. The only way that you can tell that you've won an ad impression is when the end user requests the ad from your server! That request contains the price you paid and is your confirmation that you won an auction.

To keep track of this information across multiple processes/threads we used the machine local redis instance and some embedded Lua.

The amount of budget 'inflight' could never exceed the budget remaining for a campaign. So before each bid is actually sent to the exchange the thread (actually a goroutine) calls a Lua script with the id for the campaign, the remaining budget, the price to be bid, and the current Unix timestamp.

The Lua script finds the right redis hash for the campaign, and then retrieves all the key/value pairs. The keys are the timestamp for the bid, and the values are the amount bid at that timestamp. It then deletes any pairs that happened more than 2 seconds in the past and sums the values. If that sum plus the new bid value is greater than the budget remaining it returns an error to the caller. If it is less the value of the current bid is added to the value (if any) of the hash key represented by the current timestamp.

Lua functions embedded in redis are executed atomically, so we could be sure that our threads weren't trampling on each other at this point.

This gives a two second sliding window of 'inflight' budget and contributes to smoothly spending a campaigns budget.

Cost efficiency
---------------

With Go it was relatively straightforward to create a bidder system with minimal dependencies. An entire system that could be run on a single machine. Which means that a basic 4 core AWS instance can easily handle the bid request stream from any given exchange. This is around 1/8th of the running cost of an RTB Kit cluster.

Through the process of designing and building this system I was focused on simplicity. using Go really helped in this area. The baked in language features, channels in particular, make this kind of work much more elegant.

So: Thanks to the `Golang team <https://golang.org/CONTRIBUTORS>`_. You made my last six months of work a pleasure.


