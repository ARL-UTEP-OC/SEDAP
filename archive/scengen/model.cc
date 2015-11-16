e <= $now) {

	    DisplayPositions($next_time);		

	    if ($trace_on) {
		UndisplayEventsTill($CUR_TIME);
		DisplayEventsTill($next_time);
	    }
	    if ($show_originations) {
		DisplayOriginations($CUR_TIME, $next_time);
	    }

	    # advance time, since we've done all the events up to next_time
	    $CUR_TIME = $next_time;
	    $timepos_scale->set($CUR_TIME);
	    
	    if ($slave_to_ns) {
		CheckNSSlave();
	    }
	    if (int($CUR_TIME) != $last_attrib_time) {
		$last_attrib_time = $CUR_TIME;
		DoNodeAttributes();
	    }

            DoOneEvent(DONT_WAIT | ALL_EVENTS);


	    if ($now - $scheduled_time > 1.0) { 
		$b = sprintf("%f   behind %f secs", $CUR_TIME, 
			     $now - $scheduled_time);
		Msg($b);
# changing the background when we get behind is too visually distracting
#		$CANVAS->configure(-background => $behind_canvas_bkgnd);
		$speed_scale->set($speed_scale->get() + 1);
	    } else {
		Msg("Time: $CUR_TIME");
# changing the background when we get behind is too distracting
#		$CANVAS->configure(-background => $normal_canvas_bkgnd);
	    }
	} else {

	    if ($skip && $trace_on) {
		$CUR_TIME = PeekNextEventTime();
		$skip = 0;
		$reset_time = 1;
	    }

	    # sleep for a bit, calling doonevent periodically if needed

	    # I'm disabling the sleep loop by setting $again to 0
	    # to avoid the annoying problem of the display freezing when
	    # you move the mouse while the nodes are running b/c the stupid
	    # perlTK has to loop through here until all the mouse events
	    # are drained from the queue and the draw events can happen.
	    # -dam 6/17/98

	    my $again = 0;
	  PAUSE_LOOP: while ($again && ! $skip && ! $reset_time) {
	      my $t = $scheduled_time - $now;
	      if ($t > 0.05) {
		  $t = 0.05; 
		  $again = 1;
	      } else { $again = 0; }

	      select(undef, undef, undef, $t);
	      if (! $again ) { last PAUSE_LOOP; }

	      DoOneEvent(DONT_WAIT | ALL_EVENTS);
#	      print WriteTime "\n";
#	      $now = <ReadTime>;
	      $now = $now + $t;
	  }
	}

	
    }

    if ($CUR_TIME >= $MAX_TIME ) {
	if ($autorewind) { 
	    toggle_display; 
	    change_time(0);
	    toggle_display; 
	} elsif ($running) { 
	    toggle_display;
	}
    }
}

exit;

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
sub MacfilterServer {
    my ($msg_recv_time, $now);
    my $msg;

    ClearAllNoAsk();

    my $paddr = sockaddr_in($MAC_PORT, INADDR_ANY);
    socket(S,PF_INET,SOCK_DGRAM,0) 
	or Msg("Can't get MAC server socket: $!") and return;
    bind(S,$paddr) or die "bind: $!";

    # should make this a spin wait on a select checking to see if
    # user unsets the wait_for_macfilter_server
    recv(S,$msg,$MAC_MSG_LEN,0) or die "recv $!";

    # get current time 
    print WriteTime "\n";
    $msg_recv_time = <ReadTime>;

    my ($scen_name, $wait_time) = unpack($MAC_MSG_FORMAT, $msg);
    
    $default_scenario = $scen_name;
    $default_trace = "";
    $default_commpattern = "";
    ReadScenario($default_scenario);
    change_time(0);
    $speed_scale->set(10);
    ConfigureUI();

    $msg_recv_time += ($wait_time / 1000.0);

    print WriteTime "\n";
    $now = <ReadTime>;

    if ($now < $msg_recv_time ) {
	select(undef, undef, undef, $msg_recv_time - $now);
    }
};

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

sub add_node {

    # node numbers are 1 based, so we inc first, then setup
    $NN++;

    my $index = $NUM_TIMES[$NN];
    $MOVE[$NN]->[$index]->[$TIME] = 0.0;
    $MOVE[$NN]->[$index]->[$TOY] = 10.0;
    $MOVE[$NN]->[$index]->[$TOX] = 10.0;
    $MOVE[$NN]->[$index]->[$SPEED] = 0.0;
    $NUM_TIMES[$NN]++;    

    display_waypoints($NN);
    $idscale->configure(-to => $NN);
};

###########################################################################
###########################################################################
###########################################################################
sub edit_entry;
sub build_entries;
sub add_waypoint;
sub ToggleWaypointHighlight;
sub ExtendWaypointHighlight;
sub SaveRange;
sub PasteSavedRange;

sub trace_name {
    my ($n) = @ARG;
    return "trace-$n";
  
}

sub undisplay_waypoints {
    my ($node) = @ARG;

    $CANVAS->delete(trace_name($node));
    if ($WP[$node]->{MW} ne "") {
	$WP[$node]->{MW}->destroy();
	$WP[$node]->{MW} = "";
    }
    if ($EDIT[$node]->{MW} != '') {
	$EDIT[$node]->{MW}->destroy();
	$EDIT[$node]->{MW} = '';
    }
};

sub display_waypoints {
    my ($node) = @ARG;

    $CANVAS->raise(trace_name($node));

    if ($WP[$node]->{MW} ne "") {
	Msg("Waypoints already displayed for node $node");
	return;
    }

    $WP[$node]->{highlight_start} = -1;

    $WP[$node]->{MW} = MainWindow->new;
    $WP[$node]->{MW}->title("Node $node");

    ## make the waypoint listbox
    $WP[$node]->{wplistframe} = $WP[$node]->{MW}->Frame(
               -borderwidth => 2,
               -width => '15c',
               );
    $WP[$node]->{wplistframe}->pack(-side => 'top', -expand => 'yes', -fill => 'y');
    $WP[$node]->{wplistscroll} =  $WP[$node]->{wplistframe}->Scrollbar;
    $WP[$node]->{wplistscroll}->pack(-side => 'right', -fill => 'y');
    $WP[$node]->{wplist} = $WP[$node]->{wplistframe}->Listbox(
        -yscrollcommand => [$WP[$node]->{wplistscroll} => 'set'],
        -setgrid        => 1,
        -height         => 15,
        -width          => 60,
	-selectbackground => $waypoint_highlight_color,
    );
    $WP[$node]->{wplistscroll}->configure(-command => [$WP[$node]->{wplist} => 'yview']);
    $WP[$node]->{wplist}->pack(-side => 'left', -expand => 'yes', -fill => 'both');

    ## make the controls
    $WP[$node]->{cntframe1} = $WP[$node]->{MW}->Frame(-borderwidth => 2,);
    $WP[$node]->{cntframe1}->{addwp} =  $WP[$node]->{cntframe1}->Button(
			       -text => "Add Waypoint",
#			       -width => 10,
			       -command => sub {add_waypoint($node)},
			       );
    $WP[$node]->{cntframe1}->{addwp}->pack(-side => 'left', -expand => 'yes');

    $WP[$node]->{cntframe1}->{edit} =  $WP[$node]->{cntframe1}->Button(
			       -text => "Edit",
#			       -width => 10,
			       -command => sub {edit_entry($node)},
			       );
    $WP[$node]->{cntframe1}->{edit}->pack(-side => 'left', -expand => 'yes');

    $WP[$node]->{cntframe1}->{edit} =  $WP[$node]->{cntframe1}->Button(
			       -text => "Delete Waypoint",
#			       -width => 10,
			       -command => sub {delete_waypoint($node)},
			       );
    $WP[$node]->{cntframe1}->{edit}->pack(-side => 'left', -expand => 'yes');

    $WP[$node]->{cntframe2} = $WP[$node]->{MW}->Frame(-borderwidth => 2,);
    $WP[$node]->{cntframe2}->{saverange} =  $WP[$node]->{cntframe2}->Button(
			       -text => "Save Range",
			       -command => sub {SaveRange($node);},
			       );
    $WP[$node]->{cntframe2}->{saverange}->pack(-side => 'left', -expand => 'yes');

    $WP[$node]->{cntframe2}->{pasterange} =  $WP[$node]->{cntframe2}->Button(
			       -text => "Paste Saved Range",
			       -command => sub {PasteSavedRange($node);},
			       );
    $WP[$node]->{cntframe2}->{pasterange}->pack(-side => 'left', -expand => 'yes');

    $WP[$node]->{cntframe2}->{close} =  $WP[$node]->{cntframe2}->Button(
			       -text => "Close",
#			       -width => 10,
			       -command => sub {undisplay_waypoints($node);},
			       );
    $WP[$node]->{cntframe2}->{close}->pack(-side => 'left', -expand => 'yes');

    $WP[$node]->{cntframe1}->pack();
    $WP[$node]->{cntframe2}->pack();

    $WP[$node]->{wplist}->insert(0,build_entries($node));
    display_movetrace($node);

    DoOneEvent(DONT_WAIT | ALL_EVENTS);

    ####
    $WP[$node]->{wplist}->bind('<Double-1>' => sub { edit_entry($node)},);
    $WP[$node]->{wplist}->bind('<Button-1>' => 
			       [sub {ToggleWaypointHighlight(@ARG)},$node],);
    $WP[$node]->{wplist}->bind('<B1-Motion>' => 
			       [sub {ExtendWaypointHighlight(@ARG)},$node],);
    ####

};

sub SaveRange {
    my ($node) = @ARG;
    if (-1 == $WP[$node]->{highlight_start}) {
	Msg("No range of waypoints highlighted");
	return;
    }
    @SAVED_MOVE = [];
    my ($i, $j);
    for ($i = $WP[$node]->{highlight_start}, $j = 0; 
	 $i <= $WP[$node]->{highlight_stop}; $i++, $j++) {
	@SAVED_MOVE[$j] = @MOVE[$node]->[$i];
    }
    Msg("Waypoints $WP[$node]->{highlight_start} to $WP[$node]->{highlight_stop} saved to clipboard");
    ToggleWaypointHighlight(0,$node);
}

sub WaypointCompletionTime {
    my ($node,$wp) = @ARG;
    my ($dx, $dy, $dt, $d);
    
    if (0 == $wp) {return 0;}

    $dx = $MOVE[$node]->[$wp]->[$TOX] - $MOVE[$node]->[$wp-1]->[$TOX];
    $dy = $MOVE[$node]->[$wp]->[$TOY] - $MOVE[$node]->[$wp-1]->[$TOY];
    $d = sqrt($dx * $dx + $dy * $dy);
    $dt = $MOVE[$node]->[$wp]->[$PT] + $d / $MOVE[$node]->[$wp]->[$SPEED];
    return $dt;
}

sub PasteSavedRange {
    my ($node) = @ARG;
    my ($i,$j,$insert_len);
    my ($dx, $dy, $dt, $d);

    if (-1 == $#SAVED_MOVE) {
	Msg("No saved region");
    }

    if (0 == $SAVED_MOVE[0]->[$SPEED]) {
	Msg("Can't paste in a saved range that includes a starting point");
	return;
    }

    my $wp = $WP[$node]->{wplist}->index('active');
    $wp += 1;    #insert after the selected waypoint

    print "wp is $wp\n";

#    print "Saved move\n";
#    dumpValue(\@SAVED_MOVE);
#    print "before paste\n";
#    dumpValue(\@MOVE[$node]);
    
    $insert_len = $#SAVED_MOVE + 1;
    for ($i = $NUM_TIMES[$node] + $insert_len - 1;
	 $i >= $wp + $insert_len;
	 $i--) {
	$MOVE[$node]->[$i] = @MOVE[$node]->[$i - $insert_len];
    }
    $NUM_TIMES[$node] += $insert_len;

#    print "after shift\n";
#    dumpValue(\@MOVE[$node]);
	 
    for ($j = 0; $j < $insert_len; $j++) {
	# need to make a copy of the saved_move, since we don't want sharing
	#  I just can't understand Perl's model of references well enough to
	#  do this copy in a reasonable fashion.  perl-- -dam 9/23/98
	my $cur = $wp + $j;
	$MOVE[$node]->[$cur] = [];
	$MOVE[$node]->[$cur]->[$TIME] = $SAVED_MOVE[$j]->[$TIME];
	$MOVE[$node]->[$cur]->[$SPEED] = $SAVED_MOVE[$j]->[$SPEED];
	$MOVE[$node]->[$cur]->[$TOX] = $SAVED_MOVE[$j]->[$TOX];
	$MOVE[$node]->[$cur]->[$TOY] = $SAVED_MOVE[$j]->[$TOY];
	$MOVE[$node]->[$cur]->[$PT] = $SAVED_MOVE[$j]->[$PT];

	#now fix up the start time of the new current waypoint
	$MOVE[$node]->[$cur]->[$TIME] = $MOVE[$node]->[$cur-1]->[$TIME] 
	    + WaypointCompletionTime($node,$cur-1);
    }

#    print "after paste\n";
#    dumpValue(\@MOVE[$node]);

    # now adjust the times of all following waypoints
    my $insert_stop_time = $MOVE[$node]->[$wp + $insert_len - 1]->[$TIME] + 
	WaypointCompletionTime($node, $wp + $insert_len - 1);
    my $time_delta = $insert_stop_time - $MOVE[$node]->[$wp + $insert_len]->[$TIME];
    for ($i = $wp + $insert_len; $i < $NUM_TIMES[$node] ; $i++) {
	$MOVE[$node]->[$i]->[$TIME] += $time_delta;
    }

    $CANVAS->delete(trace_name($node));
    display_movetrace($node);

    $WP[$node]->{wplist}->delete(0,'end');
    $WP[$node]->{wplist}->insert(0,build_entries($node));
}

###########################################################################
###########################################################################
sub finish_edit {
    my ($node,$wp) = @ARG;

    if (abs($EDIT[$node]->{ox} != 0 + $EDIT[$node]->{x}->get()) > $EP 
	|| abs($EDIT[$node]->{oy} != 0 + $EDIT[$node]->{y}->get()) > $EP) {
	update_waypoint_position($node,$wp, $EDIT[$node]->{x}->get(),
				 $EDIT[$node]->{y}->get());
    }
    
    if ($wp != 0
	&& abs($EDIT[$node]->{otime} != 0 + $EDIT[$node]->{time}->get()) > $EP) {
	update_waypoint_time($node, $wp, $EDIT[$node]->{time}->get());
    }
    
    if ($wp != 0
	&& abs($EDIT[$node]->{opt} != 0 + $EDIT[$node]->{pt}->get()) > $EP) {
	update_waypoint_pt($node, $wp, $EDIT[$node]->{pt}->get());
    }

    if ($wp != 0
	&& abs($EDIT[$node]->{ospeed} - $EDIT[$node]->{speed}->get()) > $EP) {
	update_waypoint_speed($node, $wp, $EDIT[$node]->{speed}->get());
    }

    $WP[$node]->{wplist}->delete(0,'end');
    $WP[$node]->{wplist}->insert(0,build_entries($node));

    $EDIT[$node]->{MW}->destroy();
    $EDIT[$node]->{MW} = '';
};

sub edit_entry {
    my ($node) = @ARG;

    my $wp = $WP[$node]->{wplist}->index('active');
#    print $WP[$node]->{wplist}->get('active');
#    print " index $wp\n";

    if ($EDIT[$node]->{MW} != '') {
	Msg("First close existing waypoint edit window for node $node!");
	return;
    }
     
    $EDIT[$node]->{ox} = $MOVE[$node]->[$wp]->[$TOX];
    $EDIT[$node]->{oy} = $MOVE[$node]->[$wp]->[$TOY];
    $EDIT[$node]->{otime} = $MOVE[$node]->[$wp]->[$TIME];
    $EDIT[$node]->{ospeed} = $MOVE[$node]->[$wp]->[$SPEED];
    $EDIT[$node]->{opt} = $MOVE[$node]->[$wp]->[$PT];

#    print "time is  $EDIT[$node]->{otime} old is \n";

    $EDIT[$node]->{MW} = MainWindow->new;
    $EDIT[$node]->{M