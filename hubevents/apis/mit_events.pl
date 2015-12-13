#!/usr/bin/evn perl

# Author: J. Halverson
# Date: December 12, 2015

use SOAP::Lite;
use Data::Dumper;

use SOAP::Lite +autodispatch =>
  uri => '/',
  proxy => 'http://events.mit.edu/websvc/';#, +trace;   # remove first semi and uncomment to see a SOAP trace

my $em = new SOAP::Lite
    -> uri('/MIT/Events/EventManager');

use String::Util qw(trim);
use Date::Calc qw(Today Add_Delta_Days);

my $start = "2015/12/12";
my $end   = "2015/12/19";
my $scevents = result($em->getDateRangeEvents($start, $end));
foreach my $event (@$scevents) {
    print $event->{'title'} . "\n";
    # type_code - S/M/R. S - indicates a simple (non-recurring) event, M indicates
    # a multiple-day event, and R indicates a repeating event
    $type_code = $event->{'type_code'}; 
    if ($type_code eq "S" or $type_code eq "R") {
      print $event->{'start'}->{'weekday'} . ", " . $event->{'start'}->{'monthname'} . " " . $event->{'start'}->{'day'} . "\n";
    }
    elsif ($type_code eq "M") {
      print $event->{'start'}->{'weekday'} . ", " . $event->{'start'}->{'monthname'} . " " . $event->{'start'}->{'day'} . "\n";
      print $event->{'end'}->{'weekday'} . ", " . $event->{'end'}->{'monthname'} . " " . $event->{'end'}->{'day'} . "\n";
    }
    else {print "ERROR: type_code\n";}
    print $event->{'start'}->{'hour'}. ":" . $event->{'start'}->{'minute'} . " - " . $event->{'end'}->{'hour'}. ":" . $event->{'end'}->{'minute'} . "\n";

    # location and address
    $lctn = $event->{'location'};
    $sloc = $event->{'shortloc'};
    if ($lctn ne "" and $sloc ne "") {
      print "MIT, " . $lctn . ", " . $sloc . ", Cambridge\n";}
    elsif ($lctn ne "" and $sloc eq "") {
      print "MIT, " . $lctn . ", Cambridge\n";}
    elsif ($lctn eq "" and $sloc ne "") {
      print "MIT, " . $sloc . ", Cambridge\n";}
    else {
      print "MIT, Cambridge\n";}
    print "\n";

    $lecturer = $event->{'lecturer'};
    if ($lecturer ne "") {print "Speaker(s): " . $event->{'lecturer'} . "\n";}
    print $event->{'description'} . "\n\n";

    # from http://events.mit.edu/help/soap/index.html#Overview
    #   opento - 0=MIT-only; 1=Everybody; 2=Other, "other" value specified in opentext
    #   opentext - used to specify who the event is open to if opento is 2
    $opento = $event->{'opento'};
    $opentext = $event->{'opentext'};
    if ($opento == 0) {print "Open to: MIT only\n";}
    elsif ($opento == 1) {print "Open to: the general public\n";}
    elsif ($opento == 2) {print "Open to: " . $opentext . "\n";}
    else {print "ERROR: opento not in list\n";}

    # print cost if not free
    $cost = $event->{'cost'};
    if (lc $cost ne "free" and lc $cost ne "free!" and $cost ne "") {
      print "Cost: " . $cost . "\n";}

    # print sponsor information
    @colors = ();
    $sponsors = $event->{'sponsors'};
    foreach $s (@$sponsors) {
      $s_name = $s->{'name'};
      $s_contact = $s->{'contact'};
      $s_email = $s->{'publicmail'};
      #print "Sponsor(s): " . $s_name . "\n";
      push(@colors, $s_name);
      #if ($s_email eq "") {
      #  print "Sponsor(s): " . $s_name . ", " . $s_contact . "\n";
      #}
      #else {
      #  print "Sponsor(s): " . $s_name . ", " . $s_contact . " (" . $s_email . ")\n";
      #}
    }
    print "Sponsor(s): " . join(", ", @colors) . "\n";
    $other_sponsors = $event->{'other_sponsors'};
    #print "OTHERS: " . $other_sponsors . "\n";
    #print "SCALAR: " . scalar(@$sponsors) . "\n";

    # contact and sponsor information
    $infoname = trim($event->{'infoname'});
    $infomail = trim($event->{'infomail'});
    if ($infoname ne "" and $infomail eq "") {
      print "Contact: " . $event->{'infoname'} . "\n";}
    elsif ($infoname ne "" and $infomail ne "") {
      print "Contact: " . $event->{'infoname'} . " (" . $event->{'infomail'} .  ")\n";}
    else {
      print "Contact: " . $event->{'infomail'} . "\n";}
    $infourl = $event->{'infourl'};
    if ($infourl ne "") {print "Web site: " . $event->{'infourl'} . "\n";}
    $infophone = $event->{'infophone'};
    if ($infophone ne "") {print "More info: " . $event->{'infophone'} . "\n";}
    $infoloc = $event->{'infoloc'};
    if ($infoloc ne "") {print "More info address: " . $event->{'infoloc'} . "\n";}

    print "\n-------------------------------\n\n";
}

### uncomment the three lines below to see the raw event info for debugging
#foreach my $event (@$scevents) {
#    print Dumper($event);
#}

exit(0);

#
# Helper to deal with SOAP faults
#
sub result {
    my ($som) = @_;
    if ($som->fault) {
	die "SOAP Error: " . $som->faultcode() . " - " . $som->faultstring() . "\n";
    }
    return($som->result);
}
