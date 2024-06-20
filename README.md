# Edutain

## Problem:

People be watching TikTok/YouTube and not be learning things.

In the age of ***AI*** (aYy-EyE...), it's super easy to fall into learning -- malaise.

## Solution:

Edutain.

(Note: I'll be workshopping and building this as a CS major. Thinking primarily stats kind of lessons for debugging purposes.)

## MVP:

Upload an EPUB.

Parse the EPUB and put it in a format that's ingestable for an LLM.

Have the LLM generate a .yml-esque format of flash card questions.

You finish a chapter of your book, head here and complete the flash cards to test comprehension.

Come back later and do some spaced repetition review.

Fin.

## Problems:

There is no simple flag that designates whether an EPUB HTML DOC is a chapter or not.

So, I'm getting wild outputs when parsing the EPUBs. For example:
[('Gödel, Escher, Bach: An Eternal Golden Braid', {})]
id1114 True 116
id1113 True 93
id1112 True 161
id1111 True 165
id1110 True 99
id1109 True 83
id1108 True 72
id1107 True 128
id1106 True 125
id1105 True 92
id1104 True 388
id1103 True 188
id1102 True 84
id1101 True 259
id1100 True 8621
id199 True 84157
id198 True 30305
id197 True 43712
id196 True 38836
id195 True 165065
id194 True 58141
id193 True 46491
id192 True 94042
id191 True 74198
id190 True 97654
id189 True 125704
id188 True 102644
id187 True 73746
id186 True 64929
id185 True 65955
id184 True 137844
id183 True 84037
id182 True 127278
id181 True 102262
id180 True 147053
id179 True 148
id178 True 350
id177 True 403
id176 True 781
id175 True 524
id174 True 1551
id173 True 1114
id172 True 89767
id139 True 58651
id138 True 2513
titlepage True 6
count        46.000000
mean      41968.152174
std       50186.998673
min           6.000000
25%         162.000000
50%        5567.000000
75%       81577.250000
max      165065.000000
dtype: float64

[('A Brief History of Intelligence', {})]
Contents1 False 25174
Cover-page True 87
Titlepage True 73
Dedication True 125
Epigraph True 390
Contents True 3104
Frontmatter_1 True 219
Frontmatter_2 True 203
Frontmatter_3 True 381
Introduction True 30520
Chapter_1 True 38893
Part_1 True 362
Chapter_2 True 26705
Chapter_3 True 32074
Chapter_4 True 28807
Chapter_4a True 1870
Part_2 True 368
Chapter_5 True 16398
Chapter_6 True 35489
Chapter_7 True 37041
Chapter_8 True 7528
Chapter_9 True 10980
Chapter_9a True 2284
Part_3 True 358
Chapter_10 True 18123
Chapter_11 True 37204
Chapter_12 True 29102
Chapter_13 True 41858
Chapter_14 True 20820
Chapter_14a True 3166
Part_4 True 361
Chapter_15 True 34082
Chapter_16 True 25202
Chapter_17 True 33494
Chapter_18 True 13702
Chapter_18a True 3894
Part_5 True 348
Chapter_19 True 30845
Chapter_20 True 26388
Chapter_21 True 41353
Chapter_22 True 27852
Chapter_22a True 1844
Conclusion True 14879
Acknowledgments True 7127
Glossary True 7270
Bibliography True 3138
Notes True 107696
Index True 36010
About_the_Author True 1214
Praise True 4062
BA True 111
Copyright True 1601
About_the_Publisher True 1137
Footnote_1 True 531
Footnote_2 True 155
Footnote_3 True 135
Footnote_4 True 336
Footnote_5 True 196
Footnote_6 True 321
Footnote_7 True 274
Footnote_8 True 227
Footnote_9 True 732
Footnote_10 True 315
Footnote_11 True 193
Footnote_12 True 249
Footnote_13 True 436
Footnote_14 True 1485
Footnote_15 True 1105
Footnote_16 True 146
Footnote_17 True 174
Footnote_18 True 361
Footnote_19 True 199
Footnote_20 True 249
Footnote_21 True 296
Footnote_22 True 214
Footnote_23 True 156
Footnote_24 True 149
Footnote_25 True 188
Footnote_26 True 211
Footnote_27 True 146
Footnote_28 True 120
Footnote_29 True 381
Footnote_30 True 270
count        83.000000
mean      10641.759036
std       17326.979556
min          73.000000
25%         238.000000
50%        1105.000000
75%       19471.500000
max      107696.000000
dtype: float64

[('The Feynman Lectures on Physics, Volume 3', {})]
Xcd61133dc93ecfbfb26bd24e898096d8 True 76
X16b04373e98e42f5aae13f717dc8ade2 True 1208
X4c8adb4b9039843ebf80fc4b555fb749 True 2048
X80db8fafa8d471841f3d0943fc13d083 True 8088
Xef44322989c70dc83a6a1152a913640f True 16719
X9c5e5cab917251866e2f5ad4e384b9b8 True 79
X15d3e5059799a3f0bcf635a4a86b279b True 10273
Xa0a54f2b2b06b941663bbd9c85820490 True 6190
X4bd7b7afb34a55609b97d03bc72fa27e True 43786
X3f856f5b0914865b9688954dfd879d6f True 40666
X6b6cbd82f554c9e480ad21c212fe5377 True 43279
X3d21710e872c6af03991df9ebd9a52db True 53605
Xb6d38ba79d6d363bc6bbc135a41668a8 True 51545
X90f6c23d706d5f688529a143d25cf06f True 49297
X42b48bb6451c77cb0c61712c3a196770 True 41819
Xa71880380ab55e014a47ed945b1389ff True 52501
Xb4d1b86e1834ec05852fcc053014b883 True 52344
Xf7214da24a318f7b6da6d1d7c984d085 True 64895
X65ae7d5a5fb4d4c289fbcff6e85f119f True 86571
Xa1dc808eebc546b56b00d2845dd11d6a True 55982
Xaffcc070dfef459e42f02da1c7867428 True 47083
X9c35624f94556a272673ff09c18f1479 True 52685
Xe8e44dbfbc1f1cb820f43a7939e59bd0 True 54335
X342fc8a7e187213eaaa682c8b836809c True 61020
X40411457dce202c7b1a6035b91a2bb52 True 67290
X8595e5e3ee67ff4723b479efad9ebc89 True 79152
X0c1a7714ac8db2cc68fd1ee653799350 True 57133
X6d9e89b801e5d04e6d2c58a390cf7f55 True 58657
Xd2a6e6dabd527881901ae661ccde14f6 True 65244
X5d669a5c0dea8ad41b38080603c404ff True 1751
X875aab21c9c4052ee6cc656f8ca14efa True 9615
X89fb02a5d5d3451e3ca895ab227bcc0c True 25
count       32.00000
mean     38592.53125
std      26543.98999
min         25.00000
25%       9233.25000
50%      48190.00000
75%      56269.75000
max      86571.00000
dtype: float64


[('Introduction to Quantum Algorithms via Linear Algebra', {'id': 'title'})]
nav False 23129
html-cover-page True 36
title_page True 190
copyright True 1283
dedication True 184
contents True 14288
preface1 True 5584
preface2 True 3764
acknowledgments True 1114
part_1 True 74
chapter_1 True 20210
chapter_2 True 13966
chapter_3 True 24006
chapter_4 True 36005
chapter_5 True 20913
chapter_6 True 24776
chapter_7 True 27917
chapter_8 True 19001
chapter_9 True 7588
chapter_10 True 8471
chapter_11 True 22971
chapter_12 True 10050
chapter_13 True 15764
part_2 True 74
chapter_14 True 81522
chapter_15 True 16728
chapter_16 True 26956
chapter_17 True 37494
chapter_18 True 35957
chapter_19 True 42611
chapter_20 True 15591
references True 18944
index True 36506
count       33.000000
mean     18595.969697
std      16910.857576
min         36.000000
25%       5584.000000
50%      16728.000000
75%      24776.000000
max      81522.000000
dtype: float64

[('The Black Swan', {})]
cvi True 51
col1 True 2283
adc True 64
tp True 50
ded True 56
toc True 22607
fm1 True 441
prl True 30889
p01 True 3301
c01 True 48872
c02 True 5612
c03 True 28240
c04 True 29561
c05 True 27945
c06 True 55726
c07 True 34773
c08 True 52754
c09 True 28745
p02 True 3610
c10 True 69919
c11 True 58955
c12 True 24554
c13 True 25400
p03 True 1762
c14 True 33649
c15 True 52372
c16 True 45240
c17 True 27593
c18 True 14508
p04 True 6
c19 True 7005
epl True 2620
bm1 True 8407
bm2 True 56
bm3 True 42051
bm4 True 14014
bm5 True 22033
bm6 True 20200
bm7 True 35413
bm8 True 9488
bm9 True 14916
bm10 True 5655
bm11 True 4798
nts True 67522
bib True 111245
ack True 11412
ata True 628
cop True 1106
count        48.000000
mean      23085.562500
std       23919.788405
min           6.000000
25%        3130.750000
50%       17558.000000
75%       33930.000000
max      111245.000000
dtype: float64

**ALL** of these are *valid* potential chapter namings. The bool is whether the ebooklib library says whether the doc is a chapter or not. Which is obviously invalid.

So, I'm going to have to use the char count to determine as well as some regex that catches common namings. But, checkout 'A Brief History of Intelligence'. Some of those chapters have suffixes... and the char count is invalid. 

I'll need to find a way to split these chapters up effectively for ingestion.

## Goal:

You can learn new things and retain the information long-term using this service.

## Tech Stack:

Svelte frontend.

Flask backend.

Firebase/Google Cloud for hosting both.

Firestore for DB.

## Features:

User login/signup flow.

Post-chapter quiz.

Spaced repition review.

Mobile-first UI. iOS "Add to Home Screen" install flow.

## Resources:

https://medium.com/@retzd/exploring-the-power-of-python-with-firebase-cloud-functions-a-comparison-with-microservices-544dcbcb0d51