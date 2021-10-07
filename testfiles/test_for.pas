program loop;
var i,a: integer;
begin
    a := 0;
	for i := 0 to 5 do
	begin
	    a := a + i;
	    writeln(a);
	end;
end.