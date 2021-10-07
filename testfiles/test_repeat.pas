program repeatLoop;
var a: integer;
begin
   a := 0;
   repeat
      writeln(a);
      a := a + 1;
   until a = 6;
end.