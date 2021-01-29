# Transplant Matching

REST API for solving the
[kidney-exchange problem](https://en.wikipedia.org/wiki/Kidney_Paired_Donation)
that uses compatibility in [blood type](#blood_types)
and in the [human leukocyte antigen](#hla) (HLA)
system to evaluate compatibility.

## Installation

### Native

Requires `python-3.8.5` and [anaconda](https://docs.anaconda.com/anaconda/install/). To create anaconda environment run:

```commandline
make conda-create
```

All scripts are configured to be run from the path of the root `transplants` directory.

## Medical Background

### Blood Types <a name="blood_types"></a>

Humans have 4 basic blood types `0`, `A`, `B`, `AB`. Those have different antigens (protein structures) on the surface
of red blood cells and different antibodies (other protein structures) floating in plasma.

|   | 0 | A | B | AB |
|---|---|---|---|----|
| antibodies in plasma | anti-A and anti-B | anti-B | anti-A | none |
| antigens in red blood cell | none | A antigen | B antigen | A and B antigens |

Two people with the same blood group are compatible (in blood group). In addition to this also pairs of donor (columns)

- recipient (rows) described by the following table are also compatible. **Basically the rule is that donor can give
  blood to recipient if the recipient has no antibodies for the donor's antigens.**

| donor &nbsp;&#9656; <hr>recipient &#9660;| 0 | A | B | AB |
|:---|---|---|---|---|
| 0 | &#9989; | &#10060; |  &#10060; | &#10060; |
| A | &#9989; | &#9989; | &#10060; | &#10060; |
| B | &#9989; | &#10060; | &#9989; | &#10060; |
| AB | &#9989; | &#9989; | &#9989; | &#9989; |

In kidney exchanges it is possible to do a transplant even with incompatible blood groups, but the match is not so good.

> Very often it is important to know so-called Rh factor
> which can be (-) or (+), however for the kidney transplants
> this does not play a role.

### Human Leukocyte Antigen (HLA) System <a name="hla"></a>

The HLA system is much more complicated than the blood groups but in many ways similar. This system is responsible for
determining own from foreign in body and is the basis for our immune system. For our purposes it (similarly as the blood
type) consists of different protein structures (antigens) on the surface of cells and other protein structures (
antibodies) in blood stream.

- In a transplant setting the situation is similar as for the blood groups -- if recipient has (unacceptably high
  concentration of)
  antibodies for donor's antigens, then the transplant can't be performed -- we call this **positive crossmatch**.
- The secondary goal is to have the antigens of recipient and antigens of donor as similar as possible.
- A healthy person does not have antibodies against their own antigens (this is the case with autoimmune diseases).
- The antibodies can be created by the body itself for example in reaction to blood transfusion, during a pregnancy etc.
  So basically genetically identical individuals can still have different antibodies. Normally they are not present.
- The protein structures (antigens) on the other hand are coded in one's DNA by Major Histocompatibility Gene
  Complex (**MHC**)
  that resides on a 3.6Mpb stretch within the chromosome 6p21 and contains 224 genes (e.g. HLA-A, HLA-B, HLA-DR). Sometimes
  it is also called HLA complex.
- Each human has two [alleles](http://hla.alleles.org/alleles/class1.html) (=variants, e.g. <i>A\*01:01:01:07</i>,
  <i>C\*01:02:01:08</i>, <i>B\*07:02:01:21</i>) for each MHC gene (one from the mother and one from the father).
- [MHC genes](http://hla.alleles.org/genes/index.html) are very polymorphic - i.e. they have many possible
  alleles
- The HLA genes can be divided in different groups:
    - MHC class I (e.g. HLA-A, HLA-B, HLA-C)
    - MHC class II (e.g. HLA-DP, HLA-DQ, HLA-DR)

  the antigens corresponding to class I are present on most nucleated cells of the body, whereas antigens corresponding
  to class II only occur on antigen-presenting cells, B cells, and T cells.

- Given the exact alleles of the genes in the HLA complex, the HLA antigens are determined.
- With a transplant there can't be a better case than if donor and recipient have the exact same HLA alleles (and thus
  the exact same antigens). See for
  example [Survival of DNA HLA-DR typed and matched cadaver kidney transplants](https://pubmed.ncbi.nlm.nih.gov/1678443/)
  .
- Finding the exact allele match is however not always possible, and it is also not always possible to use exact DNA
  based HLA typing. In our particular application, we focus on so
  called [serological antigen definitions](http://hla.alleles.org/antigens/recognised_serology.html)
  which define antigens based on serological reactions.
- These definitions are not so precise - even a person that is completely matched on "serological level" (=has the same
  serologically defined antigens) does not have to be matched on the allele level (=does not have to have the same
  alleles and not even the exact same antigens). However, person that is matched on serological level is still much
  better off than person not matched at all.
- If we know the complete allele typing, it is possible to find out the serological definition. A help with this can be
  the
  [HLA dictionary](https://www.ebi.ac.uk/ipd/imgt/hla/dictionary.html) which contains this information for many alleles.

The following is (as of 13. 12. 2020) list of recognized serologically
defined [antigens](http://hla.alleles.org/antigens/recognised_serology.html).

| A | B | C | D | DR | DQ | DP |
|---|---|---|---|----|----|----|
A1 | B5 | Cw1 | Dw1 | DR1 | DQ1 | DPw1
A2 | B7 | Cw2 | Dw2 | DR103 | DQ2 | DPw2
A203 | B703 | Cw3 | Dw3 | DR2 | DQ3 | DPw3
A210 | B8 | Cw4 | Dw4 | DR3 | DQ4 | DPw4
A3 | B12 | Cw5 | Dw5 | DR4 | DQ5(1) | DPw5
A9 | B13 | Cw6 | Dw6 | DR5 | DQ6(1) | DPw6
A10 | B14 | Cw7 | Dw7 | DR6 | DQ7(3) |
A11 | B15 | Cw8 | Dw8 | DR7 | DQ8(3) |
A19 | B16 | Cw9(w3) | Dw9 | DR8 | DQ9(3) |
A23(9) | B17 | Cw10(w3) | Dw10 | DR9 |   |
A24(9) | B18 |   | Dw11(w7) | DR10 |   |
A2403 | B21 |   | Dw12 | DR11(5) |   |
A25(10) | B22 |   | Dw13 | DR12(5) |   |
A26(10) | B27 |   | Dw14 | DR13(6) |   |
A28 | B2708 |   | Dw15 | DR14(6) |   |
A29(19) | B35 |   | Dw16 | DR1403 |   |
A30(19) | B37 |   | Dw17(w7) | DR1404 |   |
A31(19) | B38(16) |   | Dw18(w6) | DR15(2) |   |
A32(19) | B39(16) |   | Dw19(w6) | DR16(2) |   |
A33(19) | B3901 |   | Dw20 | DR17(3) |   |
A34(10) | B3902 |   | Dw21 | DR18(3) |   |
A36 | B40 |   | Dw22 |   |   |
A43 | B4005 |   | Dw23 | DR51 |   |
A66(10) | B41 |   | Dw24 | DR52 |   |
A68(28) | B42 |   | Dw25 | DR53 |   |
A69(28) | B44(12) |   | Dw26 |   |   |
A74(19) | B45(12) |   |   |   |   |
A80 | B46 |   |   |   |   |
|  | B47 |   |   |   |   |
|  | B48 |   |   |   |   |
|  | B49(21) |   |   |   |   |
|  | B50(21) |   |   |   |   |
|  | B51(5) |   |   |   |   |
|  | B5102 |   |   |   |   |
|  | B5103 |   |   |   |   |
|  | B52(5) |   |   |   |   |
|  | B53 |   |   |   |   |
|  | B54(22) |   |   |   |   |
|  | B55(22) |   |   |   |   |
|  | B56(22) |   |   |   |   |
|  | B57(17) |   |   |   |   |
|  | B58(17) |   |   |   |   |
|  | B59 |   |   |   |   |
|  | B60(40) |   |   |   |   |
|  | B61(40) |   |   |   |   |
|  | B62(15) |   |   |   |   |
|  | B63(15) |   |   |   |   |
|  | B64(14) |   |   |   |   |
|  | B65(14) |   |   |   |   |
|  | B67 |   |   |   |   |   |

#### Broads & Splits

Sometimes due to development in the serological typing new antigens were defined which were previously recognized as one
antigen. In the table above those are listed in parentheses. For example antigens A23 and A24 were defined as splits of
A9.
> If a donor has antigen A23 and recipient has antibody for A24 (=anti(A24)) then this is not a reason for positive crossmatch
> (and thus not a reason for not performing the transplant).
> This is the same with A24 > anti(A23) situation.
>
> For the situation A23 > anti(A23) we obviously have a positive crossmatch (so
> the transplant can't be performed).
>
> **CAUTION**  Must be taken with situation A23 > anti(A9) or
> A24 > anti(A9) because here the anti(A9) can mean antibodies for both A23, A24.
>
> **CAUTION** Must also be taken in situation A9 > anti(A23), A9 > anti(A24), A9 > anti(A9).
>
> In our algorithm we assume the case as if A9 = (A23, A24) and anti(A9) = (anti(A23), anti(A24))