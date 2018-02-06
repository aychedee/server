public: yes
tags: [QA, development, quality assurance]
summary: |
  I have a confession to make. When I became a software engineer I didn’t
  understand the role of QA. And it’s taken me 10 years to fully appreciate it.

Embracing quality
=================

I want to talk about my personal progression from ignorance, to indifference,
to embrace.

Ten years ago I started learning to write software. And was immediately
distressed at how bad I was at it, and how hard it was to make something that
worked properly. I spent around six months building a prediction market (The
New Product Stock Exchange! 😬), and at the end of that time it only kind of
worked. Small changes to one area of the application were likely to break
unrelated bits of it. I couldn’t hold the entire project in my head and didn’t
understand all the relationships between the different parts. 

Eight years ago I started working with the amazing group of people who created `PythonAnywhere <https://www.pythonanywhere.com>`_.
They introduced me to the wonderful world of Test Driven
Development. I fell in love. Here was the solution to the problem I’d
discovered! I wasn’t stupid. I wasn’t a terrible programmer. I just didn’t have
the tools to handle the huge complexity involved in software development. This
was my come to Jesus moment and I’ve embraced automated testing in every single
startup since. It has so many benefits. It is absolutely indispensable when
working on larger projects. The more people working on something the more
useful tests become. They are the ultimate documentation of what you expect the
code to do. 

Five years ago I left `PythonAnywhere <https://www.pythonanywhere.com>`_
and joined a series of startups. Usually leading the tech team. And on every
project I personally made sure we had comprehensive test suites. Both
integration and unit tests (though I prefer to think of Fast and Slow tests).
All written as part of the development process by the developers. Usually
starting with integration tests, and working inwards to unit tests.
`Being a Londoner, I had embraced London School TDD without realising it  <https://github.com/testdouble/contributing-tests/wiki/London-school-TDD>`_.
responsible for the successes and failures of a tech startup (and there were
many) teaches you a lot. All through this process it taught me that despite all
my tests I still struggled to deliver really high quality products. This nagged
at me constantly. Was I not writing enough tests?  Was I not writing the right
tests? Why did my well tested code still fail in the middle of a huge demo? I
mean obviously I should have written a test case to catch that failure. But…
there were so many different ways something could fail. Failure is probably the
easiest case to catch. A product being incredibly awkward and easy to use in
the wrong way. The way I hadn’t thought to test. That is also a big problem.
Plus there was a combinatorial explosion problem. The number of possible
failure scenarios were exhaustively large. Did I really have to write 10x or
20x the number of integration tests compared to the pieces of functionality in
my products? This was exhausting and I still wasn’t delivering the quality
products that I wanted to. 

One year ago I joined a larger startup called `Touch Surgery <https://www.touchsurgery.com/jobs>`_.
Again I was looking after a team and building products. And again I made sure
everything was being automatically tested but this time there was a difference.
There was a group of people in engineering doing QA. In fact my VP (hi James)
insisted that I hire someone to do QA for my team. I wasn’t reluctant. I just
didn’t understand what they would be doing. 

And so my final piece of epiphany arrived in the form of `Zak <https://www.linkedin.com/in/muhammad-zakariya-serroukh/>`_. Who once I
employed him began actively demolishing everything we’d built. Hunting for
inconsistent experiences, and unconsidered paths. 

What I had been missing for all those years was an antagonist.  

Together we started delivering quality.

So now I understand that quality requires that antagonism. I’m psychologically
incapable of thinking about something that I’ve built the same way that a user
who doesn’t know anything about it does. And no matter how many automated tests
we create, developers need the fast feedback loop of another mind bent towards
discovering actual quality in the products we build.

The quality of what our team is producing now is so much greater than anything
I have ever been able to produce through automated testing alone. I spent an
hour trying to break the responsive version of our web app today. And
absolutely could not find a single problem with it. But then, apparently I was
never very good at that anyway :)

It's apparent to me now that the role of the antagonist is absolutely vital to
build things that can withstand first contact with users. So 10 years after
starting my career and not really understanding or even being aware of the
role of QA. I now consider it to be one of the most important pillars of
engineering. If you care about quality anyway.

~~~

Of course Touch Surgery is looking for people, especially people who are
interested in building quality products. Get in touch!

