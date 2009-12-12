#! /opt/perl/bin/perl



=pod

=head1 NAME
 
RT_backup.pl-backup the RT databases

=head1 DESCRIP

Issues several system commands to backup the MySQL databases containing
    the RT instance

=head1 USAGE

Should be run as cron from an account that has read access to the config
    files, so that it can access the db, and then has write access to the
    backups dir.


-b : backup directory, defaults to /opt/rt3/var/bu



=head1 DETAILS

All backups are nightly, then this means that if the backup runs before
    you restore, you'll backup the corrupted databases.




=head2 MySQL

Uses mysqldump to do the db files, to restore from this dump on a clean
    mysql (ie. no existing rt3 db, login to mysql as rt_user and do

 CREATE DATABASE rt3;    (or tis_rt3)

Then from the command line:

 mysql --user=rt_user -p rt3 < rt3_bu.sql

If you already have an rt3 database, you should probably

 DROP DATABASE rt3;

before the above command.


=cut


use lib ("/opt/rt3/local/lib", "/opt/rt3/lib");



use Getopt::Std;

my %args=();

getopts('b:l',\%args);


my $bu_dir=$args{b} || '/opt/rt3/var/bu/';

if ($args{l}){
    my $log_dir="$bu_dir/logs";
    my ($day,$month,$year) = (localtime)[3,4,5];
    my $date=sprintf("%04d%02d%02d",$year+1900, $month+1, $day);
    my $logfile="$log_dir/$date-$$.log";
    open(LOGFILE,">$logfile") || warn "error creating Logfile";
};

my $err_tmp="$bu_dir/tmp.err";



use RT;

RT::LoadConfig();

my $user=$RT::DatabaseUser;   #reading from RT_SiteConfig
my $pw=$RT::DatabasePassword;
my $db=$RT::DatabaseName;


my $bu_file="$bu_dir/${db}_bu.sql";

$options = "--skip-opt --add-drop-table --add-locks --create-options --quick 
--extended-insert --set-charset --disable-keys "; 

#Database dump direct to backup dir

$command="/usr/bin/mysqldump $options --user=$user --password=$pw  $db >$bu_file 2> $err_tmp";

system("$command");

open(ERRS,"<$err_tmp");
@stderr=<ERRS>;
close(ERRS);

$command=~s/$pw/****/;

if ($args{l}){
    print LOGFILE "Attempted:\n $command\n Results:\n";
    print LOGFILE @stderr;
    close (LOGFILE);
}





=head1 BUGS

Plenty-most are unknown

This is still in development


=head1 AUTHOR

Travis C. Brooks  travis@SLAC.stanford.edu


=head1 COPYRIGHT

2006, Travis Brooks, Stanford Linear Accelerator Center 

=cut

