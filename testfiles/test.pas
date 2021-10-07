program if_statement;
var x, y: integer;
var z : string;
begin
	x := 3.5;
    y := 15;
    z := 'black';
	if ( x < y) then
		x := x * 2;

	writeln(x);
	writeln(y);
	writeln(z);
end.