my @world = "input".IO.lines.map({ .comb });

my $height = @world.elems;
my $width  = @world[0].elems;

my $product = 1;
for [1,1], [3,1], [5,1], [7,1], [1,2] -> ($dx, $dy) {
    my ($y, $x, $trees) = (0, 0, 0);

    while $y < $height {
        $trees++ if @world[$y][$x] eq '#';

        $y += $dy;
        $x += $dx;
        $x %= $width;
    }
    say "right $dx, down $dy -> $trees trees";

    $product *= $trees;
}
say "Product: $product";
