// This is automatically generated biogeme model file.
[Choice]
choice

[Beta]
// Name	Value	LowerBound	UpperBound	status (0=variable, 1=fixed)
costcoef	0.0	-100.0	100.0	0

[Utilities]
// Id	Name	Avail	linear-in-parameter expression (beta1*x1 + beta2*x2 + ... )
1	A1 	avail	costcoef * cost_1 
2	A2 	avail	costcoef * cost_2 
3	A3 	avail	costcoef * cost_3 
4	A4 	avail	costcoef * cost_4 
5	A5 	avail	costcoef * cost_5 
6	A6 	avail	costcoef * cost_6 
7	A7 	avail	costcoef * cost_7 
8	A8 	avail	costcoef * cost_8 
9	A9 	avail	costcoef * cost_9 

[Expressions]
constant = 1
avail = 1

[Model]
$MNL
