#!/usr/bin/env perl

# Author: J. Halverson
# Date: December 12, 2015

# Usage: perl mit_events.pl > mit_26feb2016.txt

# Dates are always in the format:
#   yyyy/mm/dd hh:mm
# where hh:mm is optional and hh is in 24-hour format

#########################
$start = "2016/04/18";
$end   = "2016/05/31";
#########################

use SOAP::Lite;
use Data::Dumper;

use SOAP::Lite +autodispatch =>
  uri => '/',
  proxy => 'http://events.mit.edu/websvc/';#, +trace;   # remove first semi and uncomment to see a SOAP trace

$em = new SOAP::Lite -> uri('/MIT/Events/EventManager');
$scevents = result($em->getDateRangeEvents($start, $end));
foreach $event (@$scevents) {
    print $event->{'title'} . "\n";
    # type_code - S/M/R. S - indicates a simple (non-recurring) event, M indicates
    # a multiple-day event, and R indicates a repeating event
    $type_code = $event->{'type_code'}; 
    $s_wkdy = $event->{'start'}->{'weekday'};
    $s_month = $event->{'start'}->{'monthname'};
    $s_day = $event->{'start'}->{'day'};
    if ($type_code eq "S" or $type_code eq "R") {
      print $s_wkdy . ", " . $s_month . " " . $s_day . "\n";
    }
    elsif ($type_code eq "M") {
      $e_wkdy = $event->{'end'}->{'weekday'};
      $e_month = $event->{'end'}->{'monthname'};
      $e_day = $event->{'end'}->{'day'};
      print $s_wkdy . ", " . $s_month . " " . $s_day . " - ";
      print $e_wkdy . ", " . $e_month . " " . $e_day . "\n";
    }
    else {print "ERROR: type_code\n";}
    $s_hour = $event->{'start'}->{'hour'}; $s_hour += 0;
    $s_mins = $event->{'start'}->{'minute'};
    $e_hour = $event->{'end'}->{'hour'}; $e_hour += 0;
    $e_mins = $event->{'end'}->{'minute'};
    print &format_time($s_hour, $s_mins) . " - " . &format_time($e_hour, $e_mins) . "\n";
 
    # location and address
    $lctn = $event->{'location'}; # event location in long text format
    $sloc = $event->{'shortloc'}; # event location in building/room format
    if ($lctn && $sloc) {
      print "MIT, " . $lctn . ", Building " . $sloc;
      if ($lctn =~ /Cambridge/) {print "\n";}
      else {print ", Cambridge\n";}}
    elsif ($lctn && !$sloc) {
      print "MIT, " . $lctn;
      if ($lctn =~ /Cambridge/) {print "\n";}
      else {print ", Cambridge\n";}}
    elsif (!$lctn && $sloc) {
      print "MIT, Building " . $sloc . ", Cambridge\n";}
    else {
      print "MIT, Cambridge\n";}
    print "\n";

    $lecturer = $event->{'lecturer'};
    if ($lecturer) {print "Speaker(s): " . $event->{'lecturer'} . "\n";}
    $d = $event->{'description'};
    $d =~ s/\015//g; # substitute ^M characters with empty space
    print $d . "\n\n";

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
    if ($cost && lc $cost ne "free" && lc $cost ne "free!") {
      print "Cost: " . $cost . "\n";}

    # print sponsor information
    @spons = ();
    $sponsors = $event->{'sponsors'};
    foreach $s (@$sponsors) {
      push(@spons, $s->{'name'});}
    print "Sponsor(s): " . join(", ", @spons) . "\n";
    $other_sponsors = $event->{'other_sponsors'};
    if ($other_sponsors) {print "Sponsor(s): " . $other_sponsors . "\n";}

    # contact and sponsor information
    $infoname = $event->{'infoname'};
    $infomail = $event->{'infomail'};
    if ($infoname && !$infomail) {
      print "Contact: " . $infoname . "\n";}
    elsif ($infoname && $infomail) {
      print "Contact: " . $infoname . " (" . $infomail .  ")\n";}
    elsif (!$infoname && $infomail) {
      print "Contact: " . $infomail . "\n";}
    $infourl = $event->{'infourl'};
    if ($infourl) {print "Web site: " . $infourl . "\n";}
    $infophone = $event->{'infophone'};
    if ($infophone) {print "More info: " . $infophone . "\n";}
    $infoloc = $event->{'infoloc'};
    if ($infoloc) {print "More info address: " . $infoloc . "\n";}

    print "\n-------------------------------\n\n";
}

# convert from 24-hour clock to 12
sub format_time {
  my ($hr, $mn) = @_;
  if ($hr >= 13) {$hr - 12 . ":" . $mn . " PM";}
  elsif ($hr == 0)  {"12:" . $mn . " AM";}
  elsif ($hr == 12) {"12:" . $mn . " PM";}
  else {$hr . ":" . $mn . " AM";}
}

### uncomment the three lines below to see the raw event info for debugging
#foreach $event (@$scevents) {
#    print Dumper($event);
#}

exit(0);


# Helper to deal with SOAP faults
sub result {
    my ($som) = @_;
    if ($som->fault) {
	die "SOAP Error: " . $som->faultcode() . " - " . $som->faultstring() . "\n";
    }
    return($som->result);
}
