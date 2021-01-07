use Encode;

sub Train
{
	open(In,"Person.txt");
	open(Out1,">Model.txt");
	while(<In>){
		chomp;
		if(/,Î´Öª/){
			next;
		}
		
		if(/(\S+),(\S+)/){
			$Sex=$2;
			$Name=$1;
		}
		$Name=decode("gbk",$Name);
		@HZs=$Name=~/./g;
		for($i=0;$i<@HZs;$i++){
			${$Prob{$HZs[$i]}}{$Sex}++;
			$Total++;
		}
	}
	close(In);

	$Val=log(1/$Total);
	print Out1 "UNK $Val\n";
	foreach (sort keys %Prob){
			$Ref=$Prob{$_};
			$HZ=encode("gbk",$_);
			print Out1 "#$HZ\n";
			print Out2 "#$HZ\n";
			foreach (sort keys %{$Ref}){
				$Val=log(${$Ref}{$_}/$Total);
				print Out1  "$_ $Val\n";
			}	
	}

	close(Out1);
}

sub ReadModel
{
	my($File,$Ref,$RefUNK)=@_;
	open(In,"$File");
	$Line=<In>;
	if($Line=~/(\S+)\s(\S+)/){
		${$RefUNK}=$2;
	}
	while(<In>){
		chomp;
		if(/#(\S+)/){
			$HZ=$1;
		}else{
			if(/(\S+)\s(\S+)/){
				${${$Ref}{$HZ}}{$1}=$2;
			}
		}
	}
	close(In);
}

sub GetProb
{
	my($Ref,$RefUNK,$HZ,$Sex)=@_;
	if( not defined ${$Ref}{$HZ}){
		return ${$RefUNK};
	}
	
	if ( defined ${${$Ref}{$HZ}}{$Sex} ){
		return ${${$Ref}{$HZ}}{$Sex};
	}
	return ${$RefUNK};
}

sub Bayes
{
	my($Name,$Ref,$RefUNK)=@_;

	$Name=decode("gbk",$Name);
	@HZs=$Name=~/./g;
	$ProbMale=0;
	$ProbFemale=0;
	for($i=0;$i<@HZs;$i++){
		$HZ=encode("gbk",$HZs[$i]);
		$Male=GetProb($Ref,$RefUNK,$HZ,"ÄÐ");
		$Female=GetProb($Ref,$RefUNK,$HZ,"Å®");
		$ProbMale+=$Male;
		$ProbFemale+=$Female;
	}
	$Ret="Female";
	if( $ProbMale > $ProbFemale){
		$Ret="male";
	}
	return $Ret;
}

sub Main
{
	ReadModel("Model.txt",\%Model,\$UNK);

	while(1){
		print "Pls Name:";
		$Name=<stdin>;
		chomp($Name);
		$Ret=Bayes($Name,\%Model,\$UNK);	
		print "$Ret\n";
	}
}

#Train();
Main();