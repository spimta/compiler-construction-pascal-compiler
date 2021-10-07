program switch;
var day: char;
begin
   day := '7';

   case ( day) of
      '1' : writeln('Monday');
      '2' : writeln('Tuesday');
      '3' : writeln('Wednesday');
      '4' : writeln('Thursday');
      '5' : writeln('Friday');
	  '6' : writeln('Satursday');
	  '7' : writeln('Sunday');
   end;
   writeln(day);
end.