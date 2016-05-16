# HubEvents Project
####Jonathan Halverson

With all that is going on in Boston it is easy to miss key events. The goal of this
project is to create a universal calendar that will make it possible to search every
instutition in Boston that holds public events.

Presently, one must visit sites like Meetup, Eventbrite, MIT Events,
Harvard Gazette, [BUGC](http://bugc.org), etc. When the project is complete it will be possible
to search all institutions and organizations with a single search.

My solution is to use APIs and web scraping to build a searchable database of all
the public events in Boston. Currently, I have written code that pulls from the
Eventbrite API and the MIT Events API. We use the RSS feed to get event listings from the
Harvard Gazette. Most insitutions do not provide APIs. For Boston University, I have written a web scraping
script in Python that uses the requests and BeautifulSoup packages. Work has begun on
other universities.

This project started with George Mokray. For more than 10 years, George has been manually compiling a list of interesting events going
on in the Boston/Cambridge area ([http://hubevents.blogspot.com](http://hubevents.blogspot.com)). I met
George when he approached us at the Boston Chapter for Data Science for the Social Good. I have been
leading the technical work since July of 2015.

I presented this projet at Data-Con on August 8, 2015 in Cambridge, MA. A hackathon devoted to the project took place in the
afternoon.
