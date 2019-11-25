# Index Sorting Benchmarks

## Overview

## Methodology

## Baseline Sorting Benchmarks

Before developing a Proof of Concept for default sorting, first tests were run to determine the impact of sorting on performance.

### Testing Parameters
* __Env__: prd
* __Index__: funding-company-read
* __Number of Iterations__: 25
* __From__: 0
* __Size__: 10
* __Num Search Terms__: 5

### Results

#### Base Query vs No Sorts

Note: a document is sorted by _score, by default, so we expected this to be similar to `Base Query vs Score Sort`

Num Results|Num Current Funding Query Hits|Num No Sort Funding Query Hits|Current Funding Query Avg Time|No Sort Funding Query Avg Time|\% Decrease in Avg|Current Funding Query Median Time|No Sort Funding Query Median Time|\% Decrease in Median|Current Funding Query 95th Percentile|No Sort Funding Query 95th Percentile|\% Decrease in 95th Percentile
------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------
10|500|500|9882.4793|361.50028|**96.34201**|9625.4704|304.19505|**96.83969**|14550.07005|567.25621|**96.10135**


#### Base Query vs Score Sort

Note: a document is sorted by _score, by default, so we expected this to be similar to `Base Query vs No Sorts`

Num Results|Num Current Funding Query Hits|Num No Sort Funding Query Hits|Current Funding Query Avg Time|No Sort Funding Query Avg Time|\% Decrease in Avg|Current Funding Query Median Time|No Sort Funding Query Median Time|\% Decrease in Median|Current Funding Query 95th Percentile|No Sort Funding Query 95th Percentile|\% Decrease in 95th Percentile
------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------
10|250|250|9975.47878|323.13507|**96.76071**|9281.47912|266.95085|**97.12383**|16163.30099|516.50524|**96.80446**

#### Base Query vs Score and Id Doc Sort

Num Results|Num Current Funding Query Hits|Num No Sort Funding Query Hits|Current Funding Query Avg Time|No Sort Funding Query Avg Time|\% Decrease in Avg|Current Funding Query Median Time|No Sort Funding Query Median Time|\% Decrease in Median|Current Funding Query 95th Percentile|No Sort Funding Query 95th Percentile|\% Decrease in 95th Percentile
------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------
10|250|250|11002.34768|10225.05185|**7.06482**|10104.27618|9919.8482|*1.82525*|17576.62892|17156.6782|*2.38926*
