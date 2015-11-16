rig($OrigList);
};

sub DeleteSrc {
    my ($list) = @ARG;
    DeleteOrig($list->index('active'));
    ShowOrig($list);
};

sub AddCBRSrc {
    my ($list) = @ARG;

    my $W = MainWindow->new;
    $W->title('Add CBR Source');

    my $cancel = sub {
	Msg("Canceled...");
	$W->destroy;
    };

    my $text = $W->Text(-font => $FONT, -width => 40, -height => 1,
			-relief => 'sunken')->pack(-side =>'top');

    $text->delete('1.0','end');
    $text->insert('1.0','Left click on source node now');

    my $l1 = $W->Frame();
    $l1->pack(-side => 'top');
    my $n1 = $l1->Entry(-relief => 'sunken', -width => 4,);
    $l1->Label(-text => 'From node:')->pack(-side => 'left');
    $n1->pack(-side => 'left');
    my $from_node = GetNode();
    if ($from_node < 0) {&$cancel(); return;}
    $n1->insert(0,$from_node); 

    $text->delete('1.0','end');
    $text->insert('1.0','Left click on destination node now');

    my $n2 = $l1->Entry(-relief => 'sunken', -width => 4,);
    $l1->Label(-text => 'To node:')->pack(-side => 'left');
    $n2->pack(-side => 'left');
    my $to_node = GetNode();
    if ($to_node < 0) {&$cancel(); return;}
    $n2->insert(0,$to_node); 

    $text->delete('1.0','end');
    $text->insert('1.0','Set parameters and hit okay or cancel');

    my $l2 = $W->Frame();
    $l2->pack(-side => 'top');
    $l2->Label(-text => 'Number pkts:')->pack(-side => 'left');
    my $count = $l2->Entry(-relief => 'sunken',);
    $count->pack(-side => 'left', -fill => 'x', -expand => 1);
    $count->insert(0,10);
    
    my $l3 = $W->Frame();
    $l3->pack(-side => 'top');
    $l3->Label(-text => 'Pkts per sec:')->pack(-side => 'left');
    my $rate = $l3->Entry(-relief => 'sunken',);
    $rate->pack(-side => 'left', -fill => 'x', -expand => 1);
    $rate->insert(0,10);

    my $l4 = $W->Frame();
    $l4->pack(-side => 'top');
    $l4->Label(-text => 'Pkt size (bytes):')->pack(-side => 'left');
    my $size = $l4->Entry(-relief => 'sunken',);
    $size->pack(-side => 'left', -fill => 'x', -expand => 1);
    $size->insert(0,512);

    my $done = sub {
	my $t;

	if (int($CUR_TIME) == $timepos_scale->get()) {
	    $t = $CUR_TIME;
	} else {
	    $t = $timepos_scale->get();
	}

	InsertOrig($t, 'cbr',
		   int($n1->get()),
		   int($n2->get()),
		   int($count->get()),
		   int($rate->get()),
		   int($size->get()));
	ShowOrig($list);	
	$W->destroy();
    };

    my $l5 = $W->Frame();
    $l5->pack(-side => 'top', -pady => 5);

    $l5->Button(-text => "Okay", -command => $done,
	       )->pack(-side => 'left', -expand => 'yes', -padx => 3);
    $l5->Button(-text => "Cancel", 
		-command => $cancel,
	       )->pack(-side => 'left', -expand => 'yes', -padx => 3);
};


sub AddTCPSrc {
    my ($list) = @ARG;

    my $W = MainWindow->new;
    $W->title('Add TCP Source');

    my $cancel = sub {
	Msg("Canceled...");
	$W->destroy;
    };

    my $text = $W->Text(-font => $FONT, -width => 40, -height => 1,
			-relief => 'sunken')->pack(-side =>'top');

    $text->delete('1.0','end');
    $text->insert('1.0','Left click on source node now');

    my $l1 = $W->Frame();
    $l1->pack(-side => 'top');
    my $n1 = $l1->Entry(-relief => 'sunken', -width => 4,);
    $l1->Label(-text => 'From node:')->pack(-side => 'left');
    $n1->pack(-side => 'left');
    my $from_node = GetNode();
    if ($from_node < 0) {&$cancel(); return;}
    $n1->insert(0,$from_node); 

    $text->delete('1.0','end');
    $text->insert('1.0','Left cli