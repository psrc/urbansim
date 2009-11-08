// Example Ben-Akiva & Lerman (1985) p. 88
// Michel Bierlaire, EPFL (c) 2002

[Choice]
choice

[Beta]
// Name Value  LowerBound UpperBound  status (0=variable, 1=fixed)
beta1      0.0     -100.0     100.0         0
beta2      0.0     -100.0     100.0         0

[Utilities]
// Id Name  Avail  linear-in-parameter expression (beta1*x1 + beta2*x2 + ... )
1 	Auto	avail	beta1 * one + beta2 * time_1
2	Bus	avail	beta2 * time_2

[Expressions]
// Define here arithmetic expressions for name that are not directly
// available from the data
one = 1
avail = 1

[Model]
// Currently, only $MNL (multinomial logit), $NL (nested logit), $CNL
// (cross-nested logit) and $NGEV (Network GEV model) are valid keywords
$MNL


