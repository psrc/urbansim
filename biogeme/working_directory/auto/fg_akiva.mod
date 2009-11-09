// This is automatically generated biogeme model file.
[Choice]
choice

[Beta]
// Name	Value	LowerBound	UpperBound	status (0=variable, 1=fixed)
beta2	0.0	-100.0	100.0	0
beta1	0.0	-100.0	100.0	0

[Utilities]
// Id	Name	Avail	linear-in-parameter expression (beta1*x1 + beta2*x2 + ... )
1	A1 	avail	beta2 * time_1 + beta1 * constant 
2	A2 	avail	beta2 * time_2 

[Expressions]
constant = 1
avail = 1

[Model]
$MNL
