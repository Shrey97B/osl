use WWW::Mechanize ();
use utf8;
use open ':std', ':encoding(UTF-8)';
use HTML::TreeBuilder::XPath;
use feature 'say';

print "Please enter the name of show:";
$show_name = <>;

$show_name = join('-', split(' ',$show_name));

my $mech = WWW::Mechanize->new();
my $url = "https://www.thetvdb.com/series/" . $show_name; 

$fildata = "";

$fildata = $fildata . "URL = " . $url . "\n";
$mech->get( $url );

my $tree = HTML::TreeBuilder::XPath->new_from_content( $mech->content() );

my @title = $tree->findnodes('//head/title');

$str = "";

for $t (@title){
      $str =  $t->as_text;
}

if($str eq "Series :: TheTVDB"){
      print("Please check the name of series or enter in proper format");
}
else{
  my @trips= $tree->findnodes( '//div[@class="change_translation_text"]');

  $fildata = $fildata . " Description of the show: ";
  foreach $trip2 (@trips){


      $lang = $trip2->attr('data-language');
      if($lang eq "en"){
        $para = $trip2->findvalue('./p');
        $fildata = $fildata . $para . "\n";
            
      }
      
          
  }



  my @actors= $tree->findnodes( '//div[@class="row thumbnail-mousey"]/div[@class="col-xs-6 col-sm-4 col-md-3"]/a/div[@class="thumbnail"]');

  $fildata = $fildata . "\n Actors:  \n";
  foreach $act (@actors){

      my $a = $act->findvalue('./h3');
      my $b  = $act->findvalue('./h3/small');
      my $alen = length($a);
      my $blen = length($b);
      
      my $cx = 0;
      $cx = $alen - $blen;
      
      $subs = substr($a,0,$cx);
      $fildata = $fildata . "\t" . $subs . " " . $b . "\n";
      
  }
  
    $fildata = $fildata . "\n Details of " . $show_name . " ";
  my @info = $tree->findnodes( '//div[@id="series_basic_info"]/ul[@class="list-group"]/li');

  foreach $inf (@info){
        
        my $key =  $inf->findvalue('./strong');
        my $val =  $inf->findvalue('./span');
        
        $fildata = $fildata . "\t" . $key . " : " . $val . "\n";
  }
  
  print $fildata;
  my $filename = 'Description.txt';
  open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
  print $fh $fildata;
  close $fh;
  system("notepad.exe Description.txt");
  
  }
