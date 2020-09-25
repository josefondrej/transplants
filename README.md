# Transplant Matching

Web application providing endpoint for solving the 
[kidney-exchange problem](https://en.wikipedia.org/wiki/Kidney_Paired_Donation) 
that uses compatibility in [blood type](#blood_types)
and in the [human leukocyte antigen](#hla) (HLA)
system to evaluate compatibility.   

## Installation

### Native
Requires [anaconda](https://docs.anaconda.com/anaconda/install/). 
To create anaconda environment run: 
```commandline
make conda-create
```


## Medical Background

### Blood Types <a name="blood_types"></a>

Humans have 4 basic blood types `0`, `A`, `B`, `AB`. Those have 
different antigens in red blood cells and different antibodies in plasma. 

|   | 0 | A | B | AB |
|---|---|---|---|----|
| antibodies in plasma | anti-A and anti-B | anti-B | anti-A | none |
| antigens in red blood cell | none | A antigen | B antigen | A and B antigens |

Two people with the same blood group are compatible (in blood group). 
In addition to this also pairs of donor (columns) - recipient (rows) described 
by the following table are also compatible.  

| donor  &nbsp;&#9656; <hr>recipient &#9660;| 0 | A | B | AB |
|:---|---|---|---|---|
| 0 | &#9989; | &#10060; |  &#10060; | &#10060; |
| A | &#9989; | &#9989; | &#10060; | &#10060; |
| B | &#9989; | &#10060; | &#9989; | &#10060; |
| AB | &#9989; | &#9989; | &#9989; | &#9989; |

In kidney exchanges it is possible to do a transplant even with 
incompatible blood groups, but the match is not so good. 

> Very often it is important to know so called Rh factor 
> which can be (-) or (+), however for the kidney transplants 
> this does not play a role. 

### Human Leukocyte Antigen System <a name="hla"></a>

**TODO**