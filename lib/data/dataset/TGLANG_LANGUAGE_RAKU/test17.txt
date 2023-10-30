unit module Test::Lab;

use Test::Lab::Experiment;

#| The default context data for an experiment created and run via the
#| C<lab> helper sub.  Override this in any class that inherits Test::Lab
#| to define your own behavior
our %context = Hash.new;

#| Change the default Experiment class to instantiate by modifying
#| this variable.
our $experiment-class = Test::Lab::Experiment;

#| Define and run a lab experiment
#|
#| $name - name for this experiment
#| &procedure - routine that takes an experiment & lays out groups and context.
#| $run - name of the test to run
#|
#| Yields an object which implements the Test::Lab::Experiment interface.
#| See `Test::Lab::Experiment.new` for how this is defined.
#|
#| Returns the calculated value of the given $run experiment, or throws
#| if an exception was thrown.
multi sub run (Str:D $name, &block) is export {
  my $experiment = $experiment-class.new(:$name);
  &block($experiment);
  $experiment.run('control');
}
multi sub run (Str:D $name, $run-name, &block) is export {
  my $experiment = $experiment-class.new(:$name);
  &block($experiment);
  $experiment.run($run-name);
}

#| Define and run a lab experiment
#|
#| $name - name for this experiment
#| &procedure - routine that takes an experiment & lays out groups and context.
#| $run - name of the test to run
#|
#| Yields an object which implements the Test::Lab::Experiment interface.
#| See `Test::Lab::Experiment.new` for how this is defined. The package %context from
#| will be applied to the experiment.
#|
#| Returns the calculated value of the given $run experiment, or throws
#| if an exception was thrown.
multi sub lab (Str:D $name, &cb) is export {
  run $name, -> Test::Lab::Experiment:D $experiment {
    $experiment.context(|%context);
    &cb($experiment);
  }
}
multi sub lab (Str:D $name, Str:D $run-name, &cb) is export {
  run $name, $run-name, -> Test::Lab::Experiment:D $experiment {
    $experiment.context(|%context);
    &cb($experiment);
  }
}
multi sub lab (Str:D $name, Nil $run-name, &cb) is export {
  run $name, -> Test::Lab::Experiment:D $experiment {
    $experiment.context(|%context);
    &cb($experiment);
  }
}
