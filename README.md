[![Pytest](https://github.com/languagetooler-gmbh/rule-creation-stats/actions/workflows/pytest.yml/badge.svg)](https://github.com/languagetooler-gmbh/rule-creation-stats/actions/workflows/pytest.yml)
[![Flake8](https://github.com/p-goulart/rule-id-dump/actions/workflows/flake8.yml/badge.svg)](https://github.com/p-goulart/rule-id-dump/actions/workflows/flake8.yml)

# Rule Creation Stats
This project contains a bunch of scripts used to dump rule IDs, count them, diff them, etc.

## Schedule
All of the scripts listed here are set to run at 3AM every weekday.

## Quarterly stats
The start of the quarter is defined arbitrarily by tagging our repos with a tag such as `2023q1`. This tag is arbitrary and, therefore, must be updated manually in the GitHub Actions variables of this repo (@p-goulart can do this).

## Scripts
### Summary

|script|artefact name|artefact contents|
|---|---|---|
|dump_all|rule-dump-latest|a flat list of all current rule IDs|
|compare|added-rules|a flat list of all rule IDs added **in the current quarter**|
|master_csv|all_rules|a massive CSV containinng data for every single rule in every locale|
|style_stats|style_stats|`all_time_summary.txt`: all currently `tone_tag`ged rules;`added_this_quarter.txt` changes in style rules as a differential in tone tag numbers|

### `dump_all`

This simple utility can serve as a sort of sanity test for the code here. All it does is print out a list of unique rule IDs from the **latest** XML files on the `master` branch of both the OS and premium repositories, e.g.:

```
ABKUERZUNG_FALSCHE_PUNKTE
ABKUERZUNG_FEHLENDE_PUNKTE
ABKUERZUNG_LEERZEICHEN
ABLAUF_SUBST
ABRAHAM_LINCOLN
ABREITEN_VS_ARBEITEN
ABSAGE_SUBST
```

#### Artefact structure

```
├── de
│   ├── os.txt
│   └── premium.txt
├── en
│   ├── os.txt
│   └── premium.txt
├── es
│   ├── os.txt
│   └── premium.txt
├── fr
│   ├── os.txt
│   └── premium.txt
├── nl
│   ├── os.txt
│   └── premium.txt
└── pt
    ├── os.txt
    └── premium.txt
```

### `compare`

A version of `dump_all` that only prints rule IDs created in the **current quarter**, e.g.:

```
ABKUERZUNG_FALSCHE_PUNKTE
ABKUERZUNG_FEHLENDE_PUNKTE
ABKUERZUNG_LEERZEICHEN
ABLAUF_SUBST
ABRAHAM_LINCOLN
ABREITEN_VS_ARBEITEN
ABSAGE_SUBST
```


#### Artefact structure

```
├── de
│   ├── os.txt
│   └── premium.txt
├── en
│   ├── os.txt
│   └── premium.txt
├── es
│   ├── os.txt
│   └── premium.txt
├── fr
│   ├── os.txt
│   └── premium.txt
├── nl
│   ├── os.txt
│   └── premium.txt
└── pt
    ├── os.txt
    └── premium.txt
```

### `master_csv`

This script is meant to provide an all-encompassing view of **all** rules created by the lingu team in **one single file** – this means *all locales* are present in the same file. For example:

```csv
row,id,subId,locale,source_repo,type,source_file,tone_tags,writing_goals,is_goal_specific
0,IN_SHANGHAI,1,en,os,grammar,grammar.xml,,,false
1,IN_SHANGHAI,2,en,os,grammar,grammar.xml,,,false
2,LOWERCASE_NAMES,1,fr,premium,grammar,grammar.xml,,,false
3,SOME_EXAMPLE,1,es,os,style,grammar.xml,professional,serious,true
```

#### Table headers

|header|description|
|---|---|
|row|row number, not unique or stable, please don't use this for anything programmatic|
|id|rule ID – if the rule is a sub-rule of a rulegroup, the ID will be that of the rulegroup|
|subId| sub rule ID – index of a (sub-)rule. The subId of a standalone rule is always `[1]`|
|source_repo|'os' or 'premium'|
|type|'grammar', 'style', or 'unknown'|
|source_file|the path to the file where this rule comes from|
|tone_tags|comma-separated list of `tone_tags` applied to the the rule, including those inherited from rulegroups and categories|
|writing_goals|comma-separate list of writing goals served by the tone tags in the previous column|
|is_goal_specific|boolean value of `is_goal_specific` rule attribute|


### `style_stats`

This script generates **two** artefacts.

The `all_time_summary.txt` file contains a count of the **latest** (per `master` branch) rule counts **per `tone_tag`**, e.g.:

```
repo     tone_tags   
os       formal          602
         clarity         289
         untagged        184
         objective        68
         academic         60
         professional     13
         povrem            8
         informal          4
         positive          3
         general           2
premium  formal           49
         confident        23
         professional     23
         positive          5
         objective         2
         clarity           1
```

The `added_this_quarter.txt` file provides us with the tone_tag differential for **the current quarter**. Each positive value means we can count more rules for that tone tag now than at the beginning of the quarter, and a negative value means that we can count fewer (i.e. rules have been deleted or re-tagged).

For example, the following data tells us that we have 'lost' 11 `clarity` rules and 'gained' 5 `professional` ones:

```
clarity,-11
formal,5
general,1
untagged,0
confident,-1
informal,0
academic,0
professional,5
persuasive,4
```

#### Artefact structure

```
├── de
│   ├── added_this_quarter.txt
│   └── all_time_summary.txt
├── en
│   ├── added_this_quarter.txt
│   └── all_time_summary.txt
├── es
│   ├── added_this_quarter.txt
│   └── all_time_summary.txt
├── fr
│   ├── added_this_quarter.txt
│   └── all_time_summary.txt
├── nl
│   ├── added_this_quarter.txt
│   └── all_time_summary.txt
└── pt
    ├── added_this_quarter.txt
    └── all_time_summary.txt
```
