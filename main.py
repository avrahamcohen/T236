'''
Variable: openCurrent(0), openOnePrevious(0);
Variable: closeOnePrevious(0), closeCurrent(0);

Variables: OverSold(20), OverBought(80);
Variables: stochasticCurrentValue(0), stochastiOnePreviousValue(0), stochastiTwoPreviousValue(0), stochastiThreePreviousValue(0);
variables: var0(0), var1(0), var3(0);
variables: var00(0), var11(0), var33(0);
variables: var000(0), var111(0), var333(0);
variables: var0000(0), var1111(0), var3333(0);

Variables: trailValueLong(0), trailExitLong(0);
Variables: trailValueShort (0), trailExitShort(0);

openCurrent = 0.5 * (Open[1] + Close[1]);
openOnePrevious = 0.5 * (Open[2] + Close[2]);
closeCurrent = 0.25 * (Open + High + Low + Close);
closeOnePrevious = 0.25 * (Open[1] + High[1] + Low[1] + Close[1]);

Value1 = Stochastic(High, Low, Close, 12, 3, 3, 1, var0, var1, stochasticCurrentValue, var3);
Value2 = Stochastic(High[1], Low[1], Close[1], 12, 3, 3, 1, var00, var11, stochastiOnePreviousValue, var33);
Value3 = Stochastic(High[2], Low[2], Close[2], 12, 3, 3, 1, var000, var111, stochastiTwoPreviousValue, var333);
Value4 = Stochastic(High[3], Low[3], Close[3], 12, 3, 3, 1, var0000, var1111, stochastiThreePreviousValue, var3333);

if ((closeCurrent > openCurrent) and (closeOnePrevious < openOnePrevious)) then Begin
	// Market Up
	// If Stochastic above 20 and was below 20 in at least 4 last bars
	if ((stochasticCurrentValue > OverSold) and ((stochastiOnePreviousValue < OverSold) or (stochastiTwoPreviousValue < OverSold) or (stochastiThreePreviousValue < OverSold))) then Begin
		Buy at this bar;
		setdollartrailing(15);
	End;
End;

if ((closeCurrent < openCurrent) and (closeOnePrevious > openOnePrevious)) then Begin
	// Market Down
	// If Stochastic below 80 and was above 80 in at least 4 last bars
	if ((stochasticCurrentValue < OverBought) and ((stochastiOnePreviousValue > OverBought) or (stochastiTwoPreviousValue > OverBought) or (stochastiThreePreviousValue > OverBought))) then Begin
		Sellshort at this bar;
		setdollartrailing(15);
	End;
End;
'''

from initialization import initialization

if __name__ == '__main__':
    initialization()