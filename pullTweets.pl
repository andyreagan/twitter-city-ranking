#!/usr/bin/env perl                                                                                                                  
use strict;
#use warnings;
use Cwd 'abs_path';
use Encode;
use utf8;
binmode STDIN,":utf8";
binmode STDOUT,":utf8";
no warnings 'utf8';

# pullTweets.pl --- queries zipped and boxed geotagged tweets
#
# by Jake R. Williams
#
#            ######################### description ###########################################
#            # 
#            #  we've been 'boxing' all of the geotweets. by 'boxing', we mean assigning
#            #  geographic codes to all of the geotagged tweets. these 'box' codes are
#            #  generally of the format 
#            #        
#            #                         box = country/state/county
#            #
#            #  with 'country', 'state' and 'county' each being a numeric ids for political
#            #  divisions as per the Global Administrative Areas (gadm.org) shapefiles. i
#            #  have delimited these as file paths for the natual structure the data will
#            #  take on once processed. if you would like to find box codes by actual box
#            #  names, then consult the accompanying file "boxKeys.txt".
#            #
#            #  since Andy Reagan set up our twitter 'spritzer' feed to collect nothing
#            #  but the best, geotagged tweets, we're getting lots of data. also, due
#            #  to some database enhancement on twitter's end (codename 'manhattan'),
#            #  we've be gathering what really does seem to be all geotagged tweets
#            #  (truly, since April 4th). this is the closest we've ever had to a complete 
#            #  data set, and since twitter recently began attaching good language 
#            #  identifications to their tweets, the data are doubly useful.
#            #  
#            #  here's what this script can do. 
#            #
#            #  the main functionality of this script is to pull tweets off of the database
#            #  by geographic, temporal, user, and linguistic filters. note that a time filter is
#            #  always necessary. the filter descriptions are listed below. i suggest using 
#            #  double quotes when applying filters for neurotic security.
#            #
#            #  it's also got some output flags, so depending on what information you are looking 
#            #  for this script will return various fields.
#            #
#            #  please note that output always comes in the following (tab-delimited) order:
#            #
#            #       time <tab> box <tab> coordinates <tab> language <tab> user <tab> tweet
#            #
#            #  where if you do not request a field, the order collapses appropriately.
#            #
#            ####################################################################################
#              #
#            ############### output flags ############
#            #   
#            #  -b    return the box id
#            #  -c    return the coordinates
#            #  -l    return the language
#            #  -m    return the message
#            #  -t    return the time
#            #  -u    return the user id
#            # 
#            #########################################
#              #
#            ########### file destination, optional ############
#            #
#            #  to avoid sending things to STDOUT:
#            #
#            #  "destination=/path/to/file.txt"
#            #
#            #########################################
#              #
#            ############################## filters ##############################
#            #  
#            ###### time, two dates, necessary ###
#            #
#            #  "start=yyyy-mm-dd-hh-MM" 
#            #
#            #  "end=yyyy-mm-dd-hh-MM" 
#            #
#            ##### users, list, optional ###
#            #
#            #  "users=[id1,id2,id3,...]"
#            #
#            ##### languages, list, optional ###
#            #
#            #  "languages=[en,es,pt,...]"
#            #
#            ###### boxes, list, optional ###
#            #
#            #  "boxes=[id1,id2,id3,...]"
#            #
#            ###
#            #   note: each id can look like a folder sequence of numbers, i.e.  
#            #
#            #             240, or, 240/46, or 240/46/2814
#            #
#            #         depending on the desired box depth
#            #
#            #
#            ###### boxnames, list, optional (same filter as boxes, but different keys) #########
#            #
#            #  "names=['name1','name2','name3',...]"
#            #
#            ###
#            #   note: each box name can look like a folder sequence of (utf8) names, i.e.
#            #
#            #              'United States', or, 'United States/Vermont', or 'United States/Vermont/Chittenden'
#            #
#            #         depending on the desired box depth
#            #
#            ######################################################################
#              #
######################################################################### sample call ##############################################################################################
#
# this should get you any english tweets from chttenden county by user 122138325 over the two days 6/2/14 and 6/3/14
#
# perl /path/to/pullTweets.pl -tblucm "start=2014-06-02-00-00" "end=2014-06-03-23-59" "destination=/path/to/outfile.txt" "users=[122138325]" "boxes=[240/46/2814]" "languages=[en]"
#
####################################################################################################################################################################################

### to do:
# -- make a bounding box filter
###

my $root = abs_path($0);
$root =~ s/\/pullTweets\.pl//;
my $start;
my $end;
my @sTIME;
my @eTIME;

my $destination = 0;

my @attributes;
my $attribute;
my %langs;
my @lans;
my $lan;
my %boxes;
my @boxs;
my $box;
my $lon;
my $lat;
my %users;
my @usrs;
my $usr;

my $curTime;
my $nexTime;
my @TIME;
my %names;
my @nams;
my $boxsize;
my $boxnums;
my @boxdata;
my $name;
my $year;
my $day;
my $file;
my $text;
my $command;
my $line;
my @lines;
my $bcheck;
my $lcheck;
my $ucheck;
my $country;
my $state;
my $county;
my $tweet;
my @data;
my $dataLine;
my $ret = 1;
my @flags;
my $flag;
my $t = 0;
my $b = 0;
my $m = 0;
my $l = 0;
my $u = 0;
my $c = 0;

@attributes = @ARGV;

foreach $attribute (@attributes){

    ### collect the span of time
    if ($attribute =~ m/^start\=(\d{4,4})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})$/i){
	$start = $attribute
    }
    if ($attribute =~ m/^end\=(\d{4,4})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})$/i){
	$end = $attribute;
    }

    ### check for a valid destination
    if ($attribute =~ m/^destination\=/i){
	$destination = $attribute;
	$destination =~ s/^destination\=//i;
	if (open(OUTFILE,">",$destination)){
	    close(OUTFILE);
	}
	else{
	    print "invalid destination: ".$destination."\n";
	    die;
	}
    }
    else{
	if (!($destination)){
	    $destination = 0;
	}
    }


    ### collect the filters
    if ($attribute =~ m/^languages\=\[(.*?)\]$/i){
	@lans = split("\,",$1);
	foreach $lan (@lans){
	    $langs{$lan} = 1;
	}
    }
    elsif ($attribute =~ m/^boxes\=\[(.*?)\]$/i){
	@boxs = split("\,",$1);
	foreach $box (@boxs){
	    $boxes{$box} = 1;
	}
    }
    elsif ($attribute =~ m/^names\=\[(.*?)\]$/i){
	@nams = split("\,",$1);
	foreach $name (@nams){
	    $names{$name} = 1;
	}
    }
    elsif ($attribute =~ m/^users\=\[(.*?)\]$/i){
	@usrs = split("\,",$1);
	foreach $usr (@usrs){
	    $users{$usr} = 1;
	}
    }

    ### collect the print flags
    if ($attribute =~ m/^\-([a-z]+)$/){
	@flags = split("",$1);
	foreach $flag (@flags){
	    if ($flag eq "t"){
		$t = 1;
	    }	    
	    if ($flag eq "m"){
		$m = 1;
	    }
	    if ($flag eq "b"){
		$b = 1;
	    }
	    if ($flag eq "l"){
		$l = 1;
	    }
	    if ($flag eq "u"){
		$u = 1;
	    }
	    if ($flag eq "c"){
		$c = 1;
	    }
	}
    }
}

### convert names into boxes and load
foreach $name (keys %names){
    $name =~ s/^\'//g;
    $name =~ s/\'$//g;
    $name =~ s/\//\t/g;
    utf8::decode($name);
    $boxsize = scalar(split("\t",$name));
    $boxnums = `grep \-P \"\^$name\" $root\/boxKeys\.txt \| perl \-wnE \'say for \/\\t\(\\d\+\)\\t\(\\d\+\)\\t\(\\d\+\)\\n\/g\'`;
    @boxdata = split("\n",$boxnums);
    if (scalar(@boxdata) >= 3){
	$box = join("\/",@boxdata[0..($boxsize-1)]);
	$boxes{$box} = 1;
    }
}


### clean up and check the span of time
if (($start =~ m/^start\=(\d{4,4})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})$/i) || ($end =~ m/^end\=(\d{4,4})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})\-(\d{2,2})$/i)){
    $start =~ s/^start\=//i;
    @sTIME = split("\-",$start);
    $end =~ s/^end\=//i;
    @eTIME = split("\-",$end);
    $curTime = $start;
}
else{
    print "invalid span of time\: ".$start." to ".$end."\n";
    die;
}

if (!(scalar(keys %users))){
    $users{"\*"} = 1;    
}
if (!(scalar(keys %langs))){
    $langs{"\*"} = 1;    
}
if (!(scalar(keys %boxes))){
    $boxes{"\*"} = 1;    
}

### subroutine check to see if the time is not after the end
sub before{
    my @cTIME = split("\-",$curTime);
    if ($cTIME[0] < $eTIME[0]){ ### check year
	$ret = 1;
    }
    elsif ($cTIME[0] == $eTIME[0]){
	if ($cTIME[1] < $eTIME[1]){ ### check month
	    $ret = 1;
	}
	elsif ($cTIME[1] == $eTIME[1]){
	    if ($cTIME[2] < $eTIME[2]){ ### check day
		$ret = 1;
	    }
	    elsif ($cTIME[2] == $eTIME[2]){
		if ($cTIME[3] < $eTIME[3]){ ### check hour
		    $ret = 1;
		}
		elsif ($cTIME[3] == $eTIME[3]){
		    if ($cTIME[4] <= $eTIME[4]){ ### check minute
			$ret = 1;
		    }
		    else{
			$ret = 0;
		    }
		}
		else{
		    $ret = 0;
		}
	    }
	    else{
		$ret = 0;
	    }
	}
	else{
	    $ret = 0;
	}
    }
    else{
	$ret = 0;
    }    
    return($ret);
}

### subroutine to get the next time
sub next{
    my @cTIME = split("\-",$curTime);
    my @nTIME = @cTIME;
    if ($nTIME[4] eq "59"){ ### move to next hour
	$nTIME[4] = "00";
	if($nTIME[3] eq "23"){ ### move to next day
	    $nTIME[3] = "00";
	    if ($nTIME[2] eq "31"){ ### move to next month
		$nTIME[2] = "01";
		if ($nTIME[1] eq "12"){ ### move to next year
		    $nTIME[1] = "01";
		    $nTIME[0] += 1;
		}
		else{
		    $nTIME[1] += 1;
		    if (length($nTIME[1]) == 1){
			$nTIME[1] = "0".$nTIME[1];
		    }
		}
	    }
	    else{ 
		$nTIME[2] += 1;
		if (length($nTIME[2]) == 1){
		    $nTIME[2] = "0".$nTIME[2];
		}
	    }
	}
	else{
	    $nTIME[3] += 1;
	    if (length($nTIME[3]) == 1){
		$nTIME[3] = "0".$nTIME[3];
	    }
	}
    }	
    else{
	$nTIME[4] += 1;
	if (length($nTIME[4]) == 1){
	    $nTIME[4] = "0".$nTIME[4];
	}
    }
    return(join("\-",@nTIME));
}

### collect the tweets
while ($ret){
    @TIME = split("\-",$curTime);
    $year = $TIME[0];
    $day = join("\-",@TIME[0..2]);
    $file = "/users/j/r/jrwillia/scratch/data/twitter/$year\/$day\/$curTime\.zip";    
    if ($destination){
	open(OUTFILE,">>",$destination);
    }
    else{
	*OUTFILE = *STDOUT;
    }
    ### get the tweets here
    if (open(INFILE,"<",$file)){
	close(INFILE);
	$command = "zless ".$file;
        $text = `$command`;
	utf8::decode($text);
        @lines = split("\n",$text);	
	foreach $line (@lines){
	    @data = ();
	    if ($line =~ m/(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$/){
                $country = $1;
                $state = $2;
                $county = $3;
		$lon = $4;
		$lat = $5;
		$usr = $6;
                $lan  = $7;
                $tweet = $8;		
		
		### check boxes for a match
		if (defined $boxes{"\*"}){
		    $bcheck = 1;
		}
		elsif (defined $boxes{$country}){
		    $bcheck = 1;
		}
		elsif (defined $boxes{$country."/".$state}){
		    $bcheck = 1;
		}
		elsif (defined $boxes{$country."/".$state."/".$county}){
		    $bcheck = 1;
		}
		else{
		    $bcheck = 0;
		}

		### check languages for a match
		if (defined $langs{"\*"}){
		    $lcheck = 1;
		}
		elsif (defined $langs{$lan}){
		    $lcheck = 1;
		}
		else{
		    $lcheck = 0;
		}

		### check users for a match
		if (defined $users{"\*"}){
		    $ucheck = 1;
		}
		elsif (defined $users{$usr}){
		    $ucheck = 1;
		}
		else{
		    $ucheck = 0;
		}
		
		### if all checks pass then print out the tweet
		if ($bcheck && $lcheck && $ucheck){
		    ### store data for the appropriate flags
		    if ($t){
			push(@data,$curTime);
		    }
		    if ($b){
			push(@data,$country."/".$state."/".$county);
		    }
		    if ($c){
			push(@data,"\[".$lon."\,".$lat."\]");
		    }
		    if ($l){
			push(@data,$lan);
		    }
		    if ($u){
			push(@data,$usr);
		    }
		    if ($m){
			push(@data,$tweet);
		    }
		    $dataLine = join("\t",@data);
		    print OUTFILE $dataLine."\n";
		    
		}
	    }
	}
    }
    ###
    if ($destination){
	close(OUTFILE);
    }
    $nexTime = &next;
    $curTime = $nexTime;
    $ret = &before;
}
